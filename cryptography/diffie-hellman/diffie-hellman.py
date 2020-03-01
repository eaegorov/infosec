from tkinter import *
import random
import time
import numpy as np


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


# Solovay-Strassen Algorithm
def solovay_strassen(n):
    k = 128  # Number of checks
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
            if ans:
                p = temp
                break

    # Finding primitive element of a finite filed GF(p)
    # start_time = time.process_time()
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

    #delta = time.process_time() - start_time
    return p, g


# Mutual secret key generation
def private_keygen(p, g):
    k = None
    a = random.randint(2, p - 1)
    b = random.randint(2, p - 1)

    # Exchange params A and B
    x = fast_pow(g, a, p)
    y = fast_pow(g, b, p)

    # Private key generation
    userA_key = fast_pow(y, a, p)
    userB_key = fast_pow(x, b, p)

    # Compare keys from A and B
    k = userA_key if userA_key == userB_key else -1
    return a, b, x, y, k


# GUI
class ApplicationClient(Frame):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.set_widgets_client()

    def set_widgets_client(self):
        # Create widget
        self.bits_number_label = Label(self.main, text='Число бит: ')
        self.bits_number_field = Entry(self.main, width=30)
        self.btn_generate = Button(self.main, text='Сгенерировать', command=self.clicked_generate)
        self.prime_p_label = Label(self.main, text='p: ')
        self.prime_p_field = Entry(self.main, width=100)
        self.generator_g_label = Label(self.main, text='g: ')
        self.generator_g_field = Entry(self.main, width=100)
        self.clear_btn = Button(self.main, text='Очистить', command=self.clicked_clear)

        self.bits_number_label.grid(column=0, row=1)
        self.bits_number_field.grid(column=1, row=1)
        self.btn_generate.grid(column=1, row=2)
        self.prime_p_label.grid(column=0, row=3)
        self.prime_p_field.grid(column=1, row=3)
        self.generator_g_label.grid(column=0, row=4)
        self.generator_g_field.grid(column=1, row=4)
        self.clear_btn.grid(column=1, row=5)

    def clicked_generate(self):
        self.bits_number = int(self.bits_number_field.get())
        p, g = public_keygen(self.bits_number)
        self.prime_p_field.insert(1, p)
        self.generator_g_field.insert(1, g)
        ApplicationServer(root_server, p, g)  # Send public params to server side

    def clicked_clear(self):
        self.bits_number_field.delete(0, 'end')
        self.prime_p_field.delete(0, 'end')
        self.generator_g_field.delete(0, 'end')


class ApplicationServer(Frame):
    def __init__(self, main, p, g):
        super().__init__()
        self.main = main
        self.public_key = p
        self.generator = g
        self.set_widgets_server()

    def set_widgets_server(self):
        # Create widget
        self.random_a_label = Label(self.main, text='Число от участника A: ')
        self.random_a_field = Entry(self.main, width=85)
        self.random_b_label = Label(self.main, text='Число от участника B: ')
        self.random_b_field = Entry(self.main, width=85)
        self.x_label = Label(self.main, text='x: ')
        self.x_field = Entry(self.main, width=85)
        self.y_label = Label(self.main, text='y: ')
        self.y_field = Entry(self.main, width=85)
        self.private_key_label = Label(self.main, text='Общий секретный ключ: ')
        self.private_key_field = Entry(self.main, width=85)
        self.btn_private = Button(self.main, text='Вычислить', command=self.generate_private)
        self.status = Label(self.main, text='')

        self.random_a_label.grid(column=0, row=1)
        self.random_a_field.grid(column=1, row=1)
        self.random_b_label.grid(column=0, row=2)
        self.random_b_field.grid(column=1, row=2)
        self.x_label.grid(column=0, row=3)
        self.x_field.grid(column=1, row=3)
        self.y_label.grid(column=0, row=4)
        self.y_field.grid(column=1, row=4)
        self.private_key_label.grid(column=0, row=5)
        self.private_key_field.grid(column=1, row=5)
        self.btn_private.grid(column=1, row=6)
        self.status.grid(column=1, row=7)

    def generate_private(self):
        # Clearing fields
        self.random_a_field.delete(0, 'end')
        self.random_b_field.delete(0, 'end')
        self.x_field.delete(0, 'end')
        self.y_field.delete(0, 'end')
        self.private_key_field.delete(0, 'end')
        self.status['text'] = ''

        # Calculating private key
        self.status['text'] = 'Статус: Идёт обмен параметрами x и y... '
        a, b, x, y, k = private_keygen(self.public_key, self.generator)
        self.private_key_field.insert(1, k)
        self.random_a_field.insert(1, a)
        self.random_b_field.insert(1, b)
        self.x_field.insert(1, x)
        self.y_field.insert(1, y)
        self.status['text'] += 'Секретный ключ сгенерирован.'


if __name__ == '__main__':
    # GUI building
    root_client = Tk()
    root_client.title("Клиент")
    root_client.geometry("700x200")
    root_client.resizable(width=False, height=False)

    root_server = Tk()
    root_server.title("Сервер")
    root_server.geometry("700x200")
    root_server.resizable(width=False, height=False)

    app_client = ApplicationClient(root_client)
    app_client.mainloop()
