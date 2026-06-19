import tkinter as tk
from tkinter import filedialog, messagebox

from pipeline.pipeline import run_pipeline


def browse():

    filename = filedialog.askopenfilename(
        filetypes=[("OSM files", "*.osm")]
    )

    entry.delete(0, tk.END)
    entry.insert(0, filename)


def generate():

    path = entry.get()

    if path == "":
        messagebox.showerror("Error", "Select an OSM file")
        return

    run_pipeline(path)

    messagebox.showinfo(
        "Success",
        "Dataset generated successfully!"
    )


root = tk.Tk()

root.title("Traffic Dataset Generator")
root.geometry("500x200")

label = tk.Label(root, text="Select OSM File")
label.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="Browse", command=browse)
button.pack(pady=5)

generate_btn = tk.Button(
    root,
    text="Generate Dataset",
    command=generate
)

generate_btn.pack(pady=20)

root.mainloop()
