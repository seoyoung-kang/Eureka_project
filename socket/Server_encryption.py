# -*- coding: utf-8 -*-

from cham import *
import socket
import os

mk = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
rk = CHAM_key_schedule(mk, 128, 16)

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5580

s.bind((host, port))
s.listen(1)
print("Server is listening for incoming connections")

cs, addr = s.accept()
print(f"Connection from: {addr}")
while True: 

    # receive data from client
    recv_data = cs.recv(25000)
    print(f"Received data: {recv_data}")

    recv_data_ints = bytes_to_int(recv_data)

    print(f"Encryped data: {recv_data_ints}")

    # 수신한 펭귄 암호문으로 저장
    recieved_encrypted_penguin = open("recieved_encrypted_penguin.png","wb")
    recieved_encrypted_bytes = int_to_bytes(recv_data_ints)
    recieved_encrypted_penguin.write(recieved_encrypted_bytes)
    recieved_encrypted_penguin.close()

    #펭귄 복호화
    decrypted_data_ints = CHAM_CTR_Encryption(recv_data_ints,rk,len(recv_data_ints))
    print(f"Origin data: {decrypted_data_ints}")
    
    # 수신한 펭귄 원본으로 저장
    recieved_penguin = open("recieved_penguin.png","wb")
    recieved_bytes = int_to_bytes(decrypted_data_ints)
    recieved_penguin.write(recieved_bytes)
    recieved_penguin.close()
    break

cs.close()