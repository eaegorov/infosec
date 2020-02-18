from gcd_modexp import fast_pow, gcd_ext
from RSA import GCD
from tkinter import *
import math
import random


# Алгоритм р-метод Поларда
def polard(n):
    x = random.randint(1, n - 1)
    y = 1
    i = 0
    stage = 2
    while GDC(n, abs(x - y)) == 1:
        if i == stage:
            y = x
            stage *= 2

        x = (x ** 2 + 1) % n
        i += 1

    return GDC(n, abs(x - y))


#16 - 47
rus_big = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
#48 - 79
rus_small = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


# GUI
def clicked_calc():

    n = int(txt1.get())
    e = int(txt2.get())
    SW = int(txt3.get())

    p = polard(n)
    q = n // p
    eiler = (p - 1) * (q - 1)
    _, d, _ = gcd_ext(e, eiler)

    code = fast_pow(SW, d, n)

    a = []
    while code % 100 != 0:
        a.append(code % 100)
        code //= 100

    a.reverse()

    message = ''
    for c in a:
        if c <= 47:
            message += rus_big[c - 16]
        else:
            message += rus_small[c - 48]

    txt4.insert(1, message)


window = Tk()
window.title('Task 6')
window.geometry('620x220')
window.resizable(width=False, height=False)

lbl1 = Label(window, text='N: ')
lbl1.grid(column=0, row=1)
txt1 = Entry(window, width=90)
txt1.grid(column=1, row=1)

lbl2 = Label(window, text='e: ')
lbl2.grid(column=0, row=2)
txt2 = Entry(window, width=90)
txt2.grid(column=1, row=2)

lbl3 = Label(window, text='SW: ')
lbl3.grid(column=0, row=3)
txt3 = Entry(window, width=90)
txt3.grid(column=1, row=3)

btn_calc = Button(window, text='Взломать', command=clicked_calc)
btn_calc.grid(column=1, row=4)

lbl4 = Label(window, text='Результат: ')
lbl4.grid(column=0, row=5)
txt4 = Entry(window, width=90)
txt4.grid(column=1, row=5)

window.mainloop()


# 13
# N - 86892104384358621580698011597
# e - 26398962489114266337226913921
# SW - 62873526787664405062856709109

# 5
# 801354636919526323408669959133
# 5357133285262456827514698587
# 630839280032278632036025925797
