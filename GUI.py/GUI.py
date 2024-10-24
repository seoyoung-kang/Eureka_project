import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from CHAM_generalization import *  # CHAM 알고리즘 관련 함수들을 가져옵니다.

# CHAM 보안 레벨에 따른 설정
def Cham_security_level(security_level):
    if security_level == '128':
        return 128, 16, 88, mk_low
    elif security_level == '192':
        return 128, 32, 112, mk_medium
    elif security_level == '256':
        return 256, 32, 120, mk_high

# 파일 선택 다이얼로그
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        original_image.set(file_path)
        load_image(file_path, original_image_label)

# 이미지 로드 및 표시
def load_image(image_path, label):
    image = Image.open(image_path)
    image = image.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    label.config(image=img)
    label.image = img  # Reference 유지

# 이미지 암호화
def encrypt_image():
    file_path = original_image.get()
    if not file_path:
        messagebox.showerror("Error", "이미지를 선택하세요!")
        return

    # 이미지 파일을 열고 바이트로 읽기
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()

    # 보안 레벨 선택
    security_level = security_level_var.get()
    k, w, r, mk = Cham_security_level(security_level)
    rk = CHAM_key_schedule(mk, k, w)

    # 이미지 데이터를 CHAM 암호화
    image_data_ints = bytes_to_int(image_data)
    encrypted_data_ints = CHAM_CTR_Encryption(image_data_ints, rk, len(image_data_ints), k, w, r)
    encrypted_data_bytes = int_to_bytes(encrypted_data_ints)

    # 암호화된 데이터를 새 파일로 저장
    encrypted_file_path = os.path.splitext(file_path)[0] + "_encrypted.png"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data_bytes)

    # 암호화된 이미지 로드 및 표시
    load_image(encrypted_file_path, encrypted_image_label)
    encrypted_image.set(encrypted_file_path)  # 암호화된 파일 경로 저장
    print(f"암호화된 파일 경로: {encrypted_image.get()}")  # 경로가 제대로 설정되었는지 확인
    messagebox.showinfo("Encryption", "이미지가 암호화되었습니다!")

# 이미지 복호화
def decrypt_image():
    file_path = encrypted_image.get()
    if not file_path:  # 암호화된 이미지가 선택되지 않았을 때
        messagebox.showerror("Error", "암호화된 이미지를 선택하세요!")
        return

    if not os.path.exists(file_path):  # 선택된 파일 경로가 실제로 존재하는지 확인
        messagebox.showerror("Error", "선택한 암호화된 파일을 찾을 수 없습니다!")
        return

    # 암호화된 이미지 파일을 바이트로 읽기
    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    # 보안 레벨 선택
    security_level = security_level_var.get()
    k, w, r, mk = Cham_security_level(security_level)
    rk = CHAM_key_schedule(mk, k, w)

    # 암호화된 데이터를 CHAM 복호화
    encrypted_data_ints = bytes_to_int(encrypted_data)
    decrypted_data_ints = CHAM_CTR_Encryption(encrypted_data_ints, rk, len(encrypted_data_ints), k, w, r)
    decrypted_data_bytes = int_to_bytes(decrypted_data_ints)

    # 복호화된 데이터를 새 파일로 저장
    decrypted_file_path = os.path.splitext(file_path)[0] + "_decrypted.png"
    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data_bytes)

    # 복호화된 이미지 로드 및 표시
    load_image(decrypted_file_path, decrypted_image_label)
    messagebox.showinfo("Decryption", "이미지가 복호화되었습니다!")

# Tkinter GUI 설정
root = tk.Tk()
root.title("CHAM Image Encryption & Decryption")
root.geometry("600x500")

# 보안 레벨 선택
security_level_var = tk.StringVar(value='128')
tk.Label(root, text="보안 레벨을 선택하세요").pack(pady=10)
tk.Radiobutton(root, text="128비트", variable=security_level_var, value='128').pack()
tk.Radiobutton(root, text="192비트", variable=security_level_var, value='192').pack()
tk.Radiobutton(root, text="256비트", variable=security_level_var, value='256').pack()

# 이미지 선택 버튼 및 경로 표시
tk.Button(root, text="이미지 선택", command=select_file).pack(pady=10)
original_image = tk.StringVar()
tk.Label(root, textvariable=original_image).pack()

# 원본 이미지 표시
original_image_label = tk.Label(root)
original_image_label.pack(pady=10)

# 암호화된 이미지 표시
tk.Label(root, text="암호화된 이미지").pack(pady=10)
encrypted_image = tk.StringVar()
encrypted_image_label = tk.Label(root)
encrypted_image_label.pack(pady=10)

# 복호화된 이미지 표시
tk.Label(root, text="복호화된 이미지").pack(pady=10)
decrypted_image_label = tk.Label(root)
decrypted_image_label.pack(pady=10)

# 암호화 및 복호화 버튼
tk.Button(root, text="Encrypt", command=encrypt_image).pack(pady=10)
tk.Button(root, text="Decrypt", command=decrypt_image).pack(pady=10)

root.mainloop()

