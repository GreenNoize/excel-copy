import customtkinter as ctk
import pandas as pd

from get_file import select_excel_file, save_excel_file


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Копирование Excel")
        self.geometry("800x600")

        self.df = None
        self.row_vars = []
        self.checkboxes = []

        self.info_label = ctk.CTkLabel(
            self, text="Всего строк: 0 | Выбрано: 0 из 0"
        )
        self.info_label.pack(side="top", anchor="w", padx=20, pady=(10, 0))

        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(side="top", fill="both", expand=True, padx=20, pady=10)

        self.empty_label = ctk.CTkLabel(self.table_frame, text="Файл не загружен")
        self.empty_label.pack(pady=20)

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        self.select_all_var = ctk.BooleanVar(value=False)
        self.select_all_checkbox = ctk.CTkCheckBox(
            self.bottom_frame,
            text="Выбрать все",
            variable=self.select_all_var,
            command=self.toggle_select_all,
            state="disabled",
        )
        self.select_all_checkbox.pack(side="left", padx=10)

        self.select_button = ctk.CTkButton(
            self.bottom_frame, text="Выбрать файл", command=self.select_file
        )
        self.select_button.pack(side="left", expand=True, padx=10)

        self.copy_button = ctk.CTkButton(
            self.bottom_frame, text="Копировать", command=self.copy_data
        )
        self.copy_button.pack(side="left", expand=True, padx=10)

    def select_file(self):
        file_path = select_excel_file()
        if not file_path:
            return
        try:
            self.df = pd.read_excel(file_path)
        except Exception as e:
            self.info_label.configure(text=f"Ошибка чтения файла: {e}")
            return
        self.display_table(self.df)

    def display_table(self, df):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.row_vars.clear()
        self.checkboxes.clear()

        columns = list(df.columns)

        header = ctk.CTkFrame(self.table_frame, height=28)
        header.pack(fill="x", pady=(0, 5))
        header.pack_propagate(False)
        ctk.CTkFrame(header, width=24).pack(side="left")
        for col in columns:
            ctk.CTkLabel(header, text=str(col), anchor="w", height=28).pack(
                side="left", padx=5, expand=True, fill="x"
            )

        for _, row in df.iterrows():
            var = ctk.BooleanVar(value=False)
            self.row_vars.append(var)

            row_frame = ctk.CTkFrame(self.table_frame)
            row_frame.pack(fill="x", pady=1)

            cb_holder = ctk.CTkFrame(row_frame, width=24)
            cb_holder.pack(side="left")
            cb = ctk.CTkCheckBox(
                cb_holder,
                text="",
                variable=var,
                command=lambda v=var: self.on_row_toggle(v),
                width=24,
            )
            cb.pack()
            self.checkboxes.append(cb)

            for col in columns:
                ctk.CTkLabel(row_frame, text=str(row[col]), anchor="w", height=28).pack(
                    side="left", padx=5, expand=True, fill="x"
                )

        self.select_all_var.set(False)
        self.select_all_checkbox.configure(state="normal")
        self.update_info()

    def on_row_toggle(self, _var):
        self.update_info()
        selected = sum(v.get() for v in self.row_vars)
        self.select_all_var.set(selected == len(self.row_vars))

    def toggle_select_all(self):
        state = self.select_all_var.get()
        for var in self.row_vars:
            var.set(state)
        self.update_info()

    def update_info(self):
        total = len(self.row_vars)
        selected = sum(v.get() for v in self.row_vars)
        self.info_label.configure(
            text=f"Всего строк: {total} | Выбрано: {selected} из {total}"
        )

    def copy_data(self):
        if self.df is None:
            self.info_label.configure(text="Сначала загрузите файл")
            return

        selected_rows = [
            self.df.iloc[i] for i, var in enumerate(self.row_vars) if var.get()
        ]
        if not selected_rows:
            self.info_label.configure(text="Не выбрано ни одной строки")
            return

        file_path = save_excel_file()
        if not file_path:
            return

        new_df = pd.DataFrame(selected_rows, columns=self.df.columns)
        try:
            new_df.to_excel(file_path, index=False)
        except Exception as e:
            self.info_label.configure(text=f"Ошибка сохранения: {e}")
            return

        self.info_label.configure(
            text=f"Сохранено строк: {len(new_df)} в {file_path}"
        )


if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
