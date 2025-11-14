# ============================================
# Działający kod - fetchall() vs fetchone()
# ============================================
# Praktyczna demonstracja tego, co pokazano w iPython
# fetchall() - pobiera WSZYSTKIE wyniki naraz
# fetchone() - pobiera po JEDNYM wyniku za każdym razem

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Nawiąż połączenie z bazą danych"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_tables_and_data(conn):
    """Stwórz tabele i dodaj przykładowe dane"""
    
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
        
        # Dodaj projekty
        projects = [
            (5, "Projekt 5", "2020-05-01", "2020-05-31"),
            (6, "Projekt 6", "2020-06-01", "2020-06-30"),
            (7, "Projekt 7", "2020-07-01", "2020-07-31"),
        ]
        
        cur.executemany("INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?)", projects)
        
        # Dodaj zadania - dokładnie jak w przykładzie
        tasks = [
            (1, 5, 'Czasowniki regularne', 'Zapamiętaj czasowniki ze strony 30', 'started', '2020-05-11 12:00:00', '2020-05-11 15:00:00'),
            (2, 6, 'Czasowniki regularne', 'Zapamiętaj czasowniki ze strony 30', 'started', '2020-05-11 12:00:00', '2020-05-11 15:00:00'),
            (3, 7, 'Czasowniki regularne', 'Zapamiętaj czasowniki ze strony 30', 'started', '2020-05-11 12:00:00', '2020-05-11 15:00:00'),
        ]
        
        cur.executemany("INSERT OR IGNORE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", tasks)
        conn.commit()
        
        print("✓ Tabele i dane utworzone\n")
        
    except Error as e:
        print(f"Błąd: {e}")


def example_fetchall(conn):
    """
    PRZYKŁAD 1: fetchall()
    Pobiera WSZYSTKIE wyniki za jednym razem i zwraca listę
    """
    print("="*70)
    print("PRZYKŁAD 1: fetchall() - POBIERZ WSZYSTKIE WYNIKI NARAZ")
    print("="*70)
    
    print("\nKod:")
    print("""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    """)
    
    print("\nWykonanie:\n")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    
    print(f"rows = {rows}\n")
    print(f"Typ wyniku: {type(rows)}")
    print(f"Liczba wyników: {len(rows)}\n")
    
    print("Iteracja po wynikach:\n")
    for row in rows:
        print(f"  {row}")
    
    return rows


def example_fetchone(conn):
    """
    PRZYKŁAD 2: fetchone()
    Pobiera po JEDNYM wyniku za każdym razem
    Kursor "pamiętał" gdzie poprzednio skończył
    """
    print("\n" + "="*70)
    print("PRZYKŁAD 2: fetchone() - POBIERZ PO JEDNYM WYNIKU")
    print("="*70)
    
    print("\nKod:")
    print("""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    
    # Pierwszy fetchone()
    result1 = cur.fetchone()
    # Drugi fetchone() - zwraca NASTĘPNY wiersz
    result2 = cur.fetchone()
    # Trzeci fetchone()
    result3 = cur.fetchone()
    # Czwarty fetchone() - nie ma więcej wierszy
    result4 = cur.fetchone()
    """)
    
    print("\nWykonanie:\n")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    
    # Pobranie wyników jeden po jednym
    print("Pierwszy fetchone():")
    result1 = cur.fetchone()
    print(f"  {result1}\n")
    
    print("Drugi fetchone():")
    result2 = cur.fetchone()
    print(f"  {result2}\n")
    
    print("Trzeci fetchone():")
    result3 = cur.fetchone()
    print(f"  {result3}\n")
    
    print("Czwarty fetchone() - brak więcej wierszy:")
    result4 = cur.fetchone()
    print(f"  {result4}\n")


def example_select_specific(conn):
    """
    PRZYKŁAD 3: SELECT z WHERE - Pobierz zadania dla konkretnego projektu
    """
    print("\n" + "="*70)
    print("PRZYKŁAD 3: SELECT z WHERE - Pobierz zadania dla projektu")
    print("="*70)
    
    project_id = 5
    
    print(f"\nZadanie: Pobierz wszystkie zadania dla projektu o ID {project_id}\n")
    
    print("Kod:")
    print(f"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE project_id = ?", ({project_id},))
    rows = cur.fetchall()
    
    for row in rows:
        print(row)
    """)
    
    print(f"\nWykonanie:\n")
    print(f"--- ZADANIA DLA PROJEKTU O ID {project_id} ---\n")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    rows = cur.fetchall()
    
    for row in rows:
        print(f"  {row}")
    
    return rows


def example_comparison_table(conn):
    """
    PORÓWNANIE: fetchall() vs fetchone()
    """
    print("\n" + "="*70)
    print("PORÓWNANIE: fetchall() vs fetchone()")
    print("="*70)
    
    print("\n┌─────────────────┬──────────────────────┬──────────────────────┐")
    print("│ METODA          │ fetchall()           │ fetchone()           │")
    print("├─────────────────┼──────────────────────┼──────────────────────┤")
    print("│ Co zwraca       │ Lista wszystkich     │ Jeden wiersz (tuple) │")
    print("│                 │ wierszy (list)       │ lub None             │")
    print("├─────────────────┼──────────────────────┼──────────────────────┤")
    print("│ Liczba wierszy  │ Wszystkie naraz      │ Po jednym            │")
    print("├─────────────────┼──────────────────────┼──────────────────────┤")
    print("│ Kiedy używać    │ Gdy chcesz           │ Gdy chcesz po        │")
    print("│                 │ wszystkie wyniki     │ jednym wyniku        │")
    print("│                 │ i iterować po nich   │ (np. ID istniejące?) │")
    print("├─────────────────┼──────────────────────┼──────────────────────┤")
    print("│ Pamięć          │ Więcej (wszystko     │ Mniej (jeden na raz) │")
    print("│                 │ na raz)              │                      │")
    print("└─────────────────┴──────────────────────┴──────────────────────┘")


def count_tasks(conn):
    """
    PRZYKŁAD 4: COUNT() - Zlicz zadania
    """
    print("\n" + "="*70)
    print("PRZYKŁAD 4: COUNT() - Zlicz liczbę zadań")
    print("="*70)
    
    print("\nKod:")
    print("""
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()
    print(f"Liczba zadań: {count[0]}")
    """)
    
    print("\nWykonanie:\n")
    
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks")
    count = cur.fetchone()
    
    print(f"  Wynik fetchone(): {count}")
    print(f"  Liczba zadań: {count[0]}")


if __name__ == "__main__":
    db_file = "tasks_demo.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Przygotowanie danych
        create_tables_and_data(conn)
        
        # Przykłady
        example_fetchall(conn)
        example_fetchone(conn)
        example_select_specific(conn)
        example_comparison_table(conn)
        count_tasks(conn)
        
        conn.close()
        
        print("\n" + "="*70)
        print("✓ Wszystkie przykłady wykonane!")
        print("="*70)
