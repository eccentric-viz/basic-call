import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageGrab
import base64
import requests
import io

API_URL = "https://ianpan-diabetic-retinopathy.hf.space/run/predict"

def send_image_to_api(img_bytes):
    img_b64 = "data:image/jpeg;base64," + base64.b64encode(img_bytes).decode()
    payload = {"data": [img_b64]}
    response = requests.post(API_URL, json=payload)
    return response.json()

def show_prediction(result):
    try:
        label = result["data"][0]["label"]
        confs = result["data"][0]["confidences"]
        text = f"Prediction: {label}\n\n"

        for c in confs:
            text += f"{c['label']}: {round(c['confidence'], 4)}\n"

        messagebox.showinfo("Result", text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to parse API response\n{e}")

def upload_image():
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png")]
    )
    if not path:
        return
    try:
        with open(path, "rb") as f:
            img_bytes = f.read()
        result = send_image_to_api(img_bytes)
        show_prediction(result)
    except Exception as e:
        messagebox.showerror("Error", f"Upload failed\n{e}")

def paste_image(event=None):
    try:
        img = ImageGrab.grabclipboard()
        if img is None:
            messagebox.showwarning("Warning", "Clipboard does not contain an image")
            return

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()

        result = send_image_to_api(img_bytes)
        show_prediction(result)

    except Exception as e:
        messagebox.showerror("Error", f"Paste failed\n{e}")

root = tk.Tk()
root.title("DR Detection")
root.geometry("400x200")

label = tk.Label(root, text="Upload or paste an image", font=("Arial", 14))
label.pack(pady=20)

upload_btn = tk.Button(root, text="Upload Image", command=upload_image, width=20, height=2)
upload_btn.pack()

root.bind("<Control-v>", paste_image)

root.mainloop()
