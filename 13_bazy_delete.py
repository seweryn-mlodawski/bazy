# ============================================
# ex_06_delete.py - POPRAWIONY KOD
# ============================================
# Usuwanie danych z bazy SQLite
# Delete with conditions, delete all

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Nawiąż połączenie z bazą danych SQLite
    :param db_file: ścieżka do pliku bazy
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(f"Błąd połączenia: {e}")
    return conn


def create_tables_and_data(conn):
    """
    Stwórz tabele i dodaj przykładowe dane
    """
    create_projects_sql = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        nazwa TEXT NOT NULL,
        start_date TEXT,
        end_date TEXT
    );
    """
    
    create_tasks_sql = """
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
        cur.execute(create_projects_sql)
        cur.execute(create_tasks_sql)
        conn.commit()
        
        # Dodaj dane
        projects = [
            (1, "Projekt 1", "2024-01-01", "2024-06-30"),
            (2, "Projekt 2", "2024-02-01", "2024-08-31"),
            (3, "Projekt 3", "2024-03-01", "2024-12-31"),
        ]
        
        tasks = [
            (1, 1, "Zadanie 1", "Opis 1", "W trakcie", "2024-01-01", "2024-02-01"),
            (2, 1, "Zadanie 2", "Opis 2", "Ukończone", "2024-02-01", "2024-03-01"),
            (3, 2, "Zadanie 3", "Opis 3", "W trakcie", "2024-02-01", "2024-04-01"),
            (4, 2, "Zadanie 4", "Opis 4", "Oczekujące", "2024-03-01", "2024-05-01"),
            (5, 3, "Zadanie 5", "Opis 5", "W trakcie", "2024-03-01", "2024-06-01"),
        ]
        
        cur.executemany("INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?)", projects)
        cur.executemany("INSERT OR IGNORE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", tasks)
        conn.commit()
        
        print("✓ Tabele i dane utworzone\n")
        
    except Error as e:
        print(f"Błąd: {e}")


def show_all_tasks(conn):
    """
    Wyświetl wszystkie zadania
    """
    sql = "SELECT * FROM tasks"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"Błąd: {e}")
        return []


def delete_where(conn, table, **kwargs):
    """
    Usuń rekordy ze spełniającą warunek(i)
    
    :param conn: Connection to the SQLite database
    :param table: nazwa tabeli
    :param kwargs: słownik atrybutów i wartości (warunki DELETE)
    :return: None
    
    LOGIKA:
    -------
    1. Budujemy warunki WHERE z kwargs
       - kwargs = {"id": 3} → "id=?"
       - kwargs = {"id": 3, "status": "Ukończone"} → "id=?, status=?"
    
    2. Łączymy warunki za pomocą AND
       - "id=?" AND "status=?"
    
    3. Zbieramy wartości do listy wartości
       - values = (3, "Ukończone")
    
    4. Wykonujemy DELETE z warunkami
       - DELETE FROM tasks WHERE id=? AND status=?
    
    PRZYKŁAD:
    ---------
    delete_where(conn, "tasks", id=3)
    # Usuwa wiersz gdzie id=3
    
    delete_where(conn, "tasks", id=3, status="Ukończone")
    # Usuwa wiersz gdzie id=3 AND status="Ukończone"
    """
    
    # KROK 1: Budowanie warunków
    qs = []  # Collect conditions like ["id=?", "status=?"]
    values = tuple()  # Collect values like (3, "Ukończone")
    
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    
    # KROK 2: Łączenie warunków za pomocą AND
    q = " AND ".join(qs)
    
    # KROK 3: Budowanie SQL
    sql = f'DELETE FROM {table} WHERE {q}'
    
    # KROK 4: Wykonanie
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print(f"✓ Deleted where {q}")
    except Error as e:
        print(f"✗ Błąd: {e}")


def delete_all(conn, table):
    """
    Usuń WSZYSTKIE rekordy z tabeli
    
    :param conn: Connection to the SQLite database
    :param table: nazwa tabeli
    :return: None
    
    LOGIKA:
    -------
    1. Brak warunku WHERE - usuwa WSZYSTKIE rekordy!
    2. UWAGA: Żaden warunek != WSZYSCY będą usunięci
    
    PRZYKŁAD:
    ---------
    delete_all(conn, "tasks")
    # Usuwa WSZYSTKIE zadania!
    
    WARNING:
    --------
    Ta funkcja jest niebezpieczna - usuwa wszystkie dane!
    Zawsze upewnij się że na pewno chcesz usunąć wszystko.
    """
    
    # KROK 1: Budowanie SQL BEZ warunku WHERE
    sql = f'DELETE FROM {table}'
    
    # KROK 2: Wykonanie
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print(f"✓ Deleted ALL from {table}")
    except Error as e:
        print(f"✗ Błąd: {e}")


if __name__ == "__main__":
    print("="*70)
    print("DELETE - USUWANIE DANYCH Z BAZY")
    print("="*70 + "\n")
    
    # Połączenie
    conn = create_connection("delete_demo.db")
    
    if conn is not None:
        # Przygotowanie
        create_tables_and_data(conn)
        
        # ============ PRZED USUNIĘCIEM ============
        print("STAN POCZĄTKOWY - wszystkie zadania:")
        print("-" * 70)
        tasks = show_all_tasks(conn)
        for task in tasks:
            print(f"  ID: {task[0]}, Nazwa: {task[2]}, Status: {task[4]}")
        print()
        
        # ============ USUNIĘCIE Z WARUNKIEM ============
        print("OPERACJA 1: delete_where(conn, 'tasks', id=3)")
        print("-" * 70)
        print("Usuwamy zadanie o ID=3\n")
        delete_where(conn, "tasks", id=3)
        
        print("\nStan po pierwszym DELETE:")
        print("-" * 70)
        tasks = show_all_tasks(conn)
        for task in tasks:
            print(f"  ID: {task[0]}, Nazwa: {task[2]}, Status: {task[4]}")
        print()
        
        # ============ USUNIĘCIE WSZYSTKICH ============
        print("OPERACJA 2: delete_all(conn, 'tasks')")
        print("-" * 70)
        print("UWAGA: To usunie WSZYSTKIE zadania!\n")
        delete_all(conn, "tasks")
        
        print("\nStan po usunięciu WSZYSTKICH:")
        print("-" * 70)
        tasks = show_all_tasks(conn)
        if tasks:
            for task in tasks:
                print(f"  ID: {task[0]}, Nazwa: {task[2]}")
        else:
            print("  Brak zadań - tabela jest pusta!")
        
        conn.close()
        
        print("\n" + "="*70)
        print("✓ Program zakończony!")
        print("="*70)


# ============================================
# PODSUMOWANIE - LOGIKA DZIAŁANIA
# ============================================
"""
DELETE_WHERE - USUWANIE Z WARUNKAMI:
====================================

Przykład: delete_where(conn, "tasks", id=3, status="Ukończone")

Krok 1: Budowanie warunków
    kwargs = {"id": 3, "status": "Ukończone"}
    qs = []
    values = ()
    
    Iteracja 1: k="id", v=3
        qs.append("id=?")         → qs = ["id=?"]
        values += (3,)            → values = (3,)
    
    Iteracja 2: k="status", v="Ukończone"
        qs.append("status=?")     → qs = ["id=?", "status=?"]
        values += ("Ukończone",)  → values = (3, "Ukończone")

Krok 2: Łączenie warunków
    q = " AND ".join(qs)
    q = "id=? AND status=?"

Krok 3: Budowanie SQL
    sql = "DELETE FROM tasks WHERE id=? AND status=?"

Krok 4: Wykonanie
    cur.execute(sql, values)
    # Podstawia wartości: DELETE FROM tasks WHERE id=3 AND status='Ukończone'
    conn.commit()
    # Zapisuje zmiany


DELETE_ALL - USUWANIE WSZYSTKICH:
==================================

Przykład: delete_all(conn, "tasks")

Krok 1: Budowanie SQL
    sql = "DELETE FROM tasks"
    (BRAK WHERE - usuwa WSZYSTKIE!)

Krok 2: Wykonanie
    cur.execute(sql)
    conn.commit()
    
UWAGA: Ta operacja jest IRREVERSIBLE - nie można cofnąć!


PORÓWNANIE:
===========

delete_where(conn, "tasks", id=3)
  Usuwa: tylko zadanie o ID=3
  SQL: DELETE FROM tasks WHERE id=3
  Bezpieczne: ✓

delete_all(conn, "tasks")
  Usuwa: WSZYSTKIE zadania
  SQL: DELETE FROM tasks
  Bezpieczne: ✗ (usuwa wszystko!)
"""
