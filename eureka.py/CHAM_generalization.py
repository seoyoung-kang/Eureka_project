def format_binary_16bit(number):
 # 16-bit 숫자를 2진수로 변환하고 앞에 0을 포함한 상태로 16자리를 맞춘다
    binary_str = f"{number:016b}"
 # 4비트씩 끊어서 출력
    formatted_binary = ' '.join([binary_str[i:i+4] for i in range(0, 16, 4)])
    return formatted_binary


def ROL(a, n, w):
    return ((a << n) & ((1 << w) - 1)) | (a >> (w - n))

def ROR(a, n, w):
    return ((a >> n) | (a << (w - n))) & ((1 << w) - 1)

mk_low = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
mk_medium = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c]
mk_high = [0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c, 0xf3f2f1f0, 0xf7f6f5f4, 0xfbfaf9f8, 0xfffefdfc]

pt_low = [0x1100, 0x3322, 0x5544, 0x7766]
pt_medium = [0x33221100, 0x77665544, 0xbbaa9988, 0xffeeddcc]
pt_high = [0x33221100, 0x77665544, 0xbbaa9988, 0xffeeddcc]


def Cham_security_level(security_level):
    if security_level == 'low':
        return 128, 16, 88, mk_low, pt_low
    elif security_level == 'medium':
        return 128, 32, 112, mk_medium, pt_medium
    elif security_level == 'high':
        return 256, 32, 120, mk_high, pt_high


def CHAM_key_schedule(mk, k, w):
    RK = [0] * (2 * (k // w))

    for i in range(k // w):
        RK[i] = mk[i] ^ ROL(mk[i], 1, w) ^ ROL(mk[i], 8, w)
        RK[(i + (k // w)) ^ 1] = mk[i] ^ ROL(mk[i], 1, w) ^ ROL(mk[i], 11, w)
    
    return RK

def CHAM_Encryption(pt, rk, k, w, r):
    RK_NUM = k // w
    
    for i in range(0, r, 2):
        
        pt[0] = pt[0] ^ i
        temp = pt[1]
        temp = ROL(temp,1,w) ^ rk[i % (2 * RK_NUM)]

        pt[0] = (pt[0] + temp) & ((1 << w) - 1)
        pt[0] = ROL(pt[0], 8,w)

        temp = pt[0]

        pt[0] = pt[1]
        pt[1] = pt[2]
        pt[2] = pt[3]
        pt[3] = temp   

        # 홀수 라운드
        pt[0] = pt[0] ^ (i + 1)
        temp = pt[1]
        temp = rk[(i + 1) %(2 * RK_NUM)]^ ROL(temp, 8,w)
        pt[0] = (pt[0] + temp) & ((1 << w) - 1)
        pt[0] = ROL(pt[0],1 ,w)
        temp = pt[0]

        pt[0] = pt[1]
        pt[1] = pt[2]
        pt[2] = pt[3]
        pt[3] = temp

    return pt

def CHAM_Decryption(ct, rk, k, w, r):
    num_word = k //w

    for i in range(r-1 ,0 , -2):
        #홀수라운드
        ct[3] = ROR(ct[3], 1,w)
        temp = ct[0]
        temp = ROL(temp, 8,w) ^ rk[(i) % (2 * num_word)]
        ct[3] = (ct[3] - temp) & ((1 << w) - 1)
        ct[3] = ct[3] ^ (i)
        
        temp = ct[3]
        ct[3] = ct[2]
        ct[2] = ct[1]
        ct[1] = ct[0]
        ct[0] = temp

        #짝수 라운드
        ct[3] = ROR(ct[3], 8,w)
        temp = ct[0]
        temp = ROL(temp, 1,w) ^ rk[(i - 1) % (2 * num_word)]
        ct[3] = (ct[3] - temp) & ((1 << w) - 1)
        ct[3] = ct[3] ^ (i - 1)
        temp = ct[3]

        ct[3] = ct[2]
        ct[2] = ct[1]
        ct[1] = ct[0]
        ct[0] = temp

    return ct

def CHAM_CTR_Encryption(pt, rk, pt_len, k, w, r):
    ctr = [0x0000, 0x0000,0x0000,0x0000]    #카운터 값
    ct_temp = [0] * 4                       #함수 출력 저장 배열
    input_temp = [0] * 4                    #함수 입력 저장 배열
    ct = [0] * pt_len                       #암호문 저장 배열
    pt_block = pt_len //4                   #평문의 블록 개수
    pt_remain = pt_len % 4                  #평문의 불록외의 남은 word 수

    for i in range(pt_block):
        input_temp = ctr.copy()
        ct_temp = CHAM_Encryption(input_temp, rk, k, w, r)
        for j in range(4):
            ct[i*4 + j] = ct_temp[j]^pt[4*i + j]
        ctr[0] += 1
    
    input_temp = ctr.copy()
    ct_temp = CHAM_Encryption(input_temp, rk, k, w, r)
    for j in range(pt_remain):
        ct[4*pt_block + j] = ct_temp[j]^pt[4*pt_block+j]

    return ct

def hex_to_int(input, input_len):
    output = []
    for i in range(0,input_len,4):
        temp = int(input[i:i+4],16)
        output.append(temp)
    return output

## int 형식에서 bytes 형식으로 변경하는 함수
def int_to_bytes(input):
    output_byte = b''
    for num in input:
        temp_byte = num.to_bytes(2,byteorder='big')
        output_byte += temp_byte
    return output_byte

#byte_to_int
def bytes_to_int(input_bytes):
    int_list = []
    for i in range(0, len(input_bytes), 2):
        int_value = int.from_bytes(input_bytes[i:i+2], byteorder='big')
        int_list.append(int_value)
    return int_list

if __name__ == "__main__":

    security_level = input("CHAM 암호 레벨을 선택하세요. 'low', 'medium', 'high' : ")

    k, w, r, mk, pt = Cham_security_level(security_level)
    rk = CHAM_key_schedule(mk, k, w)

    print("\nplaintext를 출력합니다.")
    for i in pt:
        print(hex(i), end = ',')
    print()

    ct = CHAM_Encryption(pt, rk, k, w, r)
    print("\nciphertext를 출력합니다.")
    for i in ct:
        print(hex(i), end = ',')
    print()

    pt = CHAM_Decryption(ct, rk, k, w, r)
    print("\n복호화한 plaintext를 출력합니다.")
    for i in pt:
        print(hex(i), end = ',')
    print()

    print("\nCTR 모드 테스트")

    pt2 = [0x1100, 0x3322, 0x5544, 0x7766, 0x9988, 0xbbaa, 0xddcc]
    ct2 = CHAM_CTR_Encryption(pt2, rk, 7, k, w, r)
    dt2 = CHAM_CTR_Encryption(ct2, rk, 7, k, w, r)
    
    print("\nCTR ciphertext를 출력합니다.")
    for i in ct2:
        print(hex(i), end=',')
    print()

    print(f"round key: {rk}")

    print("\n복호화한 CTR plaintext를 출력합니다.")
    for i in dt2:
        print(hex(i), end=',')
    print()


