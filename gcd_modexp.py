import numpy as np
from tkinter import *


def to_bin(x):
    if x == 0:
        return '0'
    res = ''
    while x > 0:
        res = ('0' if x % 2 == 0 else '1') + res
        x //= 2
    return res


def fast_pow(a, b, n):
    b = to_bin(b)
    a_numbers = [a]
    for i in range(1, len(b)):
        if b[i] == '0':
            a_numbers.append((a_numbers[i - 1] ** 2) % n)
        else:
            a_numbers.append(((a_numbers[i - 1] ** 2) * a_numbers[0]) % n)

    return a_numbers[-1]


def gcd_ext(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcd_ext(b, a % b)
        return d, y, x - y * (a // b)


# GUI
def click_option():
    if btn_option['text'] == 'GCD':
        lbl3.grid_remove()
        txt3.grid_remove()
        btn_option['text'] = 'Mod exp'
        lbl6.grid()
        txt6.grid()
        lbl7.grid()
        txt7.grid()
        lbl5['text'] = 'Current: GCD'
        txt1.delete(0, 'end')
        txt2.delete(0, 'end')
        txt4.delete(0, 'end')
        txt6.delete(0, 'end')
        txt7.delete(0, 'end')
    else:
        lbl3.grid()
        txt3.grid()
        btn_option['text'] = 'GCD'
        lbl6.grid_remove()
        txt6.grid_remove()
        lbl7.grid_remove()
        txt7.grid_remove()
        lbl5['text'] = 'Current: Mod exp'
        txt1.delete(0, 'end')
        txt2.delete(0, 'end')
        txt3.delete(0, 'end')
        txt4.delete(0, 'end')


def clicked_calc():
    if btn_option['text'] == 'Mod exp':
        a = txt1.get()
        b = txt2.get()
        d, x, y = gcd_ext(int(a), int(b))
        txt4.insert(1, string=d)
        txt6.insert(1, string=x)
        txt7.insert(1, string=y)
    else:
        a = txt1.get()
        b = txt2.get()
        n = txt3.get()
        res = fast_pow(int(a), int(b), int(n))
        txt4.insert(1, string=res)


window = Tk()
window.title('Task 3')
window.geometry('420x240')
window.resizable(width=False, height=False)

btn_option = Button(window, bg='yellow', width=12, height=2, text='GCD', command=click_option)
btn_option.grid(column=1, row=0)

lbl1 = Label(window, text='a: ')
lbl1.grid(column=0, row=1)
txt1 = Entry(window, width=50)
txt1.grid(column=1, row=1)

lbl2 = Label(window, text='b: ')
lbl2.grid(column=0, row=2)
txt2 = Entry(window, width=50)
txt2.grid(column=1, row=2)

lbl3 = Label(window, text='n: ')
lbl3.grid(column=0, row=3)
txt3 = Entry(window, width=50)
txt3.grid(column=1, row=3)

btn_calc = Button(window, width=12, height=1, text='Вычислить', command=clicked_calc)
btn_calc.grid(column=1, row=4)

lbl4 = Label(window, text='Результат: ')
lbl4.grid(column=0, row=5)
txt4 = Entry(window, width=50)
txt4.grid(column=1, row=5)

lbl6 = Label(window, text='x: ')
lbl6.grid(column=0, row=6)
txt6 = Entry(window, width=50)
txt6.grid(column=1, row=6)

lbl7 = Label(window, text='y: ')
lbl7.grid(column=0, row=7)
txt7 = Entry(window, width=50)
txt7.grid(column=1, row=7)


lbl5 = Label(window, text='Current: Mod exp', font='bold')
lbl5.grid(column=1, row=8)

window.mainloop()
