def ROL_16(a, n):
    # 0xFFFF와의 AND 연산을 통해 16-bit로 범위 고정
    return ((a << n) & 0xFFFF) | (a >> (16 - n))

def ROR_16(a, n):
    # 0xFFFF와의 AND 연산을 통해 16-bit로 범위 고정
    return (a >> n) | ((a << (16 - n)) & 0xFFFF)

def format_binary_16bit(number):
    # 16-bit 숫자를 2진수로 변환하고 앞에 0을 포함한 상태로 16자리를 맞춘다
    binary_str = f"{number:016b}"
    # 4비트씩 끊어서 출력
    formatted_binary = ' '.join([binary_str[i:i+4] for i in range(0, 16, 4)])
    return formatted_binary

# 예시 사용
# number = 45  # 원하는 숫자 입력
# formatted_output = format_binary_16bit(number)
# print(formatted_output)

def CHAM_key_schedule(mk, k, w):
    # 키의 워드 개수
    num_word = k // w
    # rk 초기화
    rk = [0] * (2 * num_word)
    
    for i in range(num_word):
        rk[i] = mk[i] ^ ROL_16(mk[i], 1) ^ ROL_16(mk[i], 8)
        rk[(i + num_word) ^ 1] = mk[i] ^ ROL_16(mk[i], 1) ^ ROL_16(mk[i], 11)
    
    # 라운드 키 반환
    return rk

# pt는 w-bit 4개로 이루어짐
def CHAM_Encryption(pt, rk):

    for i in range(0, 88, 2):
        # i is even (짝수 라운드)
        pt[0] = pt[0] ^ i
        temp = pt[1]
        temp = ROL_16(temp, 1)
        temp = temp ^ rk[i % 16]
        pt[0] = (pt[0] + temp) & 0xFFFF 
        pt[0] = ROL_16(pt[0], 8)
        temp = pt[0]

        pt[0] = pt[1]
        pt[1] = pt[2]
        pt[2] = pt[3]
        pt[3] = temp

        # i is odd (홀수 라운드)
        pt[0] = pt[0] ^ (i + 1)
        temp = pt[1]
        temp = ROL_16(temp, 8)
        temp = temp ^ rk[(i + 1) % 16]
        pt[0] = pt[0] + temp & 0xFFFF 
        pt[0] = ROL_16(pt[0], 1)
        temp = pt[0]

        pt[0] = pt[1]
        pt[1] = pt[2]
        pt[2] = pt[3]
        pt[3] = temp

    return pt

# ct는 w-bit 4개로 이루어짐
def CHAM_Decryption(ct, rk):

    for i in range(87, 0, -2):
        # i is odd (홀수 라운드)
        ct[3] = ROR_16(ct[3], 1)
        temp = ct[0]
        temp = ROL_16(temp, 8)
        temp = temp ^ rk[i % 16]
        ct[3] = (ct[3] - temp) & 0xFFFF
        ct[3] = ct[3] ^ i
        temp = ct[3]
        
        ct[3] = ct[2]
        ct[2] = ct[1]
        ct[1] = ct[0]
        ct[0] = temp
        
        # i is even (짝수 라운드)
        ct[3] = ROR_16(ct[3], 8)
        temp = ct[0]
        temp = ROL_16(temp, 1)
        temp = temp ^ rk[(i - 1) % 16]
        ct[3] = (ct[3] - temp) & 0xFFFF
        ct[3] = ct[3] ^ (i - 1)
        temp = ct[3]
        
        ct[3] = ct[2]
        ct[2] = ct[1]
        ct[1] = ct[0]
        ct[0] = temp

    return ct            



'''
0x0301, 0x0705, 0x0B09, 0x0F0D,
0x1311, 0x1715, 0x1B19, 0x1F1D,
0x151E, 0x0308, 0x3932, 0x2F24,
0x4D46, 0x5B50, 0x616A, 0x777C
'''

# CHAM CTR 모드==================================
def CHAM_CTR_Encryption(pt, rk, pt_len):
    
    ctr = [0x0000,0x0000,0x0000,0x0000] # 카운터 값
    ct_temp = [0] * 4                   # 함수 출력 저장 배열
    input_temp = [0] * 4                # 함수 입력 저장 배열
    ct = [0] * pt_len                   # 암호문 저장 배열
    pt_block = pt_len // 4              # 평문의 블록 개수
    pt_remain = pt_len % 4              # 평문의 블록외의 남은 word 수
    
    for i in range(pt_block):
        input_temp = ctr.copy()
        ct_temp = CHAM_Encryption(input_temp,rk)
        for j in range(4):
            ct[4*i+j] = ct_temp[j]^pt[4*i+j]
        ctr[0] += 1
        
    input_temp = ctr.copy()
    ct_temp = CHAM_Encryption(input_temp,rk)
    for j in range(pt_remain):
        ct[4*pt_block+j] = ct_temp[j]^pt[4*pt_block+j]
        
    return ct



# 파일 암호화======================================================================

# hex 문자열에서 int 형식으로 변경
def hex_to_int(input, input_len):
    output = []
    for i in range(0,input_len,4):
        temp = int(input[i:i+4],16)
        output.append(temp)
    return output

# int 형식에서 bytes 형식으로 변경하는 함수
def int_to_bytes(input):
    output_byte = b''
    for num in input:
        temp_byte = num.to_bytes(2,byteorder='big')
        output_byte += temp_byte
    return output_byte

#byte_to_int
def bytes_to_int(input_bytes):
    int_list = []
    # 2바이트씩 읽어서 int로 변환
    for i in range(0, len(input_bytes), 2):
        int_value = int.from_bytes(input_bytes[i:i+2], byteorder='big')
        int_list.append(int_value)
    return int_list

#byte_to_int
def bytes_to_int(input_bytes):
    int_list = []
    for i in range(0, len(input_bytes), 2):
        int_value = int.from_bytes(input_bytes[i:i+2], byteorder='big')
        int_list.append(int_value)
    return int_list

if __name__ == "__main__":
    mk = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
    pt = [0x1100, 0x3322, 0x5544, 0x7766]

    rk = CHAM_key_schedule(mk, 128, 16)

    # for i in rk:
    #     print(hex(i))
    # print()

    # ct = CHAM_Encryption(pt, rk)
    # for i in ct:
    #     print(hex(i))
    # print()

    # pt = CHAM_Decryption(ct, rk)
    # for i in pt:
    #     print(hex(i))
    # print()

    # print("CTR 모드 테스트")
    pt2 = [0x1100, 0x3322, 0x5544, 0x7766, 0x9988, 0xbbaa, 0xddcc, 0xffee, 0x1100,0x3322,0x5544]
    ct2 = CHAM_CTR_Encryption(pt2,rk,11)
    # 실습 4
    file = open("hello.txt","r")
    temp = file.read()
    # print(temp)
    file.close()

    file_write = open("hi.txt","w")
    temp = "hello python!"
    file_write.write(temp)
    file_write.close()

    # 이미지 파일 읽기
    file_penguin = open("penguin.png","rb")
    penguin_data = file_penguin.read()
    
    file_penguin.close()

    penguin_data_hex = penguin_data.hex()   

    Plaintext = hex_to_int(penguin_data_hex, len(penguin_data_hex))
    # print(Plaintext)

    # 실제 암호화 수행
    ct = CHAM_CTR_Encryption(Plaintext,rk,len(Plaintext))
    #print(ct)

    # 암호화된 파일 생성할 파일 객체
    file_penguin_encrypt = open("penguin_encrypt.png","wb")

    ct_bytes = int_to_bytes(ct)             # 암호문 bytes 형식으로 변경
    file_penguin_encrypt.write(ct_bytes)    # 암호화된 파일 생성
    file_penguin_encrypt.close()


    # 암호화된 파일 읽어올 파일 객체
    file_penguin_encrypt = open("penguin_encrypt.png","rb")
    penguin_encrypt_data = file_penguin_encrypt.read()
    penguin_encrypt_data_hex = penguin_encrypt_data.hex()
    Ciphertext = hex_to_int(penguin_encrypt_data_hex,len(penguin_encrypt_data_hex))
    file_penguin_encrypt.close()

    Recovered = CHAM_CTR_Encryption(Ciphertext,rk,len(Ciphertext))

    #복호화된 파일 생성
    file_penguin_recovered = open("penguin_recovered.png","wb")
    recovered_bytes = int_to_bytes(Recovered)
    file_penguin_recovered.write(recovered_bytes)
    file_penguin_recovered.close()
    

    
    