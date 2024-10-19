from cham import *
import socket

mk = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
rk = CHAM_key_schedule(mk, 128, 16)

# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5555

# Connect to the server (서버에 연결)
s.connect((host, port))
print("Connected to the server.")

# Input a message (메시지 입력)
message = input("Enter a message: ")

#문자열을 UTF-8 바이트로 인코드
message_bytes = message.encode('utf-8')
print(f"Sent Message: {message_bytes}")

# Send the encrypted message (암호화된 메시지 서버로 전송)
s.send(message_bytes)
print("(메시지 전송 완료) Message sent.")

s.close()