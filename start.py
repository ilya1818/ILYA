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
import importlib.util


def main():
    # Получаем путь к домашней директории текущего пользователя
    user_home_dir = os.path.expanduser("~")

    counterapp_dir = os.path.join(user_home_dir, "GraphicFunc")

    # Путь к main.py
    main_py_path = os.path.join(counterapp_dir, "main.py")

    try:
        # Импортируем main.py как модуль
        spec = importlib.util.spec_from_file_location("main", main_py_path)
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Возникла ошибка при запуске main.py: {e}")


if __name__ == "__main__":
    main()