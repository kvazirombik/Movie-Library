import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = 'movies_data.json'

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library (Личная кинотека)")
        self.root.geometry("850x600")
        
        self.movies = self.load_data()
        
        self.setup_ui()
        self.update_table()

    def setup_ui(self):
        # Фрейм для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавление нового фильма", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(input_frame, width=20)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(input_frame, width=20)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(input_frame, width=20)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)

        add_btn = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="#4CAF50", fg="white")
        add_btn.grid(row=0, column=4, rowspan=2, padx=20, pady=5, sticky="nsew")

        # Фрейм для фильтрации
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(filter_frame, width=15)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="По году:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_year = tk.Entry(filter_frame, width=15)
        self.filter_year.grid(row=0, column=3, padx=5, pady=5)

        filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=10)

        reset_btn = tk.Button(filter_frame, text="Сбросить", command=self.reset_filter)
        reset_btn.grid(row=0, column=5, padx=5)

        # Таблица для вывода данных
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год выпуска")
        self.tree.heading("rating", text="Рейтинг")
        
        self.tree.column("year", width=100, anchor="center")
        self.tree.column("rating", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception:
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.movies, file, ensure_ascii=False, indent=4)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Валидация
        if not all([title, genre, year_str, rating_str]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом!")
            return

        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        
        self.movies.append(movie)
        self.save_data()
        self.update_table()
        
        # Очистка полей ввода
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Фильм успешно добавлен!")

    def update_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        display_data = data if data is not None else self.movies
        for movie in display_data:
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def apply_filter(self):
        genre_query = self.filter_genre.get().strip().lower()
        year_query = self.filter_year.get().strip()
        
        filtered = self.movies
        
        if genre_query:
            filtered = [m for m in filtered if genre_query in m["genre"].lower()]
            
        if year_query:
            try:
                year_target = int(year_query)
                filtered = [m for m in filtered if m["year"] == year_target]
            except ValueError:
                messagebox.showerror("Ошибка", "Для фильтрации год должен быть числом!")
                return
                
        self.update_table(filtered)

    def reset_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.update_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
