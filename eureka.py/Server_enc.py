# -*- coding: utf-8 -*-

from CHAM_generalization import *
import socket
import os

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5550

s.bind((host, port))
s.listen(1)
print("Server is listening for incoming connections")
 
cs, addr = s.accept()
print(f"Connection from: {addr}")

while True:

    # 보안 레벨 수신
    recv_data = cs.recv(2500)  # 클라이언트로부터 데이터 수신
    security_level = recv_data.decode()  # 바이트 데이터를 문자열로 변환
    #print(f"Received security level: {security_level}")

    k, w, r, mk = socket_security_level(security_level)

    rk = CHAM_key_schedule(mk, k, w)

    # receive data from client
    recv_data = cs.recv(50000)
    #print(f"Received data: {recv_data}")

    recv_data_ints = bytes_to_int(recv_data)
    #print(f"Encryped data: {recv_data_ints}")

    # 수신한 파일 암호문으로 저장
    recieved_encrypted_file = open("recieved_encrypted_file.png","wb")
    recieved_encrypted_bytes = int_to_bytes(recv_data_ints)
    recieved_encrypted_file.write(recieved_encrypted_bytes)
    recieved_encrypted_file.close()

    #파일 복호화
    decrypted_data_ints = CHAM_CTR_Encryption(recv_data_ints,rk,len(recv_data_ints), k, w, r)
    #print(f"Origin data: {decrypted_data_ints}")
    
    # 수신한 파일 원본으로 저장
    recieved_file = open("recieved_file.png","wb")
    recieved_bytes = int_to_bytes2(decrypted_data_ints)
    #print(recieved_bytes)
    recieved_file.write(recieved_bytes)
    recieved_file.close()
    

    choice_continue = input("이미지를 계속 보내시겠습니까?. 'yes', 'no': ")
    cs.send(choice_continue.encode('utf-8'))
    print()

    if choice_continue == 'no':
        break

    # 보안 레벨 입력
    security_level = input("CHAM 암호 레벨을 선택하세요. 'low', 'medium', 'high' : ")
    k, w, r, mk = socket_security_level(security_level)
    print()

    rk = CHAM_key_schedule(mk, k, w)

    file_name = input("보내고싶은 이미지를 선택하세요.\n'heart.png','penguin.png,'puppy.png','beer.png','black_cat.png,'cat.png' :\n ")
    print()
    
    #선택한 파일 읽기
    file_image = open(file_name,"rb")
    file_data = file_image.read()
    file_image.close()
    print(file_image)

    #펭귄 데이터 hex형으로 변환
    file_data_hex = file_data.hex()


    #펭귄 암호화를 위한 list[int] 형 변환
    Plaintext = hex_to_int(file_data_hex, len(file_data_hex))
    #print(Plaintext)

    # 암호화된 파일 생성할 파일 객체
    #file_file_encrypt = open("file_encrypt.png","wb")

    # 보안 레벨 전송
    cs.send(security_level.encode('utf-8'))  # UTF-8로 인코딩하여 전송

    # 파일 암호화 수행
    ct = CHAM_CTR_Encryption(Plaintext,rk,len(Plaintext), k, w, r)
    #print(f"Encrypted data: {ct}")

    #암호화된 데이터 전송을 위해 byte형 변환
    ct_bytes= int_to_bytes(ct)
    #print(f"Sent Message: {ct_bytes}")

    # Send the encrypted message (암호화된 메시지 서버로 전송)
    cs.send(ct_bytes)
    #print("Message sent.")

    choice_data = cs.recv(2500)  # 클라이언트로부터 데이터 수신
    choice_continue = choice_data.decode()

    if choice_continue == 'no':
        break

cs.close()