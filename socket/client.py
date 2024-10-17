import socket

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