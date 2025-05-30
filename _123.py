import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
global tree, search_entry

TABLES = {
    "languages": """
        CREATE TABLE IF NOT EXISTS languages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """,
    "countries": """
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """,
    "genres": """
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """,
    "directors": """
        CREATE TABLE IF NOT EXISTS directors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """,
    "filmid": """
        CREATE TABLE IF NOT EXISTS filmid (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            director_id INTEGER,
            release_year INTEGER,
            genre_id INTEGER,
            duration INTEGER,
            rating REAL,
            language_id INTEGER,
            country_id INTEGER,
            description TEXT,
            FOREIGN KEY (director_id) REFERENCES directors(id),
            FOREIGN KEY (genre_id) REFERENCES genres(id),
            FOREIGN KEY (language_id) REFERENCES languages(id),
            FOREIGN KEY (country_id) REFERENCES countries(id)
        )
    """
}

INSERTS = {
    "languages": "INSERT INTO languages (name) VALUES ('English')",
    "countries": "INSERT INTO countries (name) VALUES ('USA'), ('UK'), ('France'), ('Germany'), ('Italy')",
    "genres": "INSERT INTO genres (name) VALUES ('Drama'), ('Sci-Fi'), ('Crime'), ('Adventure'), ('Action'), ('Thriller'), ('Comedy')",
    "directors": "INSERT INTO directors (name) VALUES ('Francis Ford Coppola'), ('Christopher Nolan'), ('Quentin Tarantino'), ('Steven Spielberg'), ('Martin Scorsese')",
    "filmid": """
        INSERT INTO filmid (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description) VALUES
        ('The From In With.', (SELECT id FROM directors WHERE name='Francis Ford Coppola'), 1994, (SELECT id FROM genres WHERE name='Drama'), 142, 9.3, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='USA'), 'The In With By On. A In From By The At. On A With By By On To A.'),
        ('The By On To.', (SELECT id FROM directors WHERE name='Christopher Nolan'), 2010, (SELECT id FROM genres WHERE name='Sci-Fi'), 148, 8.8, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='UK'), 'The A The On The In. By To A At On The. From The In With At In To A.'),
        ('In The With On.', (SELECT id FROM directors WHERE name='Quentin Tarantino'), 1972, (SELECT id FROM genres WHERE name='Crime'), 175, 9.2, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='USA'), 'On From The By At The A. In From By With To On. A The By In With At On To A.'),
        ('The A To From.', (SELECT id FROM directors WHERE name='Steven Spielberg'), 1994, (SELECT id FROM genres WHERE name='Adventure'), 154, 8.9, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='France'), 'With By In The A On. The With To A At The From. On A From With At By The.'),
        ('On The From With.', (SELECT id FROM directors WHERE name='Martin Scorsese'), 2008, (SELECT id FROM genres WHERE name='Action'), 152, 9.0, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='Germany'), 'The A By On In The. At With To A From On The. With On By The A In To From.'),
        ('From The By With.', (SELECT id FROM directors WHERE name='Christopher Nolan'), 1960, (SELECT id FROM genres WHERE name='Drama'), 134, 8.5, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='UK'), 'The A On From The At. With To By In A The On. At The In From With By To A.'),
        ('The By On A.', (SELECT id FROM directors WHERE name='Francis Ford Coppola'), 1999, (SELECT id FROM genres WHERE name='Thriller'), 112, 7.8, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='USA'), 'A The On By In The At. From With A On By To The. In The By With At A From.'),
        ('On A The From.', (SELECT id FROM directors WHERE name='Quentin Tarantino'), 2015, (SELECT id FROM genres WHERE name='Comedy'), 126, 7.9, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='Italy'), 'By With A On In The From. The By At A With On To. At In The By From With A.'),
        ('By The On From.', (SELECT id FROM directors WHERE name='Steven Spielberg'), 1975, (SELECT id FROM genres WHERE name='Action'), 143, 8.7, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='France'), 'A With On The By From In. The A At On With To From. By In The A From With At On.'),
        ('From With The By.', (SELECT id FROM directors WHERE name='Martin Scorsese'), 1980, (SELECT id FROM genres WHERE name='Crime'), 163, 9.1, (SELECT id FROM languages WHERE name='English'), (SELECT id FROM countries WHERE name='Germany'), 'On The A By In The From. With By On A The In From. To The In At By With On A.')
    """
}

root = tk.Tk()
root.title("Filmid")
entries = {}
tree = None
search_entry = None

def create_db():
    with sqlite3.connect("filmid.db") as conn:
        cursor = conn.cursor()
        for table_sql in TABLES.values():
            cursor.execute(table_sql)
        for insert_sql in INSERTS.values():
            cursor.executescript(insert_sql)
        conn.commit()

def load_data_from_db(search_query=""):
    global tree
    tree.delete(*tree.get_children())
    with sqlite3.connect("filmid.db") as conn:
        cursor = conn.cursor()
        query = """
            SELECT f.id, f.title, d.name, f.release_year, g.name, f.duration, f.rating, l.name, c.name, f.description
            FROM filmid f
            LEFT JOIN directors d ON f.director_id = d.id
            LEFT JOIN genres g ON f.genre_id = g.id
            LEFT JOIN languages l ON f.language_id = l.id
            LEFT JOIN countries c ON f.country_id = c.id
            WHERE f.title LIKE ?
        """
        cursor.execute(query, (f"%{search_query}%",))
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

def on_search():
    global search_entry
    load_data_from_db(search_entry.get())

def lisa_andmed():
    window = tk.Toplevel(root)
    window.title("Lisa uus film")
    window.geometry("400x350")

    labels = ["Nimi", "Aasta", "Keel", "Režissöör", "Žanr", "Riik"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(window, text=label).grid(row=i, column=0, padx=5, pady=5)

        if label == "Keel":
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM languages")
                languages = [row[0] for row in cursor.fetchall()]
            combobox = ttk.Combobox(window, values=languages)
            combobox.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = combobox
        else:
            entry = tk.Entry(window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[label] = entry

    def submit():
        data = [entries[label].get() for label in labels]
        with sqlite3.connect("filmid.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO filmid (nimi, aasta, keel, rezissoor, zanr, riik) VALUES (?, ?, ?, ?, ?, ?)",
                data
            )
            conn.commit()
        messagebox.showinfo("Edu", "Film edukalt lisatud!")
        window.destroy()

    tk.Button(window, text="Lisa", command=submit).grid(row=len(labels), column=1, pady=10)

def insert_data():
    global entries
    try:
        with sqlite3.connect("filmid.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO filmid (title, director_id, release_year, genre_id, duration, rating, language_id, country_id, description)
                VALUES (?, (SELECT id FROM directors WHERE name=?), ?, (SELECT id FROM genres WHERE name=?), ?, ?, (SELECT id FROM languages WHERE name=?), (SELECT id FROM countries WHERE name=?), ?)
            """, (
                entries["Pealkiri"].get(),
                entries["Režissöör"].get(),
                entries["Aasta"].get(),
                entries["Žanr"].get(),
                entries["Kestus"].get(),
                entries["Reiting"].get(),
                entries["Keel"].get(),
                entries["Riik"].get(),
                entries["Kirjeldus"].get()
            ))
            conn.commit()
            messagebox.showinfo("Edu", "Andmed sisestati edukalt!")
            load_data_from_db()
    except sqlite3.Error as e:
        messagebox.showerror("Viga", f"Andmebaasi viga: {e}")

def lisa_tabel(table, label):
    window = tk.Toplevel(root)
    window.title(f"Lisa {label.lower()}")

    input_frame = tk.Frame(window)
    input_frame.pack(pady=10)
    tk.Label(input_frame, text=label).pack(side=tk.LEFT, padx=5)
    entry = tk.Entry(input_frame)
    entry.pack(side=tk.LEFT, padx=5)
    tk.Button(input_frame, text="Salvesta", command=lambda: insert_tabel(table, entry.get(), window)).pack(side=tk.LEFT, padx=5)

    table_frame = tk.Frame(window)
    table_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(table_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree = ttk.Treeview(table_frame, yscrollcommand=scrollbar.set, columns=("id", "name"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=tree.yview)

    tree.heading("id", text="ID")
    tree.heading("name", text=label)
    tree.column("id", width=50)
    tree.column("name", width=200)

    with sqlite3.connect("filmid.db") as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name FROM {table}")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

def insert_tabel(table, value, window):
    try:
        with sqlite3.connect("filmid.db") as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table} (name) VALUES (?)", (value,))
            conn.commit()
            messagebox.showinfo("Edu", f"{table.capitalize()} lisatud!")
            window.destroy()
            load_data_from_db()
    except sqlite3.Error as e:
        messagebox.showerror("Viga", f"Andmebaasi viga: {e}")

def update_record(record_id, entries, window):
    try:
        with sqlite3.connect("filmid.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE filmid
                SET title=?, 
                    director_id=(SELECT id FROM directors WHERE name=?), 
                    release_year=?, 
                    genre_id=(SELECT id FROM genres WHERE name=?), 
                    duration=?, 
                    rating=?, 
                    language_id=(SELECT id FROM languages WHERE name=?), 
                    country_id=(SELECT id FROM countries WHERE name=?), 
                    description=?
                WHERE id=?
            """, (
                entries["Pealkiri"].get(),
                entries["Režissöör"].get(),
                entries["Aasta"].get(),
                entries["Žanr"].get(),
                entries["Kestus"].get(),
                entries["Reiting"].get(),
                entries["Keel"].get(),
                entries["Riik"].get(),
                entries["Kirjeldus"].get(),
                record_id
            ))
            conn.commit()
            messagebox.showinfo("Salvestamine", "Andmed on edukalt uuendatud!")
            load_data_from_db()
            window.destroy()
    except sqlite3.Error as e:
        messagebox.showerror("Viga", f"Andmebaasi viga: {e}")

def on_update():
    global tree
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")
        return
    values = tree.item(selected_item[0])['values']
    record_id = values[0]  # The first column is the database ID
    open_update_window()

def open_update_window():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Hoiatus", "Vali film, mida muuta!")
        return

    record = tree.item(selected_item)['values']
    update_window = tk.Toplevel(root)
    update_window.title("Muuda andmeid")
    update_window.geometry("400x350")

    labels = ["Pealkiri","Režissöör", "Aasta", "Žanr", "Kestus", "Reiting", "Keel", "Riik", "Kirjeldus"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)

        if label == "Keel":
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM languages")
                languages = [row[0] for row in cursor.fetchall()]
            combobox = ttk.Combobox(update_window, values=languages)
            combobox.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            combobox.set(value)
            entries[label] = combobox
        else:
            entry = tk.Entry(update_window, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            entry.insert(0, value)
            entries[label] = entry

        if label == "Režissöör":
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM didectors")
                directors = [row[0] for row in cursor.fetchall()]
            combobox = ttk.Combobox(update_window, values=directors)
            combobox.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            combobox.set(value)
            entries[label] = combobox
        else:
            entry = tk.Entry(update_window, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            entry.insert(0, value)
            entries[label] = entry

        if label == "Žanr":
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM genres")
                genres = [row[0] for row in cursor.fetchall()]
            combobox = ttk.Combobox(update_window, values=genres)
            combobox.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            combobox.set(value)
            entries[label] = combobox
        else:
            entry = tk.Entry(update_window, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            entry.insert(0, value)
            entries[label] = entry

        if label == "Riik":
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM countries")
                country = [row[0] for row in cursor.fetchall()]
            combobox = ttk.Combobox(update_window, values=country)
            combobox.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            combobox.set(value)
            entries[label] = combobox
        else:
            entry = tk.Entry(update_window, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            value = '' if record[i+1] is None else str(record[i+1])
            entry.insert(0, value)
            entries[label] = entry


    def update_record():
        data = [entries[label].get() for label in labels]
        with sqlite3.connect("filmid.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE filmid SET pealkiri=?, rezissoor=?,aasta=?, zanr=?, kestus=?, reiting=?, keel=?, riik=?, kirjeldus=? WHERE id=?
            """, (*data, record[0]))
            conn.commit()
        messagebox.showinfo("Edu", "Andmed edukalt muudetud!")
        update_window.destroy()
        load_data_from_db()

    tk.Button(update_window, text="Muuda", command=update_record).grid(row=len(labels), column=1, pady=10)

def on_delete():
    global tree
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Valik puudub", "Palun vali kõigepealt rida!")
        return
    values = tree.item(selected_item[0])['values']
    record_id = values[0] 
    confirm = messagebox.askyesno("Kinnita kustutamine", "Kas oled kindel, et soovid selle rea kustutada?")
    if confirm:
        try:
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM filmid WHERE id=?", (record_id,))
                conn.commit()
                messagebox.showinfo("Edukalt kustutatud", "Rida on edukalt kustutatud!")
                load_data_from_db()
        except sqlite3.Error as e:
            messagebox.showerror("Viga", f"Andmebaasi viga: {e}")



search_frame = tk.Frame(root)
search_frame.pack(pady=10)
tk.Label(search_frame, text="Otsi filmi pealkirja järgi:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=10)
tk.Button(search_frame, text="Otsi", command=on_search).pack(side=tk.LEFT)

buttons = [
    ("Lisa andmeid", lisa_andmed),
    ("Uuenda", on_update),
    ("Kustuta", on_delete),
    ("Lisa keel", lambda: lisa_tabel("languages", "Keel")),
    ("Lisa riik", lambda: lisa_tabel("countries", "Riik")),
    ("Lisa žanr", lambda: lisa_tabel("genres", "Žanr")),
    ("Lisa režissöör", lambda: lisa_tabel("directors", "Režissöör"))
]
for text, command in buttons:
    tk.Button(search_frame, text=text, command=command).pack(side=tk.LEFT, padx=10)

frame = tk.Frame(root)
frame.pack(pady=20, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree = ttk.Treeview(frame, yscrollcommand=scrollbar.set, columns=(
    "id", "title", "director_id", "release_year", "genre_id", "duration", "rating", "language_id", "country_id", "description"
), show="headings")
tree.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=tree.yview)

headers = {
    "id": "ID",
    "title": "Pealkiri",
    "director_id": "Režissöör",
    "release_year": "Aasta",
    "genre_id": "Žanr",
    "duration": "Kestus",
    "rating": "Reiting",
    "language_id": "Keel",
    "country_id": "Riik",
    "description": "Kirjeldus"
}
for col, text in headers.items():
    tree.heading(col, text=text)
tree.column("id", width=50)
tree.column("title", width=150)
tree.column("director_id", width=100)
tree.column("release_year", width=60)
tree.column("genre_id", width=100)
tree.column("duration", width=60)
tree.column("rating", width=60)
tree.column("language_id", width=80)
tree.column("country_id", width=80)
tree.column("description", width=200)

load_data_from_db()
root.mainloop()



import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

root = tk.Tk()
root.title("Filmid")
entries = {}
tree = None
search_entry = None

def create_db():
    with sqlite3.connect("filmid.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS filmid (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                director_id INTEGER,
                release_year INTEGER,
                genre_id INTEGER,
                duration INTEGER,
                rating REAL,
                language_id INTEGER,
                country_id INTEGER,
                description TEXT,
                FOREIGN KEY (director_id) REFERENCES directors(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id),
                FOREIGN KEY (language_id) REFERENCES languages(id),
                FOREIGN KEY (country_id) REFERENCES countries(id)
            )
        """)
        conn.commit()

def load_data_from_db():
    global tree
    tree.delete(*tree.get_children())
    with sqlite3.connect("filmid.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.id, f.title, d.name, f.release_year, g.name, f.duration, f.rating, l.name, c.name, f.description
            FROM filmid f
            LEFT JOIN directors d ON f.director_id = d.id
            LEFT JOIN genres g ON f.genre_id = g.id
            LEFT JOIN languages l ON f.language_id = l.id
            LEFT JOIN countries c ON f.country_id = c.id
        """)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

def open_update_window():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Hoiatus", "Vali film, mida muuta!")
        return

    record = tree.item(selected_item)['values']
    record_id = record[0]

    update_window = tk.Toplevel(root)
    update_window.title("Muuda andmeid")

    labels = ["Pealkiri", "Režissöör", "Aasta", "Žanr", "Kestus", "Reiting", "Keel", "Riik", "Kirjeldus"]
    fields = {}
    for i, label in enumerate(labels):
        tk.Label(update_window, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
        if label in ["Režissöör", "Žanr", "Keel", "Riik"]:
            with sqlite3.connect("filmid.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT name FROM {label.lower() + 's'}" if label != "Riik" else "SELECT name FROM countries")
                options = [row[0] for row in cursor.fetchall()]
            combo = ttk.Combobox(update_window, values=options)
            combo.set(record[i+1])
            combo.grid(row=i, column=1, padx=5, pady=5)
            fields[label] = combo
        else:
            entry = tk.Entry(update_window)
            entry.insert(0, record[i+1])
            entry.grid(row=i, column=1, padx=5, pady=5)
            fields[label] = entry

    def update_record():
        data = [
            fields["Pealkiri"].get(),
            fields["Režissöör"].get(),
            fields["Aasta"].get(),
            fields["Žanr"].get(),
            fields["Kestus"].get(),
            fields["Reiting"].get(),
            fields["Keel"].get(),
            fields["Riik"].get(),
            fields["Kirjeldus"].get(),
        ]
        with sqlite3.connect("filmid.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE filmid SET
                    title=?,
                    director_id=(SELECT id FROM directors WHERE name=?),
                    release_year=?,
                    genre_id=(SELECT id FROM genres WHERE name=?),
                    duration=?,
                    rating=?,
                    language_id=(SELECT id FROM languages WHERE name=?),
                    country_id=(SELECT id FROM countries WHERE name=?),
                    description=?
                WHERE id=?
            """, (*data, record_id))
            conn.commit()
        messagebox.showinfo("Edu", "Andmed edukalt muudetud!")
        update_window.destroy()
        load_data_from_db()

    tk.Button(update_window, text="Muuda", command=update_record).grid(row=len(labels), column=1, pady=10)

def setup_main_ui():
    global tree, search_entry
    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Otsi", command=load_data_from_db).pack(side=tk.LEFT)

    tree = ttk.Treeview(root, columns=(1,2,3,4,5,6,7,8,9,10), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)
    headers = ["ID", "Pealkiri", "Režissöör", "Aasta", "Žanr", "Kestus", "Reiting", "Keel", "Riik", "Kirjeldus"]
    for i, header in enumerate(headers, 1):
        tree.heading(i, text=header)

    tk.Button(root, text="Muuda valikut", command=open_update_window).pack(pady=5)

create_db()
setup_main_ui()
load_data_from_db()

root.mainloop()
