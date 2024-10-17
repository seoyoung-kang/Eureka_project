import socket
# Create a socket object (소켓 생성)
s = socket.socket()
host = "127.0.0.1"
port = 5555

s.bind((host, port))
s.listen(1)
print("Server is listening for incoming connections")

cs, addr = s.accept()
print(f"Connection from: {addr}")

while True:
    # receive data from client
    recv_data = cs.recv(4096)
    
    print(f"Received data: {recv_data}")

    #바이트를 문자열로
    recv_message_bytes = recv_data.decode('utf-8')

    print(f"Decrypted message: {recv_message_bytes}")
    
    break

cs.close()