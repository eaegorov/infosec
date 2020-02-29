from tkinter import *
import math
import random
import time
import numpy as np


# Binary converting
def to_bin(x):
    if x == 0:
        return '0'
    res = ''
    while x > 0:
        res = ('0' if x % 2 == 0 else '1') + res
        x //= 2
    return res


# GCD (Euclid)
def GCD(a, b):
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


# Jacobi symbol calculation
def jacobi_symbol(a, b):
    if GCD(a, b) != 1:
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


# Solovay_Strassen Algorithm
def solovay_strassen(n):
    k = 64  # Number of checks
    for i in range(k):
        a = random.randint(2, n - 1)
        if GCD(a, n) > 1:
            return False
        elif fast_pow(a, (n - 1) // 2, n) != jacobi_symbol(a, n) % n:
            return False

    return True


# Factorization
def factor(n):
   ans = []
   d = 2
   while d * d <= n:
       if n % d == 0:
           ans.append(d)
           n //= d
       else:
           d += 1
   if n > 1:
       ans.append(n)
   return ans


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
            if ans:  # Last condition for security improvement (and solovay_strassen((temp - 1) // 2))
                p = temp
                break

    # Finding primitive element of a finite filed GF(p)
    start_time = time.process_time()
    prime_factors = np.unique(factor(p - 1))
    for a in range(2, p):
        check = True
        for q in prime_factors:
            if fast_pow(a, (p - 1) // q, p) == 1:
                check = False
                break

        if check:
            g = a
            break

    delta = time.process_time() - start_time
    print(delta)
    print(g)
    return p, g


def private_keygen(p, g):
    a = random.randint(2, p - 1)
    b = random.randint(2, p - 1)

    x = fast_pow(g, a, p)
    y = fast_pow(g, b, p)

    userA_key = fast_pow(y, a, p)
    userB_key = fast_pow(x, b, p)

    return userA_key if userA_key == userB_key else "error"


if __name__ == '__main__':
    bit_length = 64
    p, g = public_keygen(bit_length)
    k = private_keygen(p, g)
