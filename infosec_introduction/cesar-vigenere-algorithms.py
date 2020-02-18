from tkinter import *
from tkinter.ttk import Radiobutton
from tkinter.ttk import Combobox

# Cesar algorithm
rus = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
eng = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


# Cesar algorithm
def cesar_crypt(message, alphabet, key):
    crypted_message = ''
    for i in range(len(message)):
        if message[i] in digits:
            current = digits.index(message[i])
            symbol = (current + key) % len(digits)
            crypted_message += digits[symbol]
        else:
            current = alphabet.index(message[i])
            symbol = (current + key) % len(alphabet)
            crypted_message += alphabet[symbol]

    return crypted_message


def cesar_decrypt(code, alphabet, key):
    decrypted_message = ''
    for i in range(len(code)):
        if code[i] in digits:
            current = digits.index(code[i])
            symbol = (current - key) % len(digits)
            decrypted_message += digits[symbol]
        else:
            current = alphabet.index(code[i])
            symbol = (current - key) % len(alphabet)
            decrypted_message += alphabet[symbol]

    return decrypted_message


# Vigenere algorithm
def vigenere_crypt(message, alphabet, key):
    crypted_message = ''
    key_full = ''
    for i in range(len(message)):
        key_full += key[i % len(key)]

    for i in range(len(message)):
        if message[i] in digits:
            if key_full[i] in digits:
                current_s = digits.index(message[i])
                current_k = digits.index(key_full[i])
                symbol = (current_s + current_k + 1) % len(digits)
                crypted_message += digits[symbol]
            else:
                current_s = digits.index(message[i])
                current_k = alphabet.index(key_full[i])
                symbol = (current_s + current_k + 1) % len(digits)
                crypted_message += digits[symbol]
        elif message[i] in alphabet:
            if key_full[i] in digits:
                current_s = alphabet.index(message[i])
                current_k = digits.index(key_full[i])
                symbol = (current_s + current_k + 1) % len(alphabet)
                crypted_message += alphabet[symbol]
            else:
                current_s = alphabet.index(message[i])
                current_k = alphabet.index(key_full[i])
                symbol = (current_s + current_k + 1) % len(alphabet)
                crypted_message += alphabet[symbol]

    return crypted_message


def vigenere_decrypt(code, alphabet, key):
    decrypted_message = ''
    key_full = ''
    for i in range(len(code)):
        key_full += key[i % len(key)]

    for i in range(len(code)):
        if code[i] in digits:
            if key_full[i] in digits:
                current_s = digits.index(code[i])
                current_k = digits.index(key_full[i])
                symbol = (current_s - current_k - 1) % len(digits)
                decrypted_message += digits[symbol]
            else:
                current_s = digits.index(code[i])
                current_k = alphabet.index(key_full[i])
                symbol = (current_s - current_k - 1) % len(digits)
                decrypted_message += digits[symbol]
        elif code[i] in alphabet:
            if key_full[i] in digits:
                current_s = alphabet.index(code[i])
                current_k = digits.index(key_full[i])
                symbol = (current_s - current_k - 1) % len(alphabet)
                decrypted_message += alphabet[symbol]
            else:
                current_s = alphabet.index(code[i])
                current_k = alphabet.index(key_full[i])
                symbol = (current_s - current_k - 1) % len(alphabet)
                decrypted_message += alphabet[symbol]

    return decrypted_message


# GUI
def clicked_crypto():
    method = combo.get()
    if method == 'Cesar':
        if lang.get():
            alph = eng
        else:
            alph = rus
        word = txt1.get()
        key = txt2.get()
        crypt = cesar_crypt(message=word, alphabet=alph, key=int(key))
        txt3.insert(1, string=crypt)

    if method == 'Vigenere':
        if lang.get():
            alph = eng
        else:
            alph = rus
        word = txt1.get()
        key = txt2.get()
        crypt = vigenere_crypt(message=word, alphabet=alph, key=key)
        txt3.insert(1, string=crypt)

def clicked_decrypro():
    method = combo.get()
    if method == 'Cesar':
        if lang.get():
            alph = eng
        else:
            alph = rus
        code = txt4.get()
        key = txt5.get()
        decrypt = cesar_decrypt(code=code, alphabet=alph, key=int(key))
        txt6.insert(1, string=decrypt)

    if method == 'Vigenere':
        if lang.get():
            alph = eng
        else:
            alph = rus
        code = txt4.get()
        key = txt5.get()
        crypt = vigenere_decrypt(code=code, alphabet=alph, key=key)
        txt6.insert(1, string=crypt)

window = Tk()
window.title('Task 1')
window.geometry('510x210')

combo = Combobox(window)
combo['values'] = ('Cesar', 'Vigenere')
combo.current(0)  # установите вариант по умолчанию
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

# Radio select
lang = BooleanVar()
lang.set(0)
rad1 = Radiobutton(window, text='rus', value=0, variable=lang)
rad2 = Radiobutton(window, text='eng', value=1, variable=lang)
label_lang = Label(window, text='Выберите алфавит:')
rad1.grid(column=3, row=1)
rad2.grid(column=3, row=2)
label_lang.grid(column=3, row=0)

window.mainloop()