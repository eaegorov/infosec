from tkinter import *
import math
import random


# GCD (Euclid)
def GCD(a, b):
    while b:
        t = a % b
        a = b
        b = t
    return a


# Fast modular exponentiation
def fast_pow(a, b, n):
    b = bin(b)[2:]  # To binary representation converting
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
    k = 128  # Number of checks
    for i in range(k):
        a = random.randint(2, n - 1)
        if GCD(a, n) > 1:
            return False
        elif fast_pow(a, (n - 1) // 2, n) != jacobi_symbol(a, n) % n:
            return False

    return True


# GUI methods
def clicked_calc():
    if txt2.get is not None:
        txt2.delete(0, 'end')

    n = txt1.get()
    ans = solovay_strassen(int(n))
    if ans:
        txt2.insert(1, string='Число вероятно простое'.format(n))
        lbl6['text'] = 'Статус: Число вероятно простое'
    else:
        txt2.insert(1, string='Число составное'.format(n))
        lbl6['text'] = 'Статус: Число составное'


def clicked_bit():
    while True:
        b = random.getrandbits(512)
        last_digit = b % 10
        if last_digit % 2 != 0:
            ans = solovay_strassen(b)
            if ans:
                txt4.insert(1, bin(b)[2:])
                txt5.insert(1, str(b))
                lbl6['text'] = 'Сгенерированное 512-битное вероятно простое число'
                break


def clicked_clear():
    txt1.delete(0, 'end')
    txt2.delete(0, 'end')
    txt4.delete(0, 'end')
    txt5.delete(0, 'end')
    lbl6['text'] = ''


# GUI
window = Tk()
window.title('Solovay-Strassen Test')
window.geometry('650x235')
window.resizable(width=False, height=False)

lbl1 = Label(window, text='Введите n: ')
lbl1.grid(column=0, row=1)
txt1 = Entry(window, width=80)
txt1.grid(column=1, row=1)

lbl2 = Label(window, text='Вывод: ')
lbl2.grid(column=0, row=3)
txt2 = Entry(window, width=80)
txt2.grid(column=1, row=3)

btn_calc = Button(window, text='Проверить', command=clicked_calc)
btn_calc.grid(column=1, row=2)

lbl3 = Label(window, text='\nДемонстрация в битах')
lbl3.grid(column=1, row=4)

lbl4 = Label(window, text='Вероятно простое число: ')
lbl4.grid(column=0, row=5)
txt4 = Entry(window, width=80)
txt4.grid(column=1, row=5)

lbl5 = Label(window, text='Десятичное: ')
lbl5.grid(column=0, row=6)
txt5 = Entry(window, width=80)
txt5.grid(column=1, row=6)

btn_bit = Button(window, text='Проверить биты', command=clicked_bit)
btn_bit.grid(column=1, row=7)

lbl6 = Label(window, text='Статус:')
lbl6.grid(column=1, row=8)

btn_bit = Button(window, text='Очистить', command=clicked_clear)
btn_bit.grid(column=1, row=9)

window.mainloop()
