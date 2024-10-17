from CHAM import *

# file = open("hello.txt","r")
# temp = file.read()
# print(temp)
# file.close()

# file_write = open("hi.txt", "w")
# temp = "Hello python"
# file_write.write(temp)
# file_write.close()

file_penguin = open("penguin.png","rb")
penguin_data = file_penguin.read()

penguin_data_hex = penguin_data.hex()
print(penguin_data_hex)
print(type(penguin_data_hex))

def hex_to_int(input, input_len):
    output = []
    for i in range(0, input_len,4):
        temp = int(input[i:i+4],16)
        output.append(temp)
    return output

plaintext = hex_to_int(penguin_data_hex, len(penguin_data_hex))

ct = CHAM_CTR_Encryption(plaintext, rk, len(plaintext))

file_penguin_encrypt = open("penguin_encrypt.png","wb")

def int_to_bytes(input):
    output_byte = b''
    for num in input:
        temp_byte = num.to_bytes(2,byteorder='big')
        output_byte += temp_byte
        return output_byte
    
ct_bytes = int_to_bytes(ct)
file_penguin_encrypt.write(ct_bytes)

file_penguin_encrypt = open("penguin_encrypt.png","rb")
penguin_encrypt_data = file_penguin_encrypt.read()
penguin_encrypt_data_hex = penguin_encrypt_data.hex()
Ciphertext = hex_to_int(penguin_encrypt_data_hex,len(penguin_encrypt_data_hex))
Recovered = CHAM_CTR_Encryption(Ciphertext,rk,len(Ciphertext))

file_penguin_recovered = open("penguin_recovered.png","wb")
recovered_bytes = int_to_bytes(Recovered)
file_penguin_recovered.write(recovered_bytes)
file_penguin_recovered.close()
