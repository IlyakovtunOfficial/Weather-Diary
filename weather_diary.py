# weather_diary.py
import json
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []  # все записи
        self.create_widgets()
        self.load_default()

    def create_widgets(self):
        main = ttk.Frame(self.root, padding="10")
        main.grid(row=0, column=0, sticky="nsew")

        # Левая часть: ввод данных
        left = ttk.Frame(main)
        left.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        # Дата
        ttk.Label(left, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(left, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, sticky="ew")

        # Температура
        ttk.Label(left, text="Температура (°C):").grid(row=1, column=0, sticky="w")
        self.temp_var = tk.StringVar()
        self.temp_entry = ttk.Entry(left, textvariable=self.temp_var)
        self.temp_entry.grid(row=1, column=1, sticky="ew")

        # Описание
        ttk.Label(left, text="Описание погоды:").grid(row=2, column=0, sticky="nw")
        self.desc_text = tk.Text(left, width=20, height=4)
        self.desc_text.grid(row=2, column=1, sticky="ew")

        # Осадки
        self.precip_var = tk.BooleanVar()
        self.precip_check = ttk.Checkbutton(left, text="Осадки (да/нет)", variable=self.precip_var)
        self.precip_check.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)

        # Добавить запись
        self.add_btn = ttk.Button(left, text="Добавить запись", command=self.add_record)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Правая часть: фильтры, таблица, сохранение
        right = ttk.Frame(main)
        right.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Фильтры
        filter_frame = ttk.LabelFrame(right, text="Фильтры")
        filter_frame.grid(row=0, column=0, sticky="nwe", pady=5)

        ttk.Label(filter_frame, text="Дата:").grid(row=0, column=0, sticky="w")
        self.filter_date_var = tk.StringVar()
        self.filter_date_entry = ttk.Entry(filter_frame, textvariable=self.filter_date_var, width=15)
        self.filter_date_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(filter_frame, text="Минимальная температура:").grid(row=1, column=0, sticky="w")
        self.filter_temp_var = tk.StringVar()
        self.filter_temp_entry = ttk.Entry(filter_frame, textvariable=self.filter_temp_var, width=15)
        self.filter_temp_entry.grid(row=1, column=1, sticky="ew")

        self.apply_filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filters)
        self.apply_filter_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.clear_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.clear_filters)
        self.clear_filter_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Таблица записей
        self.tree = ttk.Treeview(right, columns=("date","temp","desc","precip"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")
        self.tree.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Сохранение/загрузка
        file_frame = ttk.Frame(right)
        file_frame.grid(row=2, column=0, sticky="ew", pady=5)

        self.save_btn = ttk.Button(file_frame, text="Сохранить JSON", command=self.save_to_json)
        self.save_btn.grid(row=0, column=0, padx=5)

        self.load_btn = ttk.Button(file_frame, text="Загрузить JSON", command=self.load_from_json)
        self.load_btn.grid(row=0, column=1, padx=5)

        # Раскладка
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        left.columnconfigure(1, weight=1)
        right.rowconfigure(1, weight=1)

    def add_record(self):
        date_str = self.date_var.get().strip()
        temp_str = self.temp_var.get().strip()
        description = self.desc_text.get("1.0", "end").strip()

        # Валидация
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Ошибка ввода", "Дата должна быть в формате YYYY-MM-DD.")
            return

        try:
            temp = float(temp_str)
        except Exception:
            messagebox.showerror("Ошибка ввода", "Температура должна быть числом.")
            return

        if description == "":
            messagebox.showerror("Ошибка ввода", "Описание не должно быть пустым.")
            return

        precip = self.precip_var.get()

        rec = {
            "date": date_str,
            "temperature": temp,
            "description": description,
            "precipitation": precip
        }
        self.records.append(rec)
        self.update_treeview()
        # Очистка полей
        self.date_var.set("")
        self.temp_var.set("")
        self.desc_text.delete("1.0","end")
        self.precip_var.set(False)

    def update_treeview(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data_to_show = data if data is not None else self.records
        for rec in data_to_show:
            self.tree.insert("", "end", values=(
                rec.get("date",""),
                rec.get("temperature",""),
                rec.get("description",""),
                "Да" if rec.get("precipitation") else "Нет"
            ))

    def apply_filters(self):
        date_filter = self.filter_date_var.get().strip()
        min_temp = self.filter_temp_var.get().strip()

        filtered = self.records
        if date_filter:
            try:
                datetime.datetime.strptime(date_filter, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Ошибка фильтра", "Дата фильтра должна быть в формате YYYY-MM-DD.")
                return
            filtered = [r for r in filtered if r.get("date") == date_filter]

        if min_temp:
            try:
                t = float(min_temp)
            except Exception:
                messagebox.showerror("Ошибка фильтра", "Минимальная температура должна быть числом.")
                return
            filtered = [r for r in filtered if r.get("temperature", 0) >= t]

        self.update_treeview(filtered)

    def clear_filters(self):
        self.filter_date_var.set("")
        self.filter_temp_var.set("")
        self.update_treeview(self.records)

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON", "*.json")])
        if not filename:
            return
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def load_from_json(self):
        filename = filedialog.askopenfilename(defaultextension=".json",
                                              filetypes=[("JSON", "*.json")])
        if not filename:
            return
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            self.records = data
            self.update_treeview()
        else:
            messagebox.showerror("Ошибка", "Некорректный формат файла.")

    def load_default(self):
        # Попытка загрузить пример данных, если есть weather_records.json
        try:
            with open("weather_records.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self.records = data
                self.update_treeview()
        except FileNotFoundError:
            pass

def main():
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()