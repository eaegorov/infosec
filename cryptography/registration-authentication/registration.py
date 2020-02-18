import sqlite3
from tkinter import *
from tkinter import messagebox


def registr_button():
    query = "SELECT * FROM users"
    cursor.execute(query)
    data = cursor.fetchall()

    login = txt1.get()  # Логин пользователя
    password = txt2.get()  # Пароль пользователя
    # Ищем логин
    check = False
    for user_data in data:
        if user_data[0] == login:
            check = True
            break

    if check:
        messagebox.showinfo('Регистрация', 'Данный логин уже существует.')
    else:
        if len(password) == 0:
            messagebox.showinfo('Регистрация', 'Введите пароль.')
        else:
            data = [(login, password)]
            query = "INSERT INTO users VALUES (?, ?)"
            cursor.execute(query, data[0])
            connection.commit()
            messagebox.showinfo('Регистрация', 'Регистрация прошла успешно.')


if __name__ == '__main__':
    # Database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Interface
    window = Tk()
    window.title('Task 1')
    window.geometry('320x120')
    window.resizable(width=False, height=False)

    lbl0 = Label(window, text='Регистрация', font='bold')
    lbl0.grid(column=1, row=0)

    lbl1 = Label(window, text='Логин: ')
    lbl1.grid(column=0, row=1)
    txt1 = Entry(window, width=40)
    txt1.grid(column=1, row=1)

    lbl2 = Label(window, text='Пароль: ')
    lbl2.grid(column=0, row=2)
    txt2 = Entry(window, width=40)
    txt2.grid(column=1, row=2)

    btn_calc = Button(window, text='Зарегистрироваться', command=registr_button)
    btn_calc.grid(column=1, row=3)

    window.mainloop()