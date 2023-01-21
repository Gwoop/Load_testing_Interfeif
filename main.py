from tkinter import *
from tkinter import ttk
from functools import partial
import psutil
import pymysql
import openpyxl
import subprocess
from threading import Thread
from threading import Timer
import datetime
from datetime import date
from multiprocessing import Process


#список элементов для combobox-ов
modelForComboBox = ["Users","Others","More"]



def threads():
    zgluchka =0
    import time
    subprocess.Popen('Project1.exe')
    time.sleep(5)
    xlsx = readxlsx()
    i = 0
    T = 2  # стартовое число потоков
    countermax = T
    sended_request = 0
    while zgluchka == 0:
        if int(psutil.virtual_memory()[2]) > 90:  # верхний порог нагрузки
            T -= 1
        if int(psutil.virtual_memory()[2]) < 90:
            T += 1
        if T > countermax:  #
            counter = T
        if T <= 0:
            T = 1
        time = Timer(5, log, args=(T, countermax, sended_request,))
        time.start()

        threads = []
        for n in range(int(T)):
            t = Thread(target=bd, args=(xlsx,), daemon=False)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
            sended_request = sended_request + 1

#MainThread = Thread(target=threads, args=(), daemon=False)
#p1 = Process(target=threads, daemon=False)


def proc_start():
    p_to_start = Process(target=threads,daemon=False)
    p_to_start.start()
    return p_to_start


def proc_stop(p_to_stop):
    p_to_stop.kill()



#главное окно
class MainWindow(Tk):

    # метод для создания окна
    def __init__(self):
        super().__init__()

        # конфигурация окна
        self.title("Меню")
        self.geometry("250x200")
        self.resizable(width=False,height=False)

        #кнопки для переходв
        self.button = ttk.Button(self, text="Переход в окно нагрузки CPU")
        self.button["command"] = self.goToCPUWindow
        self.button.grid(column=0,row=0,pady=20,padx=35)

        self.button1 = ttk.Button(self, text="Переход в окно нагрузки GPU")
        self.button1["command"] = self.goToGPUWindow
        self.button1.grid(column=0,row=1,pady=20,padx=35)

        self.buttonRoot = ttk.Button(self, text="Переход в окно администратора")
        self.buttonRoot["command"] = self.goToRootWindow
        self.buttonRoot.grid(column=0, row=2,pady=20,padx=35)

    #методы переход между окнами

    def goToCPUWindow(self):
        self.destroy()
        window = WindowCPU()

    def goToGPUWindow(self):
        self.destroy()
        window = WindowGPU()

    def goToRootWindow(self):
        self.destroy()
        window = WindowRoot()

#окно нагрузки ЦПУ
class WindowCPU(Tk):

    #метод создания окна
    def __init__(self):
        super().__init__()
        #главная настройка окна
        self.title("Тест CPU")
        self.geometry("600x300")
        self.resizable(width=False, height=False)

        #элементы
        self.labelInfo = ttk.Label(self, text="Порог нагрузки CPU",
                           font=("Arial Bold", 12))
        self.labelInfo.grid(column=0, row=0, pady=20, padx=10)

        #Ввод необходимой  нагрузки
        self.procents = ttk.Entry(self, width=20, font=("Arial Bold", 12))  # поле ввода
        self.procents.insert(0,"60%")
        self.procents.grid(column=0, row=1, padx=20, pady=10)

        self.labelInfoUpper = ttk.Label(self, text="Текущая нагрузка",
                                   font=("Arial Bold", 12))
        self.labelInfoUpper.grid(column=1, row=0, pady=20, padx=10)

        #Вывод текущего процента нагрузки ЦП
        # self.labelInfo = ttk.Label(self, text= psutil.virtual_memory()[2],
        #                            font=("Arial Bold", 12))
        self.labelInfo.grid(column=1, row=1, pady=20, padx=10)

        #вывод статуса программы
        self.labelStatus = ttk.Label(self, text="Остановлен",
                                   font=("Arial Bold", 12))
        self.labelStatus.grid(column=2, row=0)

        #не до конца понимаю как работает self, но если запихнуть его в кнопки, то они перестают работать
        btnStart = ttk.Button(self, text="Старт")
        btnStart.grid(column=0, row=3, padx=15, pady=10)
        btnStart["command"] = self.btnStart

        btnPause = ttk.Button(self, text="Пауза")
        btnPause.grid(column=1, row=3, padx=15, pady=10)
        btnPause["command"] = self.btnPause

        btnStop = ttk.Button(self, text="Остановить")
        btnStop.grid(column=2, row=3, padx=15, pady=10)
        btnStop["command"] = self.btnStop

        btnBack = ttk.Button(self, text="Назад")
        btnBack.grid(column=0, row=6, padx=15, pady=10)
        btnBack["command"] = self.btnBack


        self.labelPotokiMax = ttk.Label(self, text="MAX потоков",
                                     font=("Arial Bold", 12))
        self.labelPotokiMax.grid(column=3, row=0)


        #Вывод максимального колличества потоков
        self.labelPotokiMaxINFO = ttk.Label(self, text="1",
                                        font=("Arial Bold", 12))
        self.labelPotokiMaxINFO.grid(column=3, row=1)

        self.labelPotokiNOW = ttk.Label(self, text="NOW потоков",
                                        font=("Arial Bold", 12))
        self.labelPotokiNOW.grid(column=3, row=2)

        # Вывод текущих потоков
        self.labelPotokiNOWINFO = ttk.Label(self, text="1",
                                            font=("Arial Bold", 12))
        self.labelPotokiNOWINFO.grid(column=3, row=3)

        self.Requests = ttk.Label(self, text="Отправленных\nнагрузок",
                                        font=("Arial Bold", 12), justify="center")
        self.Requests.grid(column=3, row=4)

        # Вывод текущего колличества запросов
        self.RequestsShow = ttk.Label(self, text="1",
                                            font=("Arial Bold", 12))
        self.RequestsShow.grid(column=3, row=5, rowspan=2)



    #переход в главное окно
    def btnBack(self):
        self.destroy()
        window = MainWindow()

    #старт теста
    def btnStart(self):
        self.labelStatus.config(text="Старт")
        global p
        p = proc_start()



    #пауза
    def btnPause(self):
        self.labelStatus.config(text="Пауза")

        proc_stop(p)


    #стоп
    def btnStop(self):
        self.labelStatus.config(text="Остановлен")
        
        proc_stop(p)





def readxlsx():
    wb = openpyxl.load_workbook('sql.xlsx')
    sheet = wb.active
    xlsx = []
    for i in range(sheet.max_row):
        xlsx.append(str(sheet["A" + str(i + 1)].value))
    return xlsx

def bd(quvery):
    con = pymysql.connect(host='localhost', user='root', password='1234', db='marlo')  # конект к бд
    for i in quvery:
        cur = con.cursor()
        cur.arraysize = 56000
        print(i)
        cur.execute(query=i)
    con.close()

def log(num,nummax,sended_request):
    current_date = date.today()
    dt_now = datetime.datetime.now()
    f = open(str(current_date)+'.txt','a')
    f.write(str(dt_now) + " active_thread: " + str(num)  + " max_thread: " + str(nummax) + " sended_request: " + str(sended_request) + "\n")
    f.close()






#окно нагрузки GPU
class WindowGPU(Tk):
    # метод создания окна
    def __init__(self):
        super().__init__()

        # главная настройка окна
        self.title("Тест GPU")
        self.geometry("600x300")
        self.resizable(width=False, height=False)

        # элементы
        self.labelInfo = ttk.Label(self, text="Порог нагрузки GPU",
                                   font=("Arial Bold", 12))
        self.labelInfo.grid(column=0, row=0, pady=20, padx=10)

        self.procents = ttk.Entry(self, width=20, font=("Arial Bold", 12))  # поле ввода
        self.procents.insert(0, "60%")
        self.procents.grid(column=0, row=1, padx=20, pady=10)

        self.labelInfoUpper = ttk.Label(self, text="Текущая нагрузка",
                                        font=("Arial Bold", 12))
        self.labelInfoUpper.grid(column=1, row=0, pady=20, padx=10)

        self.labelInfo = ttk.Label(self, text="60%",
                                   font=("Arial Bold", 12))
        self.labelInfo.grid(column=1, row=1, pady=20, padx=10)

        self.labelStatus = ttk.Label(self, text="Остановлен",
                                     font=("Arial Bold", 12))
        self.labelStatus.grid(column=2, row=0, rowspan=2)

        # не до конца понимаю как работает self, но если запихнуть его в кнопки, то они перестают работать
        btnStart = ttk.Button(self, text="Старт")
        btnStart.grid(column=0, row=3, padx=15, pady=10)
        btnStart["command"] = self.btnStart

        btnPause = ttk.Button(self, text="Пауза")
        btnPause.grid(column=1, row=3, padx=15, pady=10)
        btnPause["command"] = self.btnPause

        btnStop = ttk.Button(self, text="Остановить")
        btnStop.grid(column=2, row=3, padx=15, pady=10)
        btnStop["command"] = self.btnStop

        btnBack = ttk.Button(self, text="Назад")
        btnBack.grid(column=0, row=6, padx=15, pady=10)
        btnBack["command"] = self.btnBack

        self.labelInfoAboutComboBox = ttk.Label(self, text="Выпадающий список для выбора отправляемых запросов",
                                                font=("Arial Bold", 12))
        self.labelInfoAboutComboBox.grid(column=0, row=4, columnspan=3, pady=10)

        # выпадающий список
        self.combobox = ttk.Combobox(values=modelForComboBox, width=20)
        self.combobox.grid(column=0, row=5, columnspan=3, pady=10)
        # через partial передаю нормально аргументы в метод иначе оч плохо всё будет
        self.combobox.bind("<<ComboboxSelected>>", partial(self.selected))

        self.labelPotokiMax = ttk.Label(self, text="MAX потоков",
                                        font=("Arial Bold", 12))
        self.labelPotokiMax.grid(column=3, row=0, rowspan=2)

        # Вывод максимального колличества потоков
        self.labelPotokiMaxINFO = ttk.Label(self, text="1",
                                            font=("Arial Bold", 12))
        self.labelPotokiMaxINFO.grid(column=3, row=1, rowspan=2)

        self.labelPotokiNOW = ttk.Label(self, text="NOW потоков",
                                        font=("Arial Bold", 12))
        self.labelPotokiNOW.grid(column=3, row=2, rowspan=2)

        # Вывод текущих потоков
        self.labelPotokiNOWINFO = ttk.Label(self, text="1",
                                            font=("Arial Bold", 12))
        self.labelPotokiNOWINFO.grid(column=3, row=3, rowspan=2)

        self.Requests = ttk.Label(self, text="Отправленных\nзапросов",
                                  font=("Arial Bold", 12), justify="center")
        self.Requests.grid(column=3, row=4, rowspan=2)

        # Вывод текущего колличества запросов
        self.RequestsShow = ttk.Label(self, text="1",
                                      font=("Arial Bold", 12))
        self.RequestsShow.grid(column=3, row=5, rowspan=2)

    # метод для выбора элемента из комбо бокса
    def selected(self, event):
        selection = self.combobox.get()
        print(selection)

    # переход в главное окно
    def btnBack(self):
        self.destroy()
        window = MainWindow()

    # старт теста
    def btnStart(self):
        self.labelStatus.config(text="Старт")

    # пауза
    def btnPause(self):
        self.labelStatus.config(text="Пауза")

    # стоп
    def btnStop(self):
        self.labelStatus.config(text="Остановлен")

#окно root
class WindowRoot(Tk):

    #массив с эмуляцией данными
    people = [(1, "Tom", 38, "tom@email.com"), (2, "Bob", 42, "bob@email.com"),
              (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"),
              (3, "Sауйайуайam", 28, "sam@email.com"), (5, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"), (3, "Sауйауйайуam", 28, "sam@email.com"),
              (6, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"),
              (3, "Saауайуайm", 28, "sam@email.com"),
              (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"), (3, "Sam", 28, "sam@email.com"),
              (7, "Sam", 28, "sam@email.com")]

    #метод для создания окна
    def __init__(self):
        super().__init__()

        #тут я его настраивать начинаю
        self.title("Администратор")
        self.geometry("1480x400")
        self.resizable(width=True, height=False)

        #Определяю столбцы для таблицы (нужно бужет это для каждой отдельной таблицы..
        columns = ("ID","name", "age", "email")

        #создаю сам элемент и вывожу его на экран через pack
        self.tree = ttk.Treeview(columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew",rowspan=3)

        #Переименовываю зоголовки т.е это нужно так-же для каждой отдельной таблицы
        self.tree.heading("ID",text="Первичный ключ")
        self.tree.heading("name", text="Имя")
        self.tree.heading("age", text="Возраст")
        self.tree.heading("email", text="Email")



        #кнопка для обновления данных, хотя можно и без неё
        btnAddDate = ttk.Button(self, text="Обновить данные")
        btnAddDate.grid(column=1, row=7, padx=15, pady=10)
        btnAddDate["command"] = self.refreshDate

        # кнопка для обновления данных, хотя можно и без неё
        btnAddDate = ttk.Button(self, text="Удалить данные")
        btnAddDate.grid(column=2, row=7, padx=15, pady=10)
        btnAddDate["command"] = self.clearTree

        #ещё кнопки в окне
        btnAdd = ttk.Button(self, text="Добавить")
        btnAdd.grid(column=3, row=0, padx=15, pady=10)
        btnAdd["command"] = self.addData

        btnDel = ttk.Button(self, text="Удалить")
        btnDel.grid(column=3, row=1, padx=15, pady=10)
        btnDel["command"] = self.delData

        btnEdit = ttk.Button(self, text="Изменить")
        btnEdit.grid(column=3, row=2, padx=15, pady=10)
        btnEdit["command"] = self.edtData

        btnBack = ttk.Button(self, text="Назад")
        btnBack.grid(column=3, row=3, padx=15, pady=10)
        btnBack["command"] = self.goBack

        self.laberOverComboBox = ttk.Label(self, text="Выберете таблицу",
                                     font=("Arial Bold", 12))
        self.laberOverComboBox.grid(column=3, row=4, pady=10, padx=50)
        # выпадающий список
        self.combobox = ttk.Combobox(values=modelForComboBox, width=20)
        self.combobox.grid(column=3, row=5, pady=10)
        # через partial передаю нормально аргументы в метод иначе оч плохо всё будет
        self.combobox.bind("<<ComboboxSelected>>", partial(self.selected))

        #поля ввода

        # //////////// ПЕРВЫЙ СТОЛБЕЦ

        self.entry1 = ttk.Entry(self, width=20, font=("Arial Bold", 12),show="some body")  # поле ввода
        self.entry1.grid(column=1, row=1,pady=10)


        #для отображения того, что будет вводить
        self.entryLabel1 = ttk.Label(self, text="Введите что-то",
                                            font=("Arial Bold", 12))
        self.entryLabel1.grid(column=1, row=0,pady=10, padx=50)

        #////////////

        self.entry2 = ttk.Entry(self, width=20, font=("Arial Bold", 12), show="some body")  # поле ввода
        self.entry2.grid(column=1, row=3, pady=10)

        # для отображения того, что будет вводить
        self.entryLabel2 = ttk.Label(self, text="Введите что-то 2",
                                            font=("Arial Bold", 12))
        self.entryLabel2.grid(column=1, row=2, pady=10, padx=50)

        # ////////////

        self.entry3 = ttk.Entry(self, width=20, font=("Arial Bold", 12), show="some body")  # поле ввода
        self.entry3.grid(column=1, row=5, pady=10)

        # для отображения того, что будет вводить
        self.entryLabel3 = ttk.Label(self, text="Введите что-то 3",
                                     font=("Arial Bold", 12))
        self.entryLabel3.grid(column=1, row=4, pady=10, padx=50)

        # //////////// ВТОРОЙ СТОЛБЕЦ

        self.entry4 = ttk.Entry(self, width=20, font=("Arial Bold", 12), show="some body")  # поле ввода
        self.entry4.grid(column=2, row=1, pady=10)

        self.entryLabel4 = ttk.Label(self, text="Введите что-то 4",
                                     font=("Arial Bold", 12))
        self.entryLabel4.grid(column=2, row=0, pady=10, padx=50)

        # ////////////

        self.entry5 = ttk.Entry(self, width=20, font=("Arial Bold", 12), show="some body")  # поле ввода
        self.entry5.grid(column=2, row=3, pady=10)

        # для отображения того, что будет вводить
        self.entryLabel5 = ttk.Label(self, text="Введите что-то 5",
                                     font=("Arial Bold", 12))
        self.entryLabel5.grid(column=2, row=2, pady=10, padx=50)

        # ////////////

        self.entry6 = ttk.Entry(self, width=20, font=("Arial Bold", 12), show="some body")  # поле ввода
        self.entry6.grid(column=2, row=5, pady=10)

        # для отображения того, что будет вводить
        self.entryLabel6 = ttk.Label(self, text="Введите что-то 6",
                                     font=("Arial Bold", 12))
        self.entryLabel6.grid(column=2,row=4, pady=10, padx=50)


        #это типо плейсхолдера т.к обычного нет в данной библиотеке

        # метод для выбора элемента из комбо бокса

    def selected(self, event):
        selection = self.combobox.get()
        print(selection)

    #метод для очистки данных в таблице
    def clearTree(self):
        print("Очищаю данные")
        x = self.tree.get_children()
        for item in x:  ## Changing all children from root item
            self.tree.delete(item)


    #метод для обновления данных
    def refreshDate(self):
        #добавляю данные из массива в таблицу
        print("Обновляю данные")
        for person in self.people:
            self.tree.insert("", END, values=person)

    #методы кнопок добавления удаления и изменения
    def addData(self):
        print("Добавляю данные")
        self.tree.insert("", END, values=("foo", "bar","aboba","bobus"))

    def delData(self):
        print("Удаляю данные")
        selected_item = self.tree.selection()[0]  ## get selected item
        self.tree.delete(selected_item)

    def edtData(self):
        print("Изменяю данные")
        self.tree.item(self.tree.selection()[0], text="blub", values=("fGWRoo", "GRGWG","aboRGWGWRGba","bGWRGWobus"))


    #метод для кнопки, а именно переход обратно в главное окно
    def goBack(self):
        self.destroy()
        window = MainWindow()



#это код для запуска приложения, так сказать главное окно для начала переходов (костыли)
def click():
    root.destroy()
    window = MainWindow()

root = Tk()
root.title("Окно запуска")
root.geometry("250x200")
open_button = ttk.Button(text="Запуск", command=click)
open_button.pack(anchor="center", expand=1)
root.mainloop()