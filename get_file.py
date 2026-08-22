"""Диалоги выбора и сохранения Excel-файлов."""

import tkinter as tk
from tkinter import filedialog





def select_excel_file():
    """Открывает диалог выбора файла с фильтром Excel.

    Returns:
        str: Путь к выбранному файлу или пустая строка, если выбор отменён.
    """


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
    """Открывает диалог сохранения файла с фильтром Excel.

    Returns:
        str: Путь для сохранения или пустая строка, если выбор отменён.
    """


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
