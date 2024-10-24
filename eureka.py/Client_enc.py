# -*- coding: utf-8 -*-
from CHAM_generalization import *
import socket

mk_low = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
mk_medium = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c]
mk_high = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c, 0xf3f2f1f0, 0xf7f6f5f4, 0xfbfaf9f8, 0xfffefdfc]

# 보안 레벨 입력
security_level = input("CHAM 암호 레벨을 선택하세요. 'low', 'medium', 'high' : ")

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

# 첫 번째 rk 출력
print(f"round key: {rk}")  # 리스트 전체 출력

# 두 번째 rk 출력
print("\nround key 출력.")
for i in rk:
    print(hex(i), end=',')  # 리스트의 각 요소를 반복 출력
print()

#펭귄 파일 읽기
file_penguin = open("penguin.png","rb")
penguin_data = file_penguin.read()
file_penguin.close()

#펭귄 데이터 hex형으로 변환
penguin_data_hex = penguin_data.hex()

#펭귄 암호화를 위한 list[int] 형 변환
Plaintext = hex_to_int(penguin_data_hex, len(penguin_data_hex))
# print(Plaintext)

# 암호화된 파일 생성할 파일 객체
#file_penguin_encrypt = open("penguin_encrypt.png","wb")

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5550

# Connect to the server (서버에 연결)
s.connect((host, port))
print("Connected to the server.")

# 보안 레벨 전송
s.send(security_level.encode('utf-8'))  # UTF-8로 인코딩하여 전송

# 펭귄 암호화 수행
ct = CHAM_CTR_Encryption(Plaintext,rk,len(Plaintext), k, w, r)

#print(f"Encrypted data: {ct}")

#암호화된 데이터 전송을 위해 byte형 변환
ct_bytes= int_to_bytes(ct)
#print(f"Sent Message: {ct_bytes}")

# Send the encrypted message (암호화된 메시지 서버로 전송)
s.send(ct_bytes)

print("Message sent.")

s.close()