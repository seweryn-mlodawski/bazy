# ============================================
# Pobieranie danych z bazy SQLite
# ============================================
# Program na podstawie materiałów z PDFs
# Pokazuje praktyczną implementację pobierania danych z bazy

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Utwórz połączenie z bazą danych SQLite
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def select_all_projects(conn):
    """
    Pobierz wszystkie projekty z bazy
    - tworzenie kursora
    - execute() - wykonanie zapytania
    - fetchall() - pobranie wszystkich wyników
    """
    sql = "SELECT * FROM projects"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        
        print("\n--- WSZYSTKIE PROJEKTY ---")
        for row in rows:
            print(row)
            
        return rows
    except Error as e:
        print(e)


def select_all_tasks(conn):
    """
    Pobierz wszystkie zadania z bazy
    """
    sql = "SELECT * FROM tasks"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        
        print("\n--- WSZYSTKIE ZADANIA ---")
        for row in rows:
            print(row)
            
        return rows
    except Error as e:
        print(e)


def select_project_by_id(conn, project_id):
    """
    Pobierz projekt o danym ID
    - SELECT z WHERE (warunkiem)
    - Execute z parametrem
    """
    sql = "SELECT * FROM projects WHERE id=?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        row = cur.fetchone()
        
        if row:
            print(f"\n--- PROJEKT O ID {project_id} ---")
            print(row)
        else:
            print(f"Nie znaleziono projektu o ID {project_id}")
            
        return row
    except Error as e:
        print(e)


def select_tasks_by_project(conn, project_id):
    """
    Pobierz wszystkie zadania dla danego projektu
    """
    sql = "SELECT * FROM tasks WHERE project_id=?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        rows = cur.fetchall()
        
        print(f"\n--- ZADANIA DLA PROJEKTU ID {project_id} ---")
        for row in rows:
            print(row)
            
        return rows
    except Error as e:
        print(e)


def select_by_status(conn, status):
    """
    Pobierz zadania o danym statusie
    """
    sql = "SELECT * FROM tasks WHERE status=?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (status,))
        rows = cur.fetchall()
        
        print(f"\n--- ZADANIA ZE STATUSEM '{status}' ---")
        for row in rows:
            print(row)
            
        return rows
    except Error as e:
        print(e)


def count_tasks(conn):
    """
    Zlicz liczbę zadań w bazie
    - COUNT(*) agregacja
    - fetchone() - pobranie jednego wyniku
    """
    sql = "SELECT COUNT(*) FROM tasks"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        
        print(f"\n--- LICZBA ZADAŃ ---")
        print(f"Łącznie zadań: {result[0]}")
        
        return result[0]
    except Error as e:
        print(e)


def count_projects(conn):
    """
    Zlicz liczbę projektów w bazie
    """
    sql = "SELECT COUNT(*) FROM projects"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        
        print(f"\n--- LICZBA PROJEKTÓW ---")
        print(f"Łącznie projektów: {result[0]}")
        
        return result[0]
    except Error as e:
        print(e)


def create_sample_data(conn):
    """
    Dodaj przykładowe dane do bazy
    """
    # Dane projektów
    projects = [
        (1, "Projekt A", "2024-01-01", "2024-06-30"),
        (2, "Projekt B", "2024-02-01", "2024-08-31"),
        (3, "Projekt C", "2024-03-01", "2024-12-31")
    ]
    
    # Dane zadań
    tasks = [
        (1, 1, "Zadanie 1", "Opis zadania 1", "W trakcie", "2024-01-01", "2024-02-01"),
        (2, 1, "Zadanie 2", "Opis zadania 2", "Ukończone", "2024-02-01", "2024-03-01"),
        (3, 2, "Zadanie 3", "Opis zadania 3", "W trakcie", "2024-02-01", "2024-04-01"),
        (4, 3, "Zadanie 4", "Opis zadania 4", "Oczekujące", "2024-03-01", "2024-05-01"),
    ]
    
    try:
        cur = conn.cursor()
        
        # Wstaw projekty
        cur.executemany("INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?)", projects)
        
        # Wstaw zadania
        cur.executemany("INSERT OR IGNORE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", tasks)
        
        conn.commit()
        print("✓ Dane dodane do bazy")
        
    except Error as e:
        print(e)


def create_tables(conn):
    """
    Stwórz tabele w bazie
    """
    create_projects_table = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        nazwa TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT
    );
    """
    
    create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL,
        nazwa VARCHAR(250) NOT NULL,
        opis TEXT,
        status VARCHAR(15) NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """
    
    try:
        cur = conn.cursor()
        cur.execute(create_projects_table)
        cur.execute(create_tasks_table)
        conn.commit()
        print("✓ Tabele utworzone")
    except Error as e:
        print(e)


if __name__ == "__main__":
    db_file = "read_practice.db"
    
    # Połączenie z bazą
    conn = create_connection(db_file)
    
    if conn is not None:
        # Tworzenie tabel
        create_tables(conn)
        
        # Dodawanie danych
        create_sample_data(conn)
        
        # ========== POBIERANIE DANYCH ==========
        print("\n" + "="*50)
        print("POBIERANIE DANYCH Z BAZY")
        print("="*50)
        
        # Pobierz wszystkie projekty
        select_all_projects(conn)
        
        # Pobierz wszystkie zadania
        select_all_tasks(conn)
        
        # Pobierz projekt o ID 1
        select_project_by_id(conn, 1)
        
        # Pobierz zadania dla projektu 1
        select_tasks_by_project(conn, 1)
        
        # Pobierz zadania ze statusem "W trakcie"
        select_by_status(conn, "W trakcie")
        
        # Zlicz zadania
        count_tasks(conn)
        
        # Zlicz projekty
        count_projects(conn)
        
        # Zamknij połączenie
        conn.close()
        print("\n✓ Operacje zakończone")
