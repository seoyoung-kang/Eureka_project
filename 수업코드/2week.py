letters = '0123456789ABCDEF'
def convert(num, base=2):
    l = []
    while num != 0:
        l.append(letters[num % base])
        num = num//base
    s = ''.join(map(str,l[::-1]))
    return s

if __name__ == '__main__':
    n = int(input('Enter a number: '))
    print(convert(n))
    print(convert(n, 16))