from tkinter import *
import random
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


# Miller-Rabben Algorithm
def miller_rabben(n):
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


# Rho-Pollard Algorithm
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

    while n > 1:
        d = pollard(n)
        if d == 2 or d == 3:
            nums.append(d)
            n //= d
        elif miller_rabben(d):  # check d is prime or composite
            nums.append(d)
            n //= d

    nums.sort()
    return nums


# GUI
class Application(Frame):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.set_widgets_client()

    def set_widgets_client(self):
        # Create widget
        self.number_label = Label(self.main, text='Введите число: ')
        self.number_field = Entry(self.main, width=100)
        self.btn_factor = Button(self.main, text='Разложить', command=self.clicked_factor)
        self.factorization_label = Label(self.main, text='Факторизация: ')
        self.factorization_field = Entry(self.main, width=100)
        self.clear_btn = Button(self.main, text='Очистить', command=self.clicked_clear)

        self.number_label.grid(column=0, row=1)
        self.number_field.grid(column=1, row=1)
        self.btn_factor.grid(column=1, row=2)
        self.factorization_label.grid(column=0, row=3)
        self.factorization_field.grid(column=1, row=3)
        self.clear_btn.grid(column=1, row=4)

    def clicked_factor(self):
        n = int(self.number_field.get())
        factorization = pollard_factor(n)
        self.factorization_field.insert(1, str(factorization))

    def clicked_clear(self):
        self.number_field.delete(0, 'end')
        self.factorization_field.delete(0, 'end')


if __name__ == '__main__':
    # GUI building
    print(random.getrandbits(64))
    root = Tk()
    root.title("Rho-Pollard factorization")
    root.geometry("720x150")
    root.resizable(width=False, height=False)

    app_client = Application(root)
    app_client.mainloop()
