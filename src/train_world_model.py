# -*- coding: utf-8 -*-

import os
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score

# ------------------------------------------------------------
# Fix working directory
# ------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_ROOT)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

STATE_FILE = "data/processed/lane_time_tensor.csv"
GRAPH_FILE = "data/processed/lane_graph_edges.csv"

WINDOW = 20
HIDDEN_DIM = 32
EPOCHS = 15
LR = 0.001
BATCH_SIZE = 16

# ------------------------------------------------------------
# Load state tensor
# ------------------------------------------------------------
print("Loading state tensor...")
df = pd.read_csv(STATE_FILE)

lanes = sorted(df["lane_id"].unique())
lane_to_idx = {lane: i for i, lane in enumerate(lanes)}
num_lanes = len(lanes)

times = sorted(df["time"].unique())
num_timesteps = len(times)

print("Lanes:", num_lanes)
print("Timesteps:", num_timesteps)

# ------------------------------------------------------------
# Build feature + label tensors
# ------------------------------------------------------------
features = np.zeros((num_timesteps, num_lanes, 3))
labels = np.zeros((num_timesteps, num_lanes))

for _, row in df.iterrows():
    t = int(row["time"])
    i = lane_to_idx[row["lane_id"]]

    features[t, i, 0] = row["mean_speed"]
    features[t, i, 1] = row["vehicle_count"]
    features[t, i, 2] = row["violation_rate"]

    labels[t, i] = row["future_congestion"]

# Normalize features per feature
for f in range(features.shape[2]):
    mean = features[:, :, f].mean()
    std = features[:, :, f].std() + 1e-6
    features[:, :, f] = (features[:, :, f] - mean) / std

# ------------------------------------------------------------
# Create sliding windows
# ------------------------------------------------------------
print("Creating sliding windows...")

X = []
Y = []

for t in range(WINDOW, num_timesteps):
    X.append(features[t-WINDOW:t])
    Y.append(labels[t])

X = torch.tensor(np.array(X), dtype=torch.float32)
Y = torch.tensor(np.array(Y), dtype=torch.float32)

print("Total samples:", X.shape[0])

# ------------------------------------------------------------
# Train / Val / Test split (time-based)
# ------------------------------------------------------------
total_samples = X.shape[0]

train_end = int(0.7 * total_samples)
val_end = int(0.85 * total_samples)

X_train = X[:train_end].to(DEVICE)
Y_train = Y[:train_end].to(DEVICE)

X_val = X[train_end:val_end].to(DEVICE)
Y_val = Y[train_end:val_end].to(DEVICE)

X_test = X[val_end:].to(DEVICE)
Y_test = Y[val_end:].to(DEVICE)

print("Train samples:", X_train.shape[0])
print("Val samples:", X_val.shape[0])
print("Test samples:", X_test.shape[0])

# ------------------------------------------------------------
# Build adjacency matrix
# ------------------------------------------------------------
print("Building adjacency matrix...")
edges = pd.read_csv(GRAPH_FILE)

A = np.zeros((num_lanes, num_lanes))

for _, row in edges.iterrows():
    src = lane_to_idx[row["source_lane"]]
    tgt = lane_to_idx[row["target_lane"]]
    A[src, tgt] = 1

A += np.eye(num_lanes)

D = np.diag(1.0 / np.sqrt(A.sum(axis=1) + 1e-6))
A_hat = torch.tensor(D @ A @ D, dtype=torch.float32).to(DEVICE)

# ------------------------------------------------------------
# Model
# ------------------------------------------------------------
class WorldModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.gcn = nn.Linear(3, HIDDEN_DIM)
        self.lstm = nn.LSTM(HIDDEN_DIM, HIDDEN_DIM, batch_first=True)
        self.fc = nn.Linear(HIDDEN_DIM, 1)

    def forward(self, x):
        # x: [B, W, N, F]
        B, W, N, F = x.shape

        spatial_seq = []

        for t in range(W):
            xt = x[:, t]  # [B, N, F]
            xt = torch.relu(A_hat @ self.gcn(xt))
            spatial_seq.append(xt)

        spatial_seq = torch.stack(spatial_seq, dim=1)  # [B, W, N, H]

        # reshape for LSTM
        spatial_seq = spatial_seq.permute(0, 2, 1, 3)  # [B, N, W, H]
        spatial_seq = spatial_seq.reshape(B * N, W, HIDDEN_DIM)

        lstm_out, _ = self.lstm(spatial_seq)

        last_hidden = lstm_out[:, -1, :]  # [B*N, H]
        out = self.fc(last_hidden)  # [B*N, 1]

        out = out.reshape(B, N)
        return out

model = WorldModel().to(DEVICE)
optimizer = torch.optim.Adam(model.parameters(), lr=LR)

# Class imbalance handling
pos_count = (Y_train == 1).sum().item()
neg_count = (Y_train == 0).sum().item()
pos_weight = torch.tensor(neg_count / (pos_count + 1e-6)).to(DEVICE)

criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

# ------------------------------------------------------------
# Training loop
# ------------------------------------------------------------
print("\nTraining model...\n")

for epoch in range(EPOCHS):

    model.train()
    perm = torch.randperm(X_train.shape[0])
    total_loss = 0

    for i in range(0, X_train.shape[0], BATCH_SIZE):
        idx = perm[i:i+BATCH_SIZE]
        xb = X_train[idx]
        yb = Y_train[idx]

        optimizer.zero_grad()
        outputs = model(xb)
        loss = criterion(outputs, yb)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    # Validation
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val)
        val_loss = criterion(val_outputs, Y_val)

        preds = torch.sigmoid(val_outputs) > 0.5
        y_true = Y_val.cpu().numpy().flatten()
        y_pred = preds.cpu().numpy().flatten()

        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"Epoch {epoch+1}/{EPOCHS} | "
          f"Train Loss: {total_loss:.4f} | "
          f"Val Loss: {val_loss.item():.4f} | "
          f"Val F1: {f1:.4f}")

# ------------------------------------------------------------
# Final Test Evaluation
# ------------------------------------------------------------
model.eval()
with torch.no_grad():
    test_outputs = model(X_test)
    preds = torch.sigmoid(test_outputs) > 0.5

    y_true = Y_test.cpu().numpy().flatten()
    y_pred = preds.cpu().numpy().flatten()

    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

print("\nTest Results:")
print("Precision:", precision)
print("Recall:", recall)
print("F1:", f1)
print("\nTraining complete.")