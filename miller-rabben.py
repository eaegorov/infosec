from gcd_modexp import fast_pow
import numpy as np
from tkinter import *
import math
import random


def find_n_minus_1(n):
    s = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        s += 1

    return s, d


# Algorithm
def miller_rabben(n):
    r = int(math.log2(n)) # Number of checkings
    s, d = find_n_minus_1(n)

    svid_prost = []
    for i in range(r):
        a = random.randint(2, n - 2)
        x0 = fast_pow(a, d, n)
        if x0 == 1 or x0 == n - 1:
            print('{} - свидетель простоты. переходим к следующему а.'.format(a))
            svid_prost.append(a)
        else:
            x = [x0]
            for j in range(1, s):
                x.append(fast_pow(x[j - 1], 2, n))
            if n - 1 in x:
                print('{} - свидетель простоты. переходим к следующему а.'.format(a))
                svid_prost.append(a)
            else:
                return 1

    if len(svid_prost) == r:
        return 0
    else:
        return 0



# GUI
def clicked_calc():
    if (txt2.get is not None):
        txt2.delete(0, 'end')

    n = txt1.get()
    ans = miller_rabben(int(n))
    if ans == 0:
        txt2.insert(1, string='Число {} вероятно простое'.format(n))
        lbl6['text'] = 'Статус: Число вероятно простое'
    else:
        txt2.insert(1, string='Число {} составное'.format(n))
        lbl6['text'] = 'Статус: Число составное'

def clicked_bit():
    while True:
        b = random.getrandbits(512)
        last_digit = b % 10
        if last_digit % 2 != 0:
            ans = miller_rabben(b)
            if ans == 0:
                txt4.insert(1, bin(b)[2:])
                txt5.insert(1, str(b))
                lbl6['text'] = 'Число вероятно простое'
                break



window = Tk()
window.title('Task 4')
window.geometry('640x220')
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

window.mainloop()
