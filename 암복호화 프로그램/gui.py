import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from cham import CHAM_key_schedule, CHAM_CTR_Encryption, int_to_bytes, hex_to_int
import os


mk = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
rk = CHAM_key_schedule(mk, 128, 16)

def get_filename(path):
    return path.split("/")[-1]

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_listbox.delete(0, tk.END)  
        file_listbox.insert(tk.END, file_path) 
        
        try:
            image = Image.open(file_path)
            image.thumbnail((400, 400))  
            photo = ImageTk.PhotoImage(image)
            image_label.config(image=photo)
            image_label.image = photo 
        except IOError:
            image_label.config(image='') 
            image_label.image = None

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png", 
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
    if file_path:
        selected_file = file_listbox.get(tk.ACTIVE)
        if selected_file:
            try:
                file = open(selected_file, 'rb')
                file_data = file.read()
                save_file = open(file_path, 'wb')
                save_file.write(file_data)         
                save_file.close()
                file.close()
                
                messagebox.showinfo("Success", f"File saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            messagebox.showwarning("Warning", "No file selected to save.")

def encrypt_file():
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        try:
            file = open(selected_file, 'rb')
            file_data = file.read().hex()
            file_data = hex_to_int(file_data, len(file_data))
            enc_file_data = CHAM_CTR_Encryption(file_data, rk, len(file_data))
            file.close()
            
            enc_filepath = os.getcwd() + "/enc_" + get_filename(selected_file).split(".")[0]
            enc_file =  open(enc_filepath, 'wb')
            enc_file.write(int_to_bytes(enc_file_data))
            enc_file.close()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
    else:
        messagebox.showwarning("Warning", "No file selected for encryption.")

def decrypt_file():
    selected_file = file_listbox.get(tk.ACTIVE)
    if selected_file:
        try:
            file =  open(selected_file, 'rb')
            file_data = file.read().hex()
            file_data = hex_to_int(file_data, len(file_data))
            dec_file_data = CHAM_CTR_Encryption(file_data, rk, len(file_data))
            
            dec_filepath = os.getcwd() + "/dec_" + get_filename(selected_file).split(".")[0] + ".png" 
            dec_file =  open(dec_filepath, 'wb')
            dec_file.write(int_to_bytes(dec_file_data))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
    else:
        messagebox.showwarning("Warning", "No file selected for decryption.")


root = tk.Tk()
root.title("File Encryptor/Decryptor")
root.geometry("400x600")  # Set the window size to 400x600

button_frame = tk.Frame(root)
button_frame.pack(pady=10, fill=tk.X, padx=10)

select_button = tk.Button(button_frame, text="Select File", command=select_file)
select_button.pack(side=tk.LEFT, padx=5)

save_button = tk.Button(button_frame, text="Save File", command=save_file)
save_button.pack(side=tk.RIGHT, padx=5)

file_listbox = tk.Listbox(root, height=1, width=50)  
file_listbox.pack(pady=10, fill=tk.X, padx=10)  

encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_file)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_file)
decrypt_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()

