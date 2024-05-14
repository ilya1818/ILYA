import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
import importlib.util
import requests


def main():
    # Получаем путь к домашней директории текущего пользователя
    user_home_dir = os.path.expanduser("~")

    # Путь к директории CounterApp в домашней директории пользователя
    grafikapp_dir = os.path.join(user_home_dir, "GrafikApp")

    # Путь к main.py
    main_py_path = os.path.join(grafikapp_dir, "main.py")

    try:
        # Импортируем main.py как модуль
        spec = importlib.util.spec_from_file_location("main", main_py_path)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Возникла ошибка при запуске main.py: {e}")


if __name__ == "__main__":
    main()