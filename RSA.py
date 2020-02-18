from gdc_modexp import fast_pow, gcd_ext
from tkinter import *
import math
import random


# Для НОД
def GCD(a, b):
    while b:
        t = a % b
        a = b
        b = t

    return a


def find_n_minus_1(n):
    s = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        s += 1

    return s, d


# Algorithm
def miller_rabben(n):
    r = int(math.log2(n))  # Number of checks
    s, d = find_n_minus_1(n)

    svid_prost = []
    for i in range(r):
        a = random.randint(2, n - 2)
        x0 = fast_pow(a, d, n)
        if x0 == 1 or x0 == n - 1:
            svid_prost.append(a)
        else:
            x = [x0]
            for j in range(1, s):
                x.append(fast_pow(x[j - 1], 2, n))
            if n - 1 in x:
                svid_prost.append(a)
            else:
                return 1

    if len(svid_prost) == r:
        return 0
    else:
        return 0


# Key generation
def keygen(bit_length):
    # Поиск p и q
    k = 0
    pq = []
    while True:
        temp = random.getrandbits(bit_length)
        last_digit = temp % 10
        if last_digit % 2 != 0:
            ans = miller_rabben(temp)
            if ans == 0:
                k += 1
                pq.append(temp)
            if k == 2:
                break

    p = pq[0]
    q = pq[1]

    n = p * q
    # Функция Эйлера
    eiler = (p - 1) * (q - 1)

    # Поиск e - открытого ключа RSA
    while True:
        t = random.randint(2, eiler - 1)
        if GCD(t, eiler) == 1:
            e = t
            break

    # Поиск d - секретного ключа
    _, d, _ = gcd_ext(e, eiler)

    return n, p, q, e, d, eiler


# RSA algorithm
def RSA_encodig(message, e, n):
    crypted = []
    for i in range(len(message)):
        c = ord(message[i])
        h = fast_pow(c, e, n)
        crypted.append(h)

    return crypted


def RSA_decoding(code, d, n):
    message = ''
    for crypt in code:
        h = crypt
        c = fast_pow(h, d, n)
        message += str(chr(c))

    return message



# GUI
def clicked_generate():
    bit_lenth = int(txt1.get())
    n, p, q, e, d, eiler = keygen(bit_lenth)  # Ключи
    while d < 0:
        nn, pp, qq, ee, dd, eilere = keygen(bit_lenth)  # Ключи
        n = nn
        p = pp
        q = qq
        e = ee
        d = dd
        eiler = eilere

    txt2.insert(1, string=n)
    txt3.insert(1, string=p)
    txt4.insert(1, string=q)
    txt5.insert(1, string=e)
    txt6.insert(1, string=d)
    txt7.insert(1, string=eiler)


def clicked_encrypt():
    text = txt8.get("1.0", END)
    e = int(txt5.get())
    n = int(txt2.get())
    crypted_message = RSA_encodig(text, e, n)
    message = ''
    for c in crypted_message:
        message += str(c)
        message += ','

    message = message[:-1]

    txt9.insert(END, message)


def clicked_decrypt():
    crypt_message = txt9.get("1.0", END)
    symbols = []
    s = ''
    for c in crypt_message:
        if c != ',':
            s += c
        else:
            symbols.append(s)
            s = ''

    for i in range(len(symbols)):
        symbols[i] = int(symbols[i])

    d = int(txt6.get())
    n = int(txt2.get())
    message = RSA_decoding(symbols, d, n)
    txt11.insert(END, message)


window = Tk()
window.title('Task 5')
window.geometry('800x700')
window.resizable(width=False, height=False)

lbl1 = Label(window, text='Число бит: ')
lbl1.grid(column=0, row=1)
txt1 = Entry(window, width=30)
txt1.grid(column=1, row=1)

btn_generate = Button(window, text='Сгенерировать', command=clicked_generate)
btn_generate.grid(column=1, row=2)

lbl2 = Label(window, text='n: ')
lbl2.grid(column=0, row=3)
txt2 = Entry(window, width=110)
txt2.grid(column=1, row=3)

lbl3 = Label(window, text='p: ')
lbl3.grid(column=0, row=4)
txt3 = Entry(window, width=110)
txt3.grid(column=1, row=4)

lbl4 = Label(window, text='q: ')
lbl4.grid(column=0, row=5)
txt4 = Entry(window, width=110)
txt4.grid(column=1, row=5)

lbl5 = Label(window, text='e: ')
lbl5.grid(column=0, row=6)
txt5 = Entry(window, width=110)
txt5.grid(column=1, row=6)

lbl6 = Label(window, text='d: ')
lbl6.grid(column=0, row=7)
txt6 = Entry(window, width=110)
txt6.grid(column=1, row=7)

lbl7 = Label(window, text='Эйлер: ')
lbl7.grid(column=0, row=8)
txt7 = Entry(window, width=110)
txt7.grid(column=1, row=8)

lbl9 = Label(window, text='\n')
lbl9.grid(column=1, row=9)

lbl8 = Label(window, text='Сообщение: ')
lbl8.grid(column=0, row=10)
txt8 = Text(window, height=5, width=80)
txt8.grid(column=1, row=10)


btn_enc = Button(window, text='Зашифровать', command=clicked_encrypt)
btn_enc.grid(column=1, row=11)

lbl9 = Label(window, text='Шифрограмма: ')
lbl9.grid(column=0, row=12)
txt9 = Text(window, height=10, width=80)
txt9.grid(column=1, row=12)

lbl10 = Label(window, text='\n')
lbl10.grid(column=1, row=13)

btn_dec = Button(window, text='Дешифровать', command=clicked_decrypt)
btn_dec.grid(column=1, row=14)

lbl11 = Label(window, text='Расшифровка: ')
lbl11.grid(column=0, row=15)
txt11 = Text(window, height=5, width=80)
txt11.grid(column=1, row=15)

window.mainloop()
