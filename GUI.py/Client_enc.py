# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from CHAM_generalization import *
import socket
import os
import threading

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5550
# Connect to the server (서버에 연결)
s.connect((host, port))

# 이미지 파일 리스트
valid_files = ['heart.png', 'penguin.png', 'puppy.png', 'beer.png', 'black_cat.png', 'cat.png']

# 이미지 전송 함수
def send_image():
    selected_file = file_var.get()  # 드롭다운에서 선택한 파일 이름
    if selected_file:
        security_level = security_var.get()  # 드롭다운에서 선택한 보안 레벨
        if not security_level:
            messagebox.showerror("Error", "보안 레벨을 선택하세요.")
            return

        # 네트워크 작업을 별도의 스레드에서 실행
        threading.Thread(target=send_data, args=(selected_file, security_level)).start()

def send_data(file_name, security_level):
    k, w, r, mk = socket_security_level(security_level)
    rk = CHAM_key_schedule(mk, k, w)

    # 선택한 파일 읽기
    with open(file_name, "rb") as file_image:
        file_data = file_image.read()

    # 파일 데이터 hex형으로 변환
    file_data_hex = file_data.hex()
    Plaintext = hex_to_int(file_data_hex, len(file_data_hex))

    # 보안 레벨 전송
    s.send(security_level.encode('utf-8'))  # UTF-8로 인코딩하여 전송

    # 파일 암호화 수행
    ct = CHAM_CTR_Encryption(Plaintext, rk, len(Plaintext), k, w, r)

    # 암호화된 데이터 전송을 위해 byte형 변환
    ct_bytes = int_to_bytes(ct)

    # Send the encrypted message (암호화된 메시지 서버로 전송)
    s.send(ct_bytes)

    choice_continue = s.recv(1024).decode()

    if choice_continue == 'no':
        s.close()
        root.quit()

def close_program():
    if messagebox.askokcancel("Quit", "종료하시겠습니까?"):
        root.quit()  # GUI 종료
        s.close()    # 서버 소켓 종료

# GUI 설정
root = tk.Tk()
root.title("클라이언트")

# 보안 레벨 드롭다운 메뉴 생성
security_var = tk.StringVar(value="low")  # 기본값
security_menu = tk.OptionMenu(root, security_var, 'low', 'medium', 'high')
security_menu.pack(pady=20)

# 드롭다운 변수 설정
file_var = tk.StringVar(value=valid_files[0])  # 기본값은 첫 번째 파일

# 드롭다운 메뉴 생성
file_menu = tk.OptionMenu(root, file_var, *valid_files)
file_menu.pack(pady=20)

# 선택 버튼 생성
select_button = tk.Button(root, text="선택한 이미지 전송", command=send_image)
select_button.pack(pady=20)

# 종료 버튼 생성
exit_button = tk.Button(root, text="종료", command=close_program)
exit_button.pack(pady=10)


root.mainloop()