import tkinter as tk
import numpy as np
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import os
import subprocess
import shutil
import sys
import tempfile

class MainWindow(tk.Tk):  # Inherit from tk.Tk
    def __init__(self):
        super().__init__()
        self.title("График функции y = ax^3")
        self.geometry("663x700")
        self.version = '1.0.2'

        # Установка шрифта
        self.option_add("*Font", "Calibri 12")

        # Установка цвета фона
        self.configure(bg="gainsboro")

        # Создание экземпляра Figure и Axes
        self.figure, self.axes = plt.subplots()
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.figure_canvas.get_tk_widget().place(relx=0.5, rely=0.57, anchor=tk.CENTER)

        # Установка пределов осей
        self.axes.set_xlim(-10, 10)  # Пределы оси x
        self.axes.set_ylim(-10, 10)  # Пределы оси y

        # Рисование осей
        self.draw_lines()

        # Перемещение осей в центр
        self.move_axes_to_center()

        # Создание меню
        self.menu_bar = tk.Menu(self)

        # Меню "Файл"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label="Файл", menu=self.file_menu)

        # Меню "Справка"
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="О программе", command=self.show_about_dialog)
        self.menu_bar.add_cascade(label="Справка", menu=self.help_menu)

        # Меню "Обновление ПО"
        self.update_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.update_menu.add_command(label="Проверить обновления", command=self.check_update)
        self.menu_bar.add_cascade(label="Обновление ПО", menu=self.update_menu)

        # Установка созданного меню
        self.config(menu=self.menu_bar)

        # Список для хранения данных графиков
        self.plot_data = []

        self.label_a = tk.Label(self, text="Значение a =", bg="gainsboro")
        self.edit_a = tk.Entry(self)

        self.button_plot = tk.Button(self, text="Нарисовать график", command=self.plot_graph, bg="blue")
        self.button_clear = tk.Button(self, text="Очистить график", command=self.clear_graphs, bg="red")

        self.label_a.place(relx=0.3, rely=0.04, anchor=tk.CENTER)
        self.edit_a.place(relx=0.5, rely=0.04, anchor=tk.CENTER)

        self.button_plot.place(relx=0.5, rely=0.11, anchor=tk.CENTER)
        self.button_clear.place(relx=0.5, rely=0.17, anchor=tk.CENTER)

        # Создание элемента для отображения прогресса
        self.loading_label = tk.Label(self, text="", bg="gainsboro")

        self.loading_label.place(relx=0.5, rely=0.24, anchor=tk.CENTER)

    def check_update(self):
        try:
            response = requests.get('https://raw.githubusercontent.com/ilya1818/ILYA/main/version.txt')
            if self.version == response.text:
                messagebox.showinfo("Обновление ПО", "Программа не требует обновления")
                return
            else:
                user_input = messagebox.askquestion("Обновление ПО",
                                                    "Обнаружено обновление. Хотите обновить программу?")
                if user_input == "yes":
                    self.download_update()
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось проверить обновления: {e}")

    def download_update(self):
        try:
            response = requests.get('https://raw.githubusercontent.com/ilya1818/ILYA/main/main.py')
            with open('main.py', 'wb') as f:
                f.write(response.content)
            messagebox.showinfo("Обновление ПО", "Программа успешно обновлена. Перезапустите приложение.")
            # Дополнительные действия по обновлению, если необходимо
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить обновление: {e}")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding='utf-8') as file:
                text = file.read()
            self.count_characters(refresh=text)

    def run(self):
        self.mainloop()

    @staticmethod
    def show_info_message(message):
        messagebox.showinfo("Информация", message)

    def draw_lines(self):
        # Рисование вертикальной линии
        self.axes.axvline(0, color='black', linewidth=1)
        self.axes.axhline(0, color='black', linewidth=1)

    def add_tick_labels(self):
        self.axes.set_xticks([-10, -5, 0, 5, 10])
        self.axes.set_yticks([-10, -5, 0, 5, 10])

    def move_axes_to_center(self):
        canvas_width = self.figure_canvas.get_tk_widget().winfo_width()
        canvas_height = self.figure_canvas.get_tk_widget().winfo_height()
        axes_width = self.figure_canvas.get_tk_widget().winfo_width()
        axes_height = self.figure_canvas.get_tk_widget().winfo_height()

        x_offset = (canvas_height - axes_height) // 2
        y_offset = (canvas_width - axes_width) // 2

        self.figure_canvas.get_tk_widget().place(x=x_offset, y=y_offset)

    def show_about_dialog(self):
        messagebox.showinfo("О программе",
                            f"График функции y = ax^3\nВерсия: {self.version}\nАвтор: Илья\nКомпания: ILYA Company")

    def clear_graphs(self):
        for line in self.axes.lines:
            line.remove()  # Удаляем каждую линию графика
        self.plot_data.clear()  # Очищаем список данных графиков

        # Удаляем легенду
        if self.axes.legend_ is not None:
            self.axes.legend_.remove()

        self.draw_lines()  # Рисуем линии осей
        self.figure_canvas.draw_idle()  # Обновляем отображение без блокировки

    def quit(self):
        self.destroy()

    def plot_graph(self):

        a = float(self.edit_a.get())

        try:
            a = float(self.edit_a.get())
            if a > 100 or a < -100:
                messagebox.showwarning("Предупреждение", "Введите значение а в диапазоне от -100 до 100.")
                return

            # Проверка на количество графиков
            if len(self.plot_data) >= 17:
                messagebox.showerror("Ошибка", "Достигнуто максимальное количество графиков (17)")
                return

        except ValueError:
            messagebox.showwarning("Предупреждение", "Введите корректное числовое значение для а.")

        x = np.linspace(-10, 10, 100)
        y = a * x ** 3

        # Очищаем предыдущий график
        self.axes.clear()

        # Рисование линий
        self.draw_lines()

        # Устанавливаем данные графика
        self.plot_data.append((x, y, f"y = {a}x^3"))

        # Показываем все графики на одной плоскости
        for i, data in enumerate(self.plot_data):
            self.axes.plot(data[0], data[1], label=data[2])

        # Устанавливаем метки осей
        self.axes.set_xlabel('y')
        self.axes.set_ylabel('x')

        # Добавляем легенду
        self.axes.legend()

        # Показываем график
        self.figure_canvas.draw()

        # Устанавливаем пределы осей
        max_range = max(abs(-10), abs(10), abs(a))
        self.axes.set_ylim(-max_range, max_range)  # Пределы оси y

        # Обновляем отображение
        self.figure_canvas.draw()

    def center_window(self):
        # Размещение окна по центру экрана
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        x = int((screen_width - window_width) / 2) - 30
        y = int((screen_height - window_height) / 2) - 150

        self.geometry(f"+{x}+{y}")


app = MainWindow()
app.run()
