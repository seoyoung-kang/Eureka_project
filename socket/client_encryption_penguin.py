from cham import *
import socket

mk = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
rk = CHAM_key_schedule(mk, 128, 16)

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
port = 5500

# Connect to the server (서버에 연결)
s.connect((host, port))
print("Connected to the server.")

# 펭귄 암호화 수행
ct = CHAM_CTR_Encryption(Plaintext,rk,len(Plaintext))

print(f"Encrypted data: {ct}")

#암호화된 데이터 전송을 위해 byte형 변환
ct_bytes = int_to_bytes(ct)
print(f"Sent Message: {ct_bytes}")

# Send the encrypted message (암호화된 메시지 서버로 전송)
s.send(ct_bytes)
print("Message sent.")

s.close()