import tkinter as tk
from tkinter import filedialog


def select_excel_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Выберите файл Excel",
        filetypes=[
            ("Excel файлы", "*.xlsx *.xls"),
            ("Excel 2007+", "*.xlsx"),
            ("Excel 97-2003", "*.xls"),
            ("Все файлы", "*.*"),
        ],
    )

    root.destroy()
    return file_path


def save_excel_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        title="Сохранить файл как",
        defaultextension=".xlsx",
        filetypes=[
            ("Excel файлы", "*.xlsx *.xls"),
            ("Excel 2007+", "*.xlsx"),
            ("Excel 97-2003", "*.xls"),
            ("Все файлы", "*.*"),
        ],
    )

    root.destroy()
    return file_path
