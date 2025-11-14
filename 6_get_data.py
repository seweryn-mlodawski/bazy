# ============================================
# Ćwiczenie: Pobieranie danych z bazy SQLite
# ============================================
# Ten plik skupia się na praktyce pobierania danych z bazy
# Uczymy się SELECT, fetchall(), fetchone() i różnych sposobów
# wyświetlania danych pobranych z bazy

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Nawiąż połączenie z bazą danych SQLite
    :param db_file: ścieżka do pliku bazy danych
    :return: obiekt Connection
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"✓ Połączenie z bazą '{db_file}' nawiązane\n")
        return conn
    except Error as e:
        print(f"✗ Błąd połączenia: {e}")
        return None


def create_tables(conn):
    """
    Stwórz przykładowe tabele do ćwiczeń
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
        print("✓ Tabele utworzone")
    except Error as e:
        print(f"✗ Błąd tworzenia tabel: {e}")


def add_sample_data(conn):
    """
    Dodaj przykładowe dane do tabel
    """
    projects = [
        (1, "Nauka SQL", "2024-01-01", "2024-12-31"),
        (2, "Projekt Python", "2024-02-01", "2024-11-30"),
        (3, "Aplikacja webowa", "2024-03-01", "2024-10-31")
    ]
    
    tasks = [
        (1, 1, "Zainstalować SQLite", "Pobrać i zainstalować", "Ukończone", "2024-01-01", "2024-01-02"),
        (2, 1, "Nauczyć się SELECT", "Poznać podstawy SELECT", "W trakcie", "2024-01-03", "2024-01-10"),
        (3, 2, "Napisać kod", "Stworzyć główny plik", "Rozpoczęte", "2024-02-01", "2024-06-30"),
        (4, 2, "Testy jednostkowe", "Przygotować testy", "Oczekujące", "2024-07-01", "2024-08-31"),
        (5, 3, "Design UI", "Zaprojektować interfejs", "W trakcie", "2024-03-01", "2024-05-31")
    ]
    
    try:
        cur = conn.cursor()
        
        # Wstaw projekty
        cur.executemany("INSERT OR IGNORE INTO projects VALUES (?, ?, ?, ?)", projects)
        
        # Wstaw zadania
        cur.executemany("INSERT OR IGNORE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", tasks)
        
        conn.commit()
        print("✓ Przykładowe dane dodane\n")
    except Error as e:
        print(f"✗ Błąd dodawania danych: {e}")


def select_all_projects(conn):
    """
    ĆWICZENIE 1: Pobierz wszystkie projekty
    Pokazuje podstawowe użycie SELECT * i fetchall()
    """
    print("="*70)
    print("ĆWICZENIE 1: SELECT * - Pobieranie wszystkich projektów")
    print("="*70)
    
    # Zapytanie SQL
    sql = "SELECT * FROM projects;"
    
    try:
        # Tworzenie kursora
        cur = conn.cursor()
        
        # Wykonanie zapytania
        cur.execute(sql)
        
        # Pobranie WSZYSTKICH wyników za pomocą fetchall()
        projects = cur.fetchall()
        
        print(f"\nZnaleziono {len(projects)} projektów:\n")
        
        # Wyświetlenie wyników
        for project in projects:
            print(f"ID: {project[0]}, Nazwa: {project[1]}, Start: {project[2]}, Koniec: {project[3]}")
        
        return projects
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_all_tasks(conn):
    """
    ĆWICZENIE 2: Pobierz wszystkie zadania
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 2: Pobieranie wszystkich zadań")
    print("="*70)
    
    sql = "SELECT * FROM tasks;"
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        tasks = cur.fetchall()
        
        print(f"\nZnaleziono {len(tasks)} zadań:\n")
        
        for task in tasks:
            print(f"ID: {task[0]} | Projekt ID: {task[1]} | Nazwa: {task[2]} | Status: {task[4]}")
        
        return tasks
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_specific_columns(conn):
    """
    ĆWICZENIE 3: Pobierz tylko wybrane kolumny
    Pokazuje SELECT z konkretnymi nazwami kolumn
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 3: SELECT konkretnych kolumn")
    print("="*70)
    
    # Pobieramy tylko nazwę i status zadań
    sql = "SELECT nazwa, status FROM tasks;"
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        
        print("\nNazwa zadania | Status")
        print("-" * 50)
        
        for row in results:
            print(f"{row[0]:30} | {row[1]}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_with_where(conn):
    """
    ĆWICZENIE 4: SELECT z warunkiem WHERE
    Pobiera tylko zadania o konkretnym statusie
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 4: SELECT z warunkiem WHERE")
    print("="*70)
    
    # Pobierz tylko zadania "W trakcie"
    sql = "SELECT * FROM tasks WHERE status = ?;"
    
    try:
        cur = conn.cursor()
        cur.execute(sql, ("W trakcie",))
        results = cur.fetchall()
        
        print("\nZadania ze statusem 'W trakcie':\n")
        
        for task in results:
            print(f"ID: {task[0]} | Nazwa: {task[2]} | Status: {task[4]}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_with_join(conn):
    """
    ĆWICZENIE 5: SELECT z JOIN
    Łączy dane z dwóch tabel (projects i tasks)
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 5: SELECT z JOIN - łączenie tabel")
    print("="*70)
    
    sql = """
    SELECT projects.nazwa AS projekt, tasks.nazwa AS zadanie, tasks.status
    FROM tasks
    INNER JOIN projects ON tasks.project_id = projects.id;
    """
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        
        print("\nProjekt | Zadanie | Status")
        print("-" * 70)
        
        for row in results:
            print(f"{row[0]:25} | {row[1]:25} | {row[2]}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_with_count(conn):
    """
    ĆWICZENIE 6: SELECT COUNT() - zliczanie rekordów
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 6: COUNT() - zliczanie rekordów")
    print("="*70)
    
    # Zlicz ile jest projektów
    sql = "SELECT COUNT(*) FROM projects;"
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        
        # fetchone() zwraca JEDEN wiersz wyniku (w tym przypadku liczbę)
        result = cur.fetchone()
        
        print(f"\nLiczba projektów w bazie: {result[0]}")
        
        return result[0]
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_with_group_by(conn):
    """
    ĆWICZENIE 7: GROUP BY - grupowanie wyników
    Zlicz ile zadań jest w każdym projekcie
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 7: GROUP BY - grupowanie i zliczanie")
    print("="*70)
    
    sql = """
    SELECT projects.nazwa, COUNT(tasks.id) AS liczba_zadan
    FROM projects
    LEFT JOIN tasks ON projects.id = tasks.project_id
    GROUP BY projects.nazwa;
    """
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        
        print("\nProjekt | Liczba zadań")
        print("-" * 40)
        
        for row in results:
            print(f"{row[0]:30} | {row[1]}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_with_order_by(conn):
    """
    ĆWICZENIE 8: ORDER BY - sortowanie wyników
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 8: ORDER BY - sortowanie")
    print("="*70)
    
    # Sortuj projekty według daty rozpoczęcia (malejąco)
    sql = "SELECT * FROM projects ORDER BY start_date DESC;"
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        
        print("\nProjekty posortowane według daty rozpoczęcia (od najnowszych):\n")
        
        for project in results:
            print(f"{project[1]:30} | Start: {project[2]}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_with_limit(conn):
    """
    ĆWICZENIE 9: LIMIT - ograniczanie liczby wyników
    """
    print("\n" + "="*70)
    print("ĆWICZENIE 9: LIMIT - ograniczanie wyników")
    print("="*70)
    
    # Pobierz tylko 3 pierwsze zadania
    sql = "SELECT * FROM tasks LIMIT 3;"
    
    try:
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        
        print("\nPierwsze 3 zadania:\n")
        
        for task in results:
            print(f"ID: {task[0]} | {task[2]}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_tasks_by_project(conn, project_id):
    """
    ĆWICZENIE 10: Funkcja pobierająca zadania dla konkretnego projektu
    Pokazuje praktyczne zastosowanie parametryzowanych zapytań
    """
    print("\n" + "="*70)
    print(f"ĆWICZENIE 10: Zadania dla projektu o ID {project_id}")
    print("="*70)
    
    sql = """
    SELECT tasks.*, projects.nazwa AS projekt_nazwa
    FROM tasks
    INNER JOIN projects ON tasks.project_id = projects.id
    WHERE tasks.project_id = ?;
    """
    
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        results = cur.fetchall()
        
        if results:
            print(f"\nProjekt: {results[0][7]}")
            print("Zadania:")
            print("-" * 70)
            
            for task in results:
                print(f"  • {task[2]} ({task[4]})")
        else:
            print(f"\nBrak zadań dla projektu o ID {project_id}")
        
        return results
        
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ĆWICZENIA: POBIERANIE DANYCH Z BAZY SQLITE")
    print("="*70)
    print()
    
    db_file = "fetch_practice.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Przygotowanie bazy
        create_tables(conn)
        add_sample_data(conn)
        
        # Wykonaj wszystkie ćwiczenia
        select_all_projects(conn)
        select_all_tasks(conn)
        select_specific_columns(conn)
        select_with_where(conn)
        select_with_join(conn)
        select_with_count(conn)
        select_with_group_by(conn)
        select_with_order_by(conn)
        select_with_limit(conn)
        select_tasks_by_project(conn, 1)
        
        # Zamknij połączenie
        conn.close()
        
        print("\n" + "="*70)
        print("✓ Wszystkie ćwiczenia zakończone!")
        print("="*70)
