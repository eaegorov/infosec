from tkinter import *
import random


# GCD (Euclid algorithm)
def gcd(a, b):
    while b:
        t = a % b
        a = b
        b = t

    return a


# Check number is prime or composite
def isPrime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n


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
        r = pollard(n)
        if isPrime(r):
            nums.append(r)
            n //= r

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
    root = Tk()
    root.title("Rho-Pollard factorization")
    root.geometry("720x150")
    root.resizable(width=False, height=False)

    app_client = Application(root)
    app_client.mainloop()
