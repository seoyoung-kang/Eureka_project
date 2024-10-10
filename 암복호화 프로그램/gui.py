import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cham import CHAM_CTR_Encryption, CHAM_key_schedule, int_to_bytes, hex_to_int
import os



root = tk.Tk()
root.title("File Encryptor/Decrytor")
root.geometry("400x600")

button_frame = tk.Frame(root)
button_frame.pack(pady = 10, fill = tk.X, padx=10)

select_button = tk.Button(button_frame, text="Select File", command = select_file)
select_button.pack(side=tk.LEFT, padx=5)

select_button = tk.Button(button_frame, text="Select File", command = save_file)
select_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()