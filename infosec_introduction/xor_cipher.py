import numpy as np
from tkinter import *
from tkinter.ttk import Combobox


def to_bin(x):
    if x == 0:
        return '0'
    res = ''
    while x > 0:
        res = ('0' if x % 2 == 0 else '1') + res
        x //= 2
    return res


def xor(a, b):
    x = [int(i) for i in a]
    y = [int(i) for i in b]
    while len(x) != len(y):
        if len(a) < len(b):
            x.insert(0, 0)
        else:
            y.insert(0, 0)

    return np.array(x) ^ np.array(y)


def to_str(bits):
    s = ''
    for c in bits:
        s += str(c)
    return s


def gammirovanie_key(message, key):
    crypted_message = ''
    key_full = ''
    for i in range(len(message)):
        key_full += key[i % len(key)]

    for (x, y) in zip(message, key_full):
        crypted_message += chr(ord(x) ^ ord(y))

    return crypted_message


def gammirovanie_bits(message, gamma=None):
    crypted_message = ''

    if gamma is None:
        gamma = [0] * 64 + [1] * 64
        np.random.shuffle(gamma)

        if len(message) > len(gamma) / 8:
            k = int(len(message) - len(gamma) / 8)
            gamma += gamma[:k * 8]

    k_begin = 0
    k_end = 8
    for i in range(len(message)):
        ch_m = ord(message[i])
        bits = to_str(gamma[k_begin:k_end])
        ch_g = int(bits, 2)
        crypted_message += chr(ch_m ^ ch_g)
        k_begin = k_end
        k_end += 8

    return crypted_message, gamma


# GUI
def clicked_crypto():
    method = combo.get()
    if method == 'Key':
        word = txt1.get()
        key = txt2.get()
        crypt = gammirovanie_key(message=word, key=key)
        txt3.insert(1, string=crypt)

    if method == 'Random bits':
        word = txt1.get()
        #key = txt2.get()
        crypt, gamma = gammirovanie_bits(message=word)
        g = ''
        for i in gamma:
            g += str(i)
        txt2.insert(1, string=g)
        txt3.insert(1, string=crypt)


def clicked_decrypro():
    method = combo.get()
    if method == 'Key':
        code = txt4.get()
        key = txt5.get()
        decrypt = gammirovanie_key(message=code, key=key)
        txt6.insert(1, string=decrypt)

    if method == 'Random bits':
        code = txt4.get()
        key = txt5.get()
        g = []
        for i in key:
            g.append(int(i))
        decrypt, _ = gammirovanie_bits(message=code, gamma=key)
        txt6.insert(1, string=decrypt)


window = Tk()
window.title('Task 2')
window.geometry('420x220')
window.resizable(width=False, height=False)

combo = Combobox(window)
combo['values'] = ('Key', 'Random bits')
combo.current(0)  # установит вариант по умолчанию
combo.grid(column=1, row=0)

# Crypting
lbl1 = Label(window, text='Сообщение: ')
lbl1.grid(column=0, row=1)
txt1 = Entry(window, width=50)
txt1.grid(column=1, row=1)

lbl2 = Label(window, text='Ключ: ')
lbl2.grid(column=0, row=2)
txt2 = Entry(window, width=50)
txt2.grid(column=1, row=2)

lbl3 = Label(window, text='Шифр: ')
lbl3.grid(column=0, row=3)
txt3 = Entry(window, width=50)
txt3.grid(column=1, row=3)

btn_crypt = Button(window, text='Зашифровать', command=clicked_crypto)
btn_crypt.grid(column=1, row=4)


# Decrypring
lbl4 = Label(window, text='Шифр: ')
lbl4.grid(column=0, row=6)
txt4 = Entry(window, width=50)
txt4.grid(column=1, row=6)

lbl5 = Label(window, text='Ключ: ')
lbl5.grid(column=0, row=7)
txt5 = Entry(window, width=50)
txt5.grid(column=1, row=7)

lbl6 = Label(window, text='Сообщение: ')
lbl6.grid(column=0, row=8)
txt6 = Entry(window, width=50)
txt6.grid(column=1, row=8)

btn_decrypt = Button(window, text='Дешифровать', command=clicked_decrypro)
btn_decrypt.grid(column=1, row=9)


window.mainloop()