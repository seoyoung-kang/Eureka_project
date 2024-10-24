while True:
#     # receive data from client
#     recv_data = cs.recv(25000)
#     print(f"Received data: {recv_data}")

#     recv_data_ints = bytes_to_int(recv_data)

#     print(f"Encryped data: {recv_data_ints}")

#     # 복호화 수행 (암호문 복호화)
#     decrypted_data_ints = CHAM_CTR_Encryption(recv_data_ints,rk,len(recv_data_ints),k, w, r)
#     print(f"Origin data: {decrypted_data_ints}")

#     # 복호화된 정수 리스트를 바이트로 변환
#     decrypted_bytes = int_to_bytes(decrypted_data_ints)

#     #바이트를 문자열로
#     recv_message_bytes = decrypted_bytes.decode('utf-8')
    
#     print(f"Decrypted message: {recv_message_bytes}")

#     break

# cs.close()