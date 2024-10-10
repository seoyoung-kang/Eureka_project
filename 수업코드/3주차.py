def format_binary_16bit(number):
 # 16-bit 숫자를 2진수로 변환하고 앞에 0을 포함한 상태로 16자리를 맞춘다
    binary_str = f"{number:016b}"
 # 4비트씩 끊어서 출력
    formatted_binary = ' '.join([binary_str[i:i+4] for i in range(0, 16, 4)])
    return formatted_binary

def ROL(a, n):
    return ((a << n) & 0xFFFF) | (a >> (16 - n))

def ROR(a, n):
    return (a >> n) | (a << (16 - n) & 0xFFFF)

# number1 = 0b0000111100001111 # 원하는 숫자 입력
# formatted_output1 = format_binary_16bit(ROL(number1, 4))
# print(formatted_output1)

# number2 = 0b0011110011110000
# formatted_output2 = format_binary_16bit(ROR(number2, 6))
# print(formatted_output2)

def CHAM_key_schedule(mk, k, w):
    
    RK = [0] * (2 * (k // w))

    for i in range(k // w):
        RK[i] = mk[i] ^ ROL(mk[i], 1) ^ ROL(mk[i], 8)
        RK[(i + k // w) ^ 1] = mk[i] ^ ROL(mk[i], 1) ^ ROL(mk[i], 11)
    
    return RK

def CHAM_Encryption(pt, rk, k, w, r):
    RK_NUM = k // w
    
    for i in range(0, r, 2):
        pt[0] = pt[0] ^ i
        temp = pt[1]
        temp = ROL(temp,1) ^ rk[i % (2 * RK_NUM)]
        '''
        pt[0] = (pt[0] + temp) & 0xFFFF를 해야하는데,
        워드길이가 16, 32로 바뀔 때 마다 코드를 다시 짜기 힘드니까
        0xFFFF를 32비트, 64비트에서도 이용할 수 있도록 일반화 해줘야 한다. 
        이 때 w가 워드길이 16이므로 2^4 -> 왼쪽으로 한 칸씩 밀고 ('1'0000으로 만들기 위해) -1을 하면 FFFF가 나온다.
        '''
        pt[0] = (pt[0] + temp) & ((1 << w) - 1)
        pt[0] = ROL(pt[0], 8)
        temp = pt[0]

        pt[0] = pt[1]
        pt[1] = pt[2]
        pt[2] = pt[3]
        pt[3] = temp   

        # 홀수 라운드
        pt[0] = pt[0] ^ (i + 1)
        temp = pt[1]
        temp = rk[(i + 1) %(2 * RK_NUM)]^ ROL(temp, 8)
        pt[0] = (pt[0] + temp) & ((1 << w) - 1)
        pt[0] = ROL(pt[0],1)
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
        ct[3] = ROR(ct[3], 1)
        temp = ct[0]
        temp = ROL(temp, 8) ^ rk[(i) % (2 * num_word)]
        ct[3] = (ct[3] - temp) & ((1 << w) - 1)
        ct[3] = ct[3] ^ (i)
        
        temp = ct[3]
        ct[3] = ct[2]
        ct[2] = ct[1]
        ct[1] = ct[0]
        ct[0] = temp

        #짝수 라운드
        ct[3] = ROR(ct[3], 8)
        temp = ct[0]
        temp = ROL(temp, 1) ^ rk[(i - 1) % (2 * num_word)]
        ct[3] = (ct[3] - temp) & ((1 << w) - 1)
        ct[3] = ct[3] ^ (i - 1)
        temp = ct[3]

        ct[3] = ct[2]
        ct[2] = ct[1]
        ct[1] = ct[0]
        ct[0] = temp

    return ct

def CHAM_CTR_Encryption(pt, rk, pt_len):
    ctr = [0x0000, 0x0000,0x0000,0x0000]#카운터 값
    ct_temp = [0] * 4                   #함수 출력 저장 배열
    input_temp = [0] * 4                #함수 입력 저장 배열
    ct = [0] * pt_len                   #암호문 저장 배열
    pt_block = pt_len //4               #평문의 블록 개수
    pt_remain = pt_len % 4              #평문의 불록외의 남은 word 수

    for i in range(pt_block):
        input_temp = ctr.copy()
        ct_temp = CHAM_Encryption(input_temp, rk, 128, 16, 88)
        for j in range(4):
            ct[i*4 + j] = ct_temp[j]^pt[4*i + j]
        ctr[0] += 1
    
    input_temp = ctr.copy()
    ct_temp = CHAM_Encryption(input_temp, rk, 128, 16, 88)
    for j in range(pt_remain):
        ct[4*pt_block + j] = ct_temp[j]^pt[4*pt_block+j]

    return ct


mk = [0x0100, 0x0302, 0x0504, 0x0706, 0x0908, 0x0b0a, 0x0d0c, 0x0f0e]
rk = CHAM_key_schedule(mk, 128, 16)

pt = [0x1100, 0x3322, 0x5544, 0x7766]
print("\nplaintext를 출력합니다.")
for i in pt:
    print(hex(i), end = ',')
print()

ct = CHAM_Encryption(pt, rk, 128, 16, 88)
print("\nciphertext를 출력합니다.")
for i in ct:
    print(hex(i), end = ',')
print()

pt = CHAM_Decryption(ct, rk, 128, 16, 88)
print("\n복호화한 plaintext를 출력합니다.")
for i in pt:
    print(hex(i), end = ',')
print()

print("\nCTR 모드 테스트")

pt2 = [0x1100, 0x3322, 0x5544, 0x7766, 0x9988, 0xbbaa, 0xddcc]
ct2 = CHAM_CTR_Encryption(pt2, rk, 7)
for i in ct2:
    print(hex(i), end=',')
print()

