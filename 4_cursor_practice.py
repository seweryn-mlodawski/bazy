# ============================================
# Ćwiczenia z kursorem w SQLite
# ============================================
# Ten plik zawiera praktyczne ćwiczenia do nauczenia się
# jak używać kursora do komunikacji z bazą danych

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Nawiąz połączenie z bazą danych SQLite
    :param db_file: ścieżka do pliku bazy danych
    :return: obiekt Connection lub None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"✓ Połączenie z bazą '{db_file}' nawiązane")
        return conn
    except Error as e:
        print(f"✗ Błąd połączenia: {e}")
        return None


def execute_sql(conn, sql):
    """
    Wykonaj polecenie SQL bez pobierania wyników
    :param conn: obiekt Connection
    :param sql: polecenie SQL
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        print(f"✓ Polecenie SQL wykonane pomyślnie")
    except Error as e:
        print(f"✗ Błąd wykonania: {e}")


def execute_sql_with_results(conn, sql):
    """
    Wykonaj polecenie SQL i pobierz wyniki
    :param conn: obiekt Connection
    :param sql: polecenie SQL SELECT
    :return: lista wyników
    """
    try:
        c = conn.cursor()
        c.execute(sql)
        results = c.fetchall()
        return results
    except Error as e:
        print(f"✗ Błąd wykonania: {e}")
        return None


def exercise_1_create_tables():
    """
    ĆWICZENIE 1: Tworzenie tabel za pomocą kursora
    Zadanie: Stwórzcie tabelę 'students' z polami: id, imie, nazwisko, ocena
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 1: Tworzenie tabel")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Tutaj KURSOR bierze nasze polecenie i wysyła je do bazy
        create_students_table = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            imie TEXT NOT NULL,
            nazwisko TEXT NOT NULL,
            ocena REAL NOT NULL
        );
        """
        
        execute_sql(conn, create_students_table) # KURSOR wykonuje polecenie SQL
        conn.close() # Zamykamy połączenie


def exercise_2_insert_single_record():
    """
    ĆWICZENIE 2: Wstawianie jednego rekordu
    Zadanie: Wstawić jednego ucznia do tabeli
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 2: Wstawianie jednego rekordu")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Kursor otrzymuje zapytanie INSERT z parametrami (?)
        insert_student = """
        INSERT INTO students (imie, nazwisko, ocena)
        VALUES (?, ?, ?);
        """
        
        # Tworzymy kursor
        c = conn.cursor()
        
        # Wykonujemy INSERT z konkretnymi danymi
        student_data = ("Jan", "Kowalski", 4.5)
        c.execute(insert_student, student_data)
        
        # Zatwierdzamy zmianę
        conn.commit()
        print(f"✓ Uczeń dodany: {student_data[0]} {student_data[1]}")
        
        conn.close()


def exercise_3_insert_multiple_records():
    """
    ĆWICZENIE 3: Wstawianie wielu rekordów
    Zadanie: Wstawić kilku uczniów za pomocą pętli
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 3: Wstawianie wielu rekordów")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        insert_student = """
        INSERT INTO students (imie, nazwisko, ocena)
        VALUES (?, ?, ?);
        """
        
        # Lista uczniów do wstawienia
        students = [
            ("Maria", "Nowak", 5.0),
            ("Piotr", "Lewandowski", 3.5),
            ("Anna", "Wiśniewski", 4.8),
            ("Tomasz", "Dabrowski", 3.2),
        ]
        
        c = conn.cursor()
        
        # Pętla: dla każdego ucznia, kursor wykonuje INSERT
        for student in students:
            c.execute(insert_student, student)
            print(f"  + Dodano: {student[0]} {student[1]} - ocena: {student[2]}")
        
        # Jedno commit dla wszystkich zmian naraz (efektywniej!)
        conn.commit()
        print(f"✓ Łącznie dodano {len(students)} uczniów")
        
        conn.close()


def exercise_4_select_all_records():
    """
    ĆWICZENIE 4: Pobieranie wszystkich rekordów
    Zadanie: Wyświetlić wszystkich uczniów z tabeli
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 4: Pobieranie wszystkich rekordów (SELECT)")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Kursor pobiera wszystkie rekordy
        select_all = "SELECT * FROM students;"
        
        results = execute_sql_with_results(conn, select_all)
        
        if results:
            print("\nWszyscy uczniowie w bazie:")
            print("-" * 50)
            for row in results:
                print(f"ID: {row[0]}, Imię: {row[1]}, Nazwisko: {row[2]}, Ocena: {row[3]}")
        
        conn.close()


def exercise_5_select_with_condition():
    """
    ĆWICZENIE 5: Pobieranie rekordów z warunkiem
    Zadanie: Wyświetlić uczniów z oceną wyższą niż 4.0
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 5: SELECT z warunkiem WHERE")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Kursor pobiera tylko uczniów z wysoką oceną
        select_good_students = "SELECT imie, nazwisko, ocena FROM students WHERE ocena >= ?;"
        
        c = conn.cursor()
        c.execute(select_good_students, (4.0,))
        results = c.fetchall()
        
        if results:
            print("\nUczniowie z oceną >= 4.0:")
            print("-" * 50)
            for row in results:
                print(f"{row[0]} {row[1]} - ocena: {row[2]}")
        
        conn.close()


def exercise_6_update_record():
    """
    ĆWICZENIE 6: Aktualizacja rekordu
    Zadanie: Zmienić ocenę ucznia
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 6: Aktualizacja rekordu (UPDATE)")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Kursor aktualizuje ocenę
        update_grade = """
        UPDATE students
        SET ocena = ?
        WHERE imie = ? AND nazwisko = ?;
        """
        
        c = conn.cursor()
        c.execute(update_grade, (4.9, "Piotr", "Lewandowski"))
        
        conn.commit()
        print(f"✓ Ocena ucznia Piotr Lewandowski zmieniona na 4.9")
        
        conn.close()


def exercise_7_delete_record():
    """
    ĆWICZENIE 7: Usuwanie rekordu
    Zadanie: Usunąć ucznia z najniższą oceną
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 7: Usuwanie rekordu (DELETE)")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Kursor usuwa ucznia
        delete_student = """
        DELETE FROM students
        WHERE imie = ? AND nazwisko = ?;
        """
        
        c = conn.cursor()
        c.execute(delete_student, ("Tomasz", "Dabrowski"))
        
        conn.commit()
        print(f"✓ Uczeń Tomasz Dabrowski usunięty z bazy")
        
        conn.close()


def exercise_8_count_records():
    """
    ĆWICZENIE 8: Zliczanie rekordów
    Zadanie: Sprawdzić, ilu uczniów jest w bazie
    """
    print("\n" + "="*50)
    print("ĆWICZENIE 8: Zliczanie rekordów (COUNT)")
    print("="*50)
    
    db_file = "curriculum.db"
    conn = create_connection(db_file)
    
    if conn is not None:
        # Kursor zlicza rekordy
        count_query = "SELECT COUNT(*) FROM students;"
        
        c = conn.cursor()
        c.execute(count_query)
        result = c.fetchone()  # fetchone() pobiera jeden wynik
        
        if result:
            print(f"✓ Liczba uczniów w bazie: {result[0]}")
        
        conn.close()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("PRAKTYKA Z KURSOREM W SQLITE")
    print("="*50)
    
    # Uruchamiamy ćwiczenia po kolei
    exercise_1_create_tables()
    exercise_2_insert_single_record()
    exercise_3_insert_multiple_records()
    exercise_4_select_all_records()
    exercise_5_select_with_condition()
    exercise_6_update_record()
    exercise_7_delete_record()
    exercise_8_count_records()
    
    # Na koniec ponownie wyświetl wszystkich uczniów
    print("\n" + "="*50)
    print("STAN KOŃCOWY BAZY")
    print("="*50)
    exercise_4_select_all_records()
    
    print("\n✓ Wszystkie ćwiczenia zostały ukończone!")
