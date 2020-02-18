import sqlite3
from hashlib import md5
from tkinter import *
from tkinter import messagebox
import random
import copy
import datetime


# Methods for GUI buttons
def clear_button():
    txt1.delete(0, 'end')
    txt2.delete(0, 'end')
    txt3.delete(0, 'end')
    global hash_code
    hash_code = ''
    global main_login
    main_login = ''
    global time_start
    time_start = None


def auth_button():
    query = "SELECT * FROM users"
    cursor.execute(query)
    data = cursor.fetchall()

    login = txt1.get()  # Логин пользователя
    # Ищем логин
    check = False
    for user_data in data:
        if user_data[0] == login:
            check = True
            break

    if check:
        txt3.insert(1, string='Сеанс начался. ')
        n = 512
        code = ''  # Secret word (code)
        for i in range(n):
            k = random.randint(0, 1)
            if k == 0:
                c = random.randint(97, 122)
            else:
                c = random.randint(65, 90)

            code += chr(c)

        global time_start
        time_start = datetime.datetime.now()

        hash = md5(code.encode()).hexdigest()  # Вычисленный хэш от случайного слова
        txt2.insert(1, string=hash)

        global hash_code
        hash_code = copy.deepcopy(str(hash))
        global main_login
        main_login = copy.deepcopy(login)

    else:
        txt3.insert(1, string='Неправильный логин.')


def word_password_hash():
    time_now = datetime.datetime.now()
    delta = ((time_now - time_start).seconds) / 60  # Время существования случайного слова в минутах

    if delta < 2:
        hash_and_pass = txt2.get()
        hash_pass = md5(hash_and_pass.encode()).hexdigest()  # Вычисленный хэш от хэша слова + пароля

        query = "SELECT password FROM users WHERE login=?"
        cursor.execute(query, [(main_login)])
        data = cursor.fetchall()

        check_code = hash_code + data[0][0]
        result_hash = md5(check_code.encode()).hexdigest()
        txt3.insert(len(txt3.get()), string='Идёт хэширование и проверка... ')

        if hash_pass == result_hash:
            messagebox.showinfo('Аутентификация', 'Проверка пройдена.')
        else:
            messagebox.showinfo('Аутентификация', 'Проверка не пройдена.')
            clear_button()

    else:
        messagebox.showinfo('Аутентификация', 'Время сеанса истекло. Начните заново.')
        clear_button()


if __name__ == '__main__':
    # Database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    hash_code = ''
    main_login = ''
    time_start = None

    # Interface
    window = Tk()
    window.title('Task 1')
    window.geometry('445x225')
    window.resizable(width=False, height=False)

    lbl0 = Label(window, text='Challenge-response authentication', font='bold')
    lbl0.grid(column=1, row=0)

    lbl1 = Label(window, text='Логин: ')
    lbl1.grid(column=0, row=1)
    txt1 = Entry(window, width=60)
    txt1.grid(column=1, row=1)

    btn_calc = Button(window, text='Запрос', command=auth_button)
    btn_calc.grid(column=1, row=2)

    lbl2 = Label(window, text='Хэш-код: ')
    lbl2.grid(column=0, row=3)
    txt2 = Entry(window, width=60)
    txt2.grid(column=1, row=3)

    btn_hash = Button(window, text='Войти', width=8, command=word_password_hash)
    btn_hash.grid(column=1, row=4)

    empty_row = Label(window, text='\n ')
    empty_row.grid(column=1, row=5)

    lbl3 = Label(window, text='Статус: ')
    lbl3.grid(column=0, row=6)
    txt3 = Entry(window, width=60)
    txt3.grid(column=1, row=6)

    btn_calc = Button(window, text='Очистить', command=clear_button)
    btn_calc.grid(column=1, row=7)

    window.mainloop()
