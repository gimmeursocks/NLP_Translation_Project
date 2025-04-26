import tkinter as tk
from tkinter import messagebox, ttk
import requests

GITHUB_TOKEN = ""
GIST_URL = "https://api.github.com/gists/16f74bf6e17c2641ab18fae28d3fc49b"

with open("github_token", "r") as f:
    for line in f:
        GITHUB_TOKEN = line

def get_kaggle_url():
    try:
        response = requests.get(
            GIST_URL,
            headers={"Authorization": f"token {GITHUB_TOKEN}"},
            timeout=5
        )
        gist_data = response.json()
        return gist_data["files"]["gistfile1.txt"]["content"].strip()
    except Exception as e:
        print("Failed to get URL:", e)
        return None

def check_connection():
    kaggle_url = get_kaggle_url()
    try:
        response = requests.get(f"{kaggle_url}/ping", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "ok":
            status_label.config(text="Connected to Kaggle: ✅", foreground="green")
        else:
            status_label.config(text="Connected to Kaggle: ❌", foreground="red")
    except:
        status_label.config(text="Connected to Kaggle: ❌", foreground="red")
    app.after(3000, check_connection)

def translate(event=None):
    kaggle_url = get_kaggle_url()
    if not kaggle_url:
        messagebox.showerror("Error", "Cannot connect to Kaggle notebook.")
        return

    text = input_text.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showerror("Error", "Input cannot be empty.")
        return

    try:
        response = requests.post(f"{kaggle_url}/translate", json={"text": text})
        if response.status_code == 200:
            result = response.json()["translation"]
            output_text.config(state='normal')
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, result)
            output_text.config(state='disabled')
        else:
            messagebox.showerror("Error", response.json().get("error", "Unknown error"))
    except Exception as e:
        messagebox.showerror("Error", f"Translation failed: {str(e)}")

# GUI Setup
app = tk.Tk()
app.title("🌐 English to Arabic Translator")
app.geometry("600x500")
app.configure(bg="#f9f9f9")

# Fonts and Styles
LABEL_FONT = ("Helvetica", 12)
TEXT_FONT = ("Courier New", 12)

# Status Label
status_label = ttk.Label(app, text="Checking connection...", font=LABEL_FONT, foreground="orange")
status_label.pack(pady=10)

# Input Section
input_frame = ttk.LabelFrame(app, text="Enter English Text", padding=10)
input_frame.pack(fill="x", padx=20, pady=10)

input_text = tk.Text(input_frame, height=6, font=TEXT_FONT, wrap="word")
input_text.pack(fill="x")
input_text.bind("<Return>", translate)
input_text.bind("<Shift-Return>", lambda e: input_text.insert("insert", "\n"))

# Translate Button
translate_button = ttk.Button(app, text="Translate ➡️", command=translate)
translate_button.pack(pady=10)

# Output Section
output_frame = ttk.LabelFrame(app, text="Arabic Translation", padding=10)
output_frame.pack(fill="x", padx=20, pady=10)

output_text = tk.Text(output_frame, height=6, font=TEXT_FONT, wrap="word", state='disabled')
output_text.pack(fill="x")

# Start checking connection
app.after(1000, check_connection)

app.mainloop()