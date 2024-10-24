# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from CHAM_generalization import *
import socket
import os
import threading

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5550

s.bind((host, port))
s.listen(1)
print("Server is listening for incoming connections")

cs, addr = s.accept()
print(f"Connection from: {addr}")

# 수신 데이터 함수
def receive_data():
    while True:
        try:
            # 보안 레벨 수신
            recv_data = cs.recv(1024)  # 클라이언트로부터 데이터 수신
            
            if not recv_data:
                print("No data received, closing connection.")
                break
            
            print(f"Received raw data: {recv_data}")  # 수신한 원본 데이터 로그
            
            security_level = recv_data.decode('utf-8')  # 바이트 데이터를 문자열로 변환
            print(f"Received security level: {security_level}")

            # 보안 레벨에 따라 키 스케줄링
            k, w, r, mk = socket_security_level(security_level)
            rk = CHAM_key_schedule(mk, k, w)

            # 클라이언트로부터 데이터 수신
            recv_data = cs.recv(50000)
            if not recv_data:
                print("No data received, closing connection.")
                break  # 연결이 끊어지면 종료
            
            # 수신한 데이터 처리
            recv_data_ints = bytes_to_int(recv_data)

            # 수신한 파일 암호문으로 저장
            with open("recieved_encrypted_file.png", "wb") as received_encrypted_file:
                received_encrypted_bytes = int_to_bytes(recv_data_ints)
                received_encrypted_file.write(received_encrypted_bytes)

            # 파일 복호화
            decrypted_data_ints = CHAM_CTR_Encryption(recv_data_ints, rk, len(recv_data_ints), k, w, r)

            # 수신한 파일 원본으로 저장
            with open("recieved_file.png", "wb") as received_file:
                received_bytes = int_to_bytes2(decrypted_data_ints)
                received_file.write(received_bytes)

            # GUI 업데이트
            update_gui("recieved_file.png")  # 수신한 이미지 표시
            choice_continue = messagebox.askyesno("Continue", "이미지를 계속 보내시겠습니까?")
            cs.send(str(choice_continue).encode('utf-8'))  # 선택 결과 전송

            if not choice_continue:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    cs.close()

# GUI 업데이트 함수
def update_gui(image_path):
    img = Image.open(image_path)
    img = img.resize((200, 200))  # 이미지 크기 조정
    img_tk = ImageTk.PhotoImage(img)

    img_label.config(image=img_tk)
    img_label.image = img_tk  # Keep a reference

# 종료 함수
def close_program():
    if messagebox.askokcancel("Quit", "종료하시겠습니까?"):
        root.quit()  # GUI 종료
        cs.close()   # 소켓 종료
        s.close()    # 서버 소켓 종료

# GUI 설정
root = tk.Tk()
root.title("서버")

# 이미지 표시할 Label
img_label = tk.Label(root)
img_label.pack(pady=20)

# 종료 버튼 추가
exit_button = tk.Button(root, text="종료", command=close_program)
exit_button.pack(pady=10)

# 수신 데이터 스레드 시작
threading.Thread(target=receive_data, daemon=True).start()

root.mainloop()