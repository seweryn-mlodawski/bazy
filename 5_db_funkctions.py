# ============================================
# Funkcje do zarządzania bazą danych
# ============================================
# Zaawansowany przykład z funkcjami do wstawiania projektów i zadań
# Kursor jest teraz ukryty wewnątrz funkcji - czystszy kod!

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Nawiąz połączenie z bazą danych SQLite
    :param db_file: ścieżka do pliku bazy danych
    :return: obiekt Connection
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"✓ Połączenie z bazą '{db_file}' nawiązane")
        return conn
    except Error as e:
        print(f"✗ Błąd połączenia: {e}")
        return None


def add_project(conn, project):
    """
    Dodaj nowy projekt do tabeli projects
    :param conn: obiekt Connection
    :param project: krotka (nazwa, start_date, end_date)
    :return: ID nowo dodanego projektu
    """
    sql = '''INSERT INTO projects(nazwa, start_date, end_date)
             VALUES(?, ?, ?)'''
    try:
        cur = conn.cursor()
        cur.execute(sql, project)
        conn.commit()
        print(f"✓ Projekt '{project[0]}' dodany z ID: {cur.lastrowid}")
        return cur.lastrowid
    except Error as e:
        print(f"✗ Błąd dodawania projektu: {e}")
        return None


def add_task(conn, task):
    """
    Dodaj nowe zadanie do tabeli tasks
    :param conn: obiekt Connection
    :param task: krotka (project_id, nazwa, opis, status, start_date, end_date)
    :return: ID nowo dodanego zadania
    """
    sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date)
             VALUES(?, ?, ?, ?, ?, ?)'''
    try:
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        print(f"✓ Zadanie '{task[1]}' dodane z ID: {cur.lastrowid}")
        return cur.lastrowid
    except Error as e:
        print(f"✗ Błąd dodawania zadania: {e}")
        return None


def get_all_projects(conn):
    """
    Pobierz wszystkie projekty
    :param conn: obiekt Connection
    :return: lista projektów
    """
    sql = 'SELECT * FROM projects'
    try:
        cur = conn.cursor()
        cur.execute(sql)
        projects = cur.fetchall()
        return projects
    except Error as e:
        print(f"✗ Błąd pobierania projektów: {e}")
        return None


def get_all_tasks(conn):
    """
    Pobierz wszystkie zadania
    :param conn: obiekt Connection
    :return: lista zadań
    """
    sql = 'SELECT * FROM tasks'
    try:
        cur = conn.cursor()
        cur.execute(sql)
        tasks = cur.fetchall()
        return tasks
    except Error as e:
        print(f"✗ Błąd pobierania zadań: {e}")
        return None


def get_tasks_by_project(conn, project_id):
    """
    Pobierz wszystkie zadania dla danego projektu
    :param conn: obiekt Connection
    :param project_id: ID projektu
    :return: lista zadań należących do projektu
    """
    sql = 'SELECT * FROM tasks WHERE project_id = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        tasks = cur.fetchall()
        return tasks
    except Error as e:
        print(f"✗ Błąd pobierania zadań: {e}")
        return None


def update_project(conn, project_id, new_name):
    """
    Zaktualizuj nazwę projektu
    :param conn: obiekt Connection
    :param project_id: ID projektu do aktualizacji
    :param new_name: nowa nazwa
    :return: True jeśli sukces, False jeśli błąd
    """
    sql = 'UPDATE projects SET nazwa = ? WHERE id = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (new_name, project_id))
        conn.commit()
        print(f"✓ Projekt o ID {project_id} zaktualizowany na '{new_name}'")
        return True
    except Error as e:
        print(f"✗ Błąd aktualizacji: {e}")
        return False


def update_task_status(conn, task_id, new_status):
    """
    Zaktualizuj status zadania
    :param conn: obiekt Connection
    :param task_id: ID zadania
    :param new_status: nowy status (np. 'W trakcie', 'Ukończone')
    :return: True jeśli sukces, False jeśli błąd
    """
    sql = 'UPDATE tasks SET status = ? WHERE id = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (new_status, task_id))
        conn.commit()
        print(f"✓ Zadanie o ID {task_id} zmienione na status: {new_status}")
        return True
    except Error as e:
        print(f"✗ Błąd aktualizacji statusu: {e}")
        return False


def delete_project(conn, project_id):
    """
    Usuń projekt
    :param conn: obiekt Connection
    :param project_id: ID projektu do usunięcia
    :return: True jeśli sukces, False jeśli błąd
    """
    sql = 'DELETE FROM projects WHERE id = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (project_id,))
        conn.commit()
        print(f"✓ Projekt o ID {project_id} usunięty")
        return True
    except Error as e:
        print(f"✗ Błąd usuwania: {e}")
        return False


def delete_task(conn, task_id):
    """
    Usuń zadanie
    :param conn: obiekt Connection
    :param task_id: ID zadania do usunięcia
    :return: True jeśli sukces, False jeśli błąd
    """
    sql = 'DELETE FROM tasks WHERE id = ?'
    try:
        cur = conn.cursor()
        cur.execute(sql, (task_id,))
        conn.commit()
        print(f"✓ Zadanie o ID {task_id} usunięte")
        return True
    except Error as e:
        print(f"✗ Błąd usuwania: {e}")
        return False


def print_projects(projects):
    """
    Wyświetl wszystkie projekty w ładnym formacie
    :param projects: lista projektów
    """
    if projects:
        print("\n" + "="*70)
        print("PROJEKTY")
        print("="*70)
        for project in projects:
            print(f"ID: {project[0]:3} | Nazwa: {project[1]:25} | Start: {project[2]} | Koniec: {project[3]}")
    else:
        print("Brak projektów w bazie")


def print_tasks(tasks):
    """
    Wyświetl wszystkie zadania w ładnym formacie
    :param tasks: lista zadań
    """
    if tasks:
        print("\n" + "="*100)
        print("ZADANIA")
        print("="*100)
        for task in tasks:
            print(f"ID: {task[0]:3} | Proj ID: {task[1]:3} | Nazwa: {task[2]:20} | Status: {task[4]:15} | Start: {task[5]}")
    else:
        print("Brak zadań w bazie")


def create_tables(conn):
    """
    Stwórz tabele projects i tasks
    :param conn: obiekt Connection
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
        print("✓ Tabele utworzone pomyślnie")
    except Error as e:
        print(f"✗ Błąd tworzenia tabel: {e}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ZAAWANSOWANE FUNKCJE DO ZARZĄDZANIA BAZĄ DANYCH")
    print("="*70)
    
    db_file = "project_manager.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Stwórz tabele
        create_tables(conn)
        
        # ============================================================
        # ĆWICZENIE 1: Dodaj projekty
        # ============================================================
        print("\n" + "-"*70)
        print("DODAWANIE PROJEKTÓW")
        print("-"*70)
        
        project1 = ("Zrób to dobrze", "2024-01-01", "2024-06-30")
        project2 = ("Zrób to LEPIEJ", "2024-02-01", "2024-08-31")
        project3 = ("Python na sterydach", "2024-03-01", "2024-12-31")
        
        pid1 = add_project(conn, project1)
        pid2 = add_project(conn, project2)
        pid3 = add_project(conn, project3)
        
        # ============================================================
        # ĆWICZENIE 2: Dodaj zadania do projektów
        # ============================================================
        print("\n" + "-"*70)
        print("DODAWANIE ZADAŃ")
        print("-"*70)
        
        task1 = (pid1, "Zaplanować projekt", "Przygotować szczegółowy plan", "Rozpoczęte", "2024-01-01", "2024-01-10")
        task2 = (pid1, "Kodować", "Napisać główny kod", "W trakcie", "2024-01-11", "2024-06-25")
        task3 = (pid2, "Refaktoryzacja", "Ulepszyć kod", "Oczekujące", "2024-02-01", "2024-08-25")
        task4 = (pid3, "Nauka", "Pogłębiać wiedzę", "Rozpoczęte", "2024-03-01", "2024-12-31")
        
        add_task(conn, task1)
        add_task(conn, task2)
        add_task(conn, task3)
        add_task(conn, task4)
        
        # ============================================================
        # ĆWICZENIE 3: Pobierz i wyświetl dane
        # ============================================================
        print("\n" + "-"*70)
        print("POBIERANIE DANYCH Z BAZY")
        print("-"*70)
        
        all_projects = get_all_projects(conn)
        print_projects(all_projects)
        
        all_tasks = get_all_tasks(conn)
        print_tasks(all_tasks)
        
        # ============================================================
        # ĆWICZENIE 4: Pobierz zadania dla konkretnego projektu
        # ============================================================
        print("\n" + "-"*70)
        print(f"ZADANIA DLA PROJEKTU O ID {pid1}")
        print("-"*70)
        
        project1_tasks = get_tasks_by_project(conn, pid1)
        print_tasks(project1_tasks)
        
        # ============================================================
        # ĆWICZENIE 5: Aktualizuj dane
        # ============================================================
        print("\n" + "-"*70)
        print("AKTUALIZACJA DANYCH")
        print("-"*70)
        
        update_project(conn, pid1, "MEGA PROJECT - Zrób to perfekcyjnie")
        update_task_status(conn, 1, "Ukończone")
        update_task_status(conn, 2, "Ukończone")
        
        # ============================================================
        # ĆWICZENIE 6: Wyświetl zaktualizowane dane
        # ============================================================
        print("\n" + "-"*70)
        print("STAN PO AKTUALIZACJI")
        print("-"*70)
        
        all_projects = get_all_projects(conn)
        print_projects(all_projects)
        
        all_tasks = get_all_tasks(conn)
        print_tasks(all_tasks)
        
        # ============================================================
        # ĆWICZENIE 7: Usuń dane
        # ============================================================
        print("\n" + "-"*70)
        print("USUWANIE DANYCH")
        print("-"*70)
        
        delete_task(conn, 3)
        
        # ============================================================
        # ĆWICZENIE 8: Stan końcowy
        # ============================================================
        print("\n" + "-"*70)
        print("STAN KOŃCOWY BAZY")
        print("-"*70)
        
        all_projects = get_all_projects(conn)
        print_projects(all_projects)
        
        all_tasks = get_all_tasks(conn)
        print_tasks(all_tasks)
        
        print("\n✓ Wszystkie operacje zakończone!")
        
        conn.close()
