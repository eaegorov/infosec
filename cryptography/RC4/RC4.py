from tkinter import *
import random
import numpy as np
import math


# To binary representation converting
def to_bin(x):
    if x == 0:
        return '0'
    res = ''
    while x > 0:
        res = ('0' if x % 2 == 0 else '1') + res
        x //= 2
    return res


# GCD (Euclid algorithm)
def gcd(a, b):
    while b:
        t = a % b
        a = b
        b = t
    return a


# Fast modular exponentiation
def fast_pow(a, b, n):
    b = to_bin(b)
    a_numbers = [a]
    for i in range(1, len(b)):
        if b[i] == '0':
            a_numbers.append((a_numbers[i - 1] ** 2) % n)
        else:
            a_numbers.append(((a_numbers[i - 1] ** 2) * a_numbers[0]) % n)

    return a_numbers[-1]

# n-1 representation for Millen-Rabben params
def find_n_minus_1(n):
    s = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        s += 1

    return s, d


# Miller-Rabben Algorithm for Pollard factorization
def miller_rabben(n):
    if n == 2 or n == 3:
        return True
    r = int(math.log2(n))  # Number of checks
    s, d = find_n_minus_1(n)

    svid_prost = 0
    for i in range(r):
        a = random.randint(2, n - 2)
        x0 = fast_pow(a, d, n)
        if x0 == 1 or x0 == n - 1:
            svid_prost += 1
        else:
            x = [x0]
            for j in range(1, s):
                x.append(fast_pow(x[j - 1], 2, n))
            if n - 1 in x:
                svid_prost += 1
            else:
                return False

    if svid_prost == r:
        return True
    else:
        return True


# Rho-Pollard Algorithm for factorization
def pollard(n):
    x = random.randint(1, n - 1)
    y = 1
    i = 0
    stage = 2
    while gcd(n, abs(x - y)) == 1:
        if i == stage:
            y = x
            stage *= 2

        x = (x ** 2 + 1) % n
        i += 1

    return gcd(n, abs(x - y))


def pollard_factor(n):
    nums = []

    while n > 1 and not miller_rabben(n):
        d = pollard(n)
        if miller_rabben(d) and n != d:
            nums.append(d)
            n //= d

    nums.append(n)
    nums.sort()
    return nums


# Jacobi symbol calculation
def jacobi_symbol(a, b):
    if gcd(a, b) != 1:
        return 0
    else:
        r = 1
        if a < 0:
            a = -a
            if b % 4 == 3:
                r = -r

        while a != 0:
            t = 0
            while a % 2 == 0:
                t += 1
                a //= 2
            if t % 2 == 1:
                if b % 8 == 3 or b % 8 == 5:
                    r = -r

            if a % 4 == b % 4 == 3:
                r = -r
            c = a
            a = b % c
            b = c

        return r


# Solovay-Strassen Algorithm
def solovay_strassen(n):
    k = 128  # Number of checks
    for i in range(k):
        a = random.randint(2, n - 1)
        if gcd(a, n) > 1:
            return False
        elif fast_pow(a, (n - 1) // 2, n) != jacobi_symbol(a, n) % n:
            return False

    return True


# Public key and primitive element generation
def public_keygen(bit_length):
    p = None
    g = None

    # Generate public key p
    while True:
        temp = random.getrandbits(bit_length)
        last_digit = temp % 10
        if last_digit % 2 != 0:
            ans = solovay_strassen(temp)
            if ans:
                p = temp
                break

    # Finding primitive element of a finite filed GF(p)
    prime_factors = pollard_factor(p - 1)
    for a in range(2, p):
        check = True
        for q in prime_factors:
            if fast_pow(a, (p - 1) // q, p) == 1:
                check = False
                break

        if check:
            g = a
            break

    return p, g


# Mutual secret key generation
def private_keygen(p, g):
    k = None
    a = random.randint(2, p - 1)
    b = random.randint(2, p - 1)

    # Exchange params A and B
    x = fast_pow(g, a, p)
    y = fast_pow(g, b, p)

    # Private key generation
    userA_key = fast_pow(y, a, p)
    userB_key = fast_pow(x, b, p)

    # Compare keys from A and B
    k = userA_key if userA_key == userB_key else -1
    return k


# Key-Scheduling Algorithm
def KSA(bits_number, key):
    key = to_bin(key)
    if bits_number - len(key) > 0:
        key = '0' * (bits_number - len(key)) + key

    key_length = len(key) // 8
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + int(key[i % key_length])) % 256
        S[i], S[j] = S[j], S[i]

    return S


# Pseudo-Random Generation Algorithm
def PRGA(S, n):
    i = 0
    j = 0

    keystream = []
    while n > 0:
        n -= 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)

    return keystream


# RC4 encoding
def encode(text, bits_number, key):
    S = KSA(bits_number, key)
    keystream = np.array(PRGA(S, len(text)))

    message = np.array([ord(i) for i in text])
    cipher = message ^ keystream
    cipher_code = [chr(c) for c in cipher]

    return cipher_code


# RC4 decoding
def decode(cipher, bits_number, key):
    decoded_message = encode(cipher, bits_number, key)

    return decoded_message


# GUI
class Application(Frame):
    def __init__(self, main):
        super().__init__()
        self.bits_number = 64
        self.p = None
        self.g = None
        self.key = None
        self.cipher = None
        self.main = main
        self.set_widgets_client()

    def set_widgets_client(self):
        # Create widget
        self.bits_number_label = Label(self.main, text='Число бит ключа - 64')
        self.key_label = Label(self.main, text='Ключ: ')
        self.key_field = Entry(self.main, width=100)
        self.text_label = Label(self.main, text='Текст: ')
        self.text_field = Entry(self.main, width=100)
        self.btn_encode = Button(self.main, text='Зашифровать', command=self.clicked_encode)
        self.encoded_text_label = Label(self.main, text='Шифр: ')
        self.encoded_text_field = Entry(self.main, width=100)
        self.btn_decode = Button(self.main, text='Расшифровать', command=self.clicked_decode)
        self.decoded_text_label = Label(self.main, text='Исходный текст: ')
        self.decoded_text_field = Entry(self.main, width=100)
        self.clear_btn = Button(self.main, text='Очистить', command=self.clicked_clear)

        self.bits_number_label.grid(column=1, row=1)
        self.text_label.grid(column=0, row=2)
        self.text_field.grid(column=1, row=2)
        self.key_label.grid(column=0, row=3)
        self.key_field.grid(column=1, row=3)
        self.btn_encode.grid(column=1, row=4)
        self.encoded_text_label.grid(column=0, row=5)
        self.encoded_text_field.grid(column=1, row=5)
        self.btn_decode.grid(column=1, row=6)
        self.decoded_text_label.grid(column=0, row=7)
        self.decoded_text_field.grid(column=1, row=7)
        self.clear_btn.grid(column=1, row=8)

    def clicked_encode(self):
        self.p, self.g = public_keygen(self.bits_number)
        self.key = private_keygen(self.p, self.g)
        self.key_field.insert(1, to_bin(self.key))

        self.message = self.text_field.get()
        self.cipher = encode(self.message, self.bits_number, self.key)
        self.encoded_text_field.insert(1, self.cipher)

    def clicked_decode(self):
        # cipher = [i for i in str(self.encoded_text_field.get()).split()]
        decoded_message = decode(self.cipher, self.bits_number, self.key)

        src = ''
        for symbol in decoded_message:
            src += symbol

        self.decoded_text_field.insert(1, src)

    def clicked_clear(self):
        self.key_field.delete(0, 'end')
        self.text_field.delete(0, 'end')
        self.encoded_text_field.delete(0, 'end')
        self.decoded_text_field.delete(0, 'end')


if __name__ == '__main__':
    # GUI building
    root = Tk()
    root.title("RC4")
    root.geometry("750x250")
    root.resizable(width=False, height=False)

    app_client = Application(root)
    app_client.mainloop()
