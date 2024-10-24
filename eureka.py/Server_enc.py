# -*- coding: utf-8 -*-

from CHAM_generalization import *
import socket
import os

mk_low = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
mk_medium = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c]
mk_high = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c, 0xf3f2f1f0, 0xf7f6f5f4, 0xfbfaf9f8, 0xfffefdfc]

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5550

s.bind((host, port))
s.listen(1)
print("Server is listening for incoming connections")
 
cs, addr = s.accept()
print(f"Connection from: {addr}")

# 보안 레벨 수신
recv_data = cs.recv(2500)  # 클라이언트로부터 데이터 수신
security_level = recv_data.decode()  # 바이트 데이터를 문자열로 변환
print(f"Received security level: {security_level}")

if security_level == 'low':
    k = 128
    w = 16
    r = 88
    mk = mk_low

elif security_level == 'medium':
    k = 128
    w = 32
    r = 112
    mk = mk_medium

elif security_level == 'high':
    k = 256
    w = 32
    r = 120
    mk = mk_high

rk = CHAM_key_schedule(mk, k, w)
print(f"round key : {rk}")

while True:
    # receive data from client
    recv_data = cs.recv(50000)
   #print(f"Received data: {recv_data}")

    recv_data_ints = bytes_to_int(recv_data)

    #print(f"Encryped data: {recv_data_ints}")

    # 수신한 펭귄 암호문으로 저장
    recieved_encrypted_penguin = open("recieved_encrypted_penguin.png","wb")
    recieved_encrypted_bytes = int_to_bytes(recv_data_ints)
    recieved_encrypted_penguin.write(recieved_encrypted_bytes)
    recieved_encrypted_penguin.close()

    #펭귄 복호화
    decrypted_data_ints = CHAM_CTR_Encryption(recv_data_ints,rk,len(recv_data_ints), k, w, r)
    #print(f"Origin data: {decrypted_data_ints}")
    
    # 수신한 펭귄 원본으로 저장
    recieved_penguin = open("recieved_penguin.png","wb")
    recieved_bytes = int_to_bytes(decrypted_data_ints)
    
    recieved_penguin.write(recieved_bytes)
    recieved_penguin.close()
    break

cs.close()