# ============================================
# MY_DATABASE.PY - MOJA BAZA DANYCH
# ============================================
# Praktyczne zastosowanie CRUD operacji
# CREATE, READ, UPDATE, DELETE
# 
# Temat: Zarządzanie kolekcją książek bibliotecznej

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    KROK 1: POŁĄCZENIE Z BAZĄ
    Nawiąż połączenie z bazą danych SQLite
    
    :param db_file: ścieżka do pliku bazy
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(f"✗ Błąd połączenia: {e}")
    return conn


def create_tables(conn):
    """
    KROK 2: TWORZENIE TABEL (CREATE TABLE)
    Stwórz strukturę bazy danych
    """
    
    # Tabela kategorii
    create_categories_sql = """
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        nazwa TEXT NOT NULL UNIQUE,
        opis TEXT
    );
    """
    
    # Tabela książek
    create_books_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        tytul TEXT NOT NULL,
        autor TEXT NOT NULL,
        rok_wydania INTEGER,
        category_id INTEGER NOT NULL,
        dostepna BOOLEAN DEFAULT 1,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );
    """
    
    try:
        cur = conn.cursor()
        cur.execute(create_categories_sql)
        cur.execute(create_books_sql)
        conn.commit()
        print("✓ Tabele utworzone\n")
    except Error as e:
        print(f"✗ Błąd: {e}")


def add_category(conn, nazwa, opis=""):
    """
    KROK 3: DODAWANIE DANYCH (CREATE - INSERT)
    Dodaj nową kategorię do bazy
    """
    sql = "INSERT INTO categories(nazwa, opis) VALUES(?, ?)"
    try:
        cur = conn.cursor()
        cur.execute(sql, (nazwa, opis))
        conn.commit()
        print(f"✓ Dodano kategorię: {nazwa}")
        return cur.lastrowid
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def add_book(conn, tytul, autor, rok, category_id):
    """
    KROK 3: DODAWANIE DANYCH (CREATE - INSERT)
    Dodaj nową książkę do bazy
    """
    sql = "INSERT INTO books(tytul, autor, rok_wydania, category_id) VALUES(?, ?, ?, ?)"
    try:
        cur = conn.cursor()
        cur.execute(sql, (tytul, autor, rok, category_id))
        conn.commit()
        print(f"✓ Dodano książkę: {tytul}")
        return cur.lastrowid
    except Error as e:
        print(f"✗ Błąd: {e}")
        return None


def select_all_books(conn):
    """
    KROK 4: POBIERANIE DANYCH (READ - SELECT)
    Pobierz wszystkie książki z bazy
    """
    sql = """
    SELECT books.id, books.tytul, books.autor, books.rok_wydania, 
           categories.nazwa, books.dostepna
    FROM books
    INNER JOIN categories ON books.category_id = categories.id
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"✗ Błąd: {e}")
        return []


def select_books_by_category(conn, category_id):
    """
    KROK 4: POBIERANIE DANYCH (READ - SELECT Z WARUNKIEM)
    Pobierz książki z konkretnej kategorii
    """
    sql = """
    SELECT * FROM books 
    WHERE category_id = ?
    """
    try:
        cur = conn.cursor()
        cur.execute(sql, (category_id,))
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"✗ Błąd: {e}")
        return []


def count_books(conn):
    """
    KROK 4: POBIERANIE DANYCH (COUNT)
    Policz ile jest wszystkich książek
    """
    sql = "SELECT COUNT(*) FROM books"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        return result[0]
    except Error as e:
        print(f"✗ Błąd: {e}")
        return 0


def update_book_availability(conn, book_id, dostepna):
    """
    KROK 5: AKTUALIZACJA DANYCH (UPDATE)
    Zmień dostępność książki (wypożyczenie/zwrot)
    """
    sql = "UPDATE books SET dostepna = ? WHERE id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (dostepna, book_id))
        conn.commit()
        status = "dostępna" if dostepna else "wypożyczona"
        print(f"✓ Książka teraz: {status}")
    except Error as e:
        print(f"✗ Błąd: {e}")


def delete_book(conn, book_id):
    """
    KROK 6: USUWANIE DANYCH (DELETE Z WARUNKIEM)
    Usuń książkę z bazy (np. zniszczona)
    """
    sql = "DELETE FROM books WHERE id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (book_id,))
        conn.commit()
        print(f"✓ Usunięto książkę o ID {book_id}")
    except Error as e:
        print(f"✗ Błąd: {e}")


def display_all_books(conn):
    """
    Wyświetl wszystkie książki w ładnym formacie
    """
    books = select_all_books(conn)
    if books:
        print("\n" + "="*80)
        print("WSZYSTKIE KSIĄŻKI W BIBLIOTECE")
        print("="*80)
        for book in books:
            status = "✓" if book[5] else "✗"
            print(f"ID: {book[0]:2} | {book[1]:30} | {book[2]:20} | "
                  f"{book[3]} | {book[4]:15} | {status}")
        print("="*80 + "\n")
    else:
        print("Brak książek w bazie!\n")


def display_statistics(conn):
    """
    Wyświetl statystyki
    """
    total = count_books(conn)
    print(f"\n📊 STATYSTYKI:")
    print(f"   Łącznie książek: {total}")
    print()

#============================================
# MAIN - URUCHOMIENIE PROGRAMU

if __name__ == "__main__":
    print("\n" + "="*80)
    print("MOJA BAZA DANYCH - BIBLIOTEKA")
    print("="*80 + "\n")
    
    # KROK 1: Połączenie z bazą
    print("KROK 1: Połączenie z bazą danych")
    print("-" * 80)
    conn = create_connection("moja_biblioteka.db")
    
    if conn is not None:
        
        # KROK 2: Tworzenie tabel
        print("\nKROK 2: Tworzenie struktury bazy (tabel)")
        print("-" * 80)
        create_tables(conn)
        
        # KROK 3: DODAWANIE DANYCH (CREATE)
        print("\nKROK 3: Dodawanie kategorii i książek (CREATE - INSERT)")
        print("-" * 80)
        
        # Dodaj kategorie
        cat_fiction = add_category(conn, "Fikcja", "Powieści i opowiadania")
        cat_non_fiction = add_category(conn, "Non-fiction", "Książki faktu")
        cat_programming = add_category(conn, "Programowanie", "Informatyka i kurs")
        
        # Dodaj książki
        add_book(conn, "1984", "George Orwell", 1949, cat_fiction)
        add_book(conn, "Mistrz i Małgorzata", "Mikhail Bulgakov", 1967, cat_fiction)
        add_book(conn, "Sapiens", "Yuval Harari", 2011, cat_non_fiction)
        add_book(conn, "Clean Code", "Robert Martin", 2008, cat_programming)
        add_book(conn, "Python dla każdego", "Mark Lutz", 2013, cat_programming)
        
        # KROK 4: POBIERANIE DANYCH (READ - SELECT)
        print("\n\nKROK 4: Pobieranie i wyświetlanie danych (READ - SELECT)")
        print("-" * 80)
        display_all_books(conn)
        
        # Pobierz tylko książki o programowaniu
        print("Książki tylko z kategorii 'Programowanie':")
        print("-" * 80)
        programming_books = select_books_by_category(conn, cat_programming)
        for book in programming_books:
            print(f"  • {book[1]} - {book[2]} ({book[3]})")
        print()
        
        # KROK 5: AKTUALIZACJA DANYCH (UPDATE)
        print("\nKROK 5: Aktualizacja danych (UPDATE)")
        print("-" * 80)
        print("Symulacja: Wypożyczenie książki 'Clean Code'")
        update_book_availability(conn, 4, 0)  # dostepna = 0 (wypożyczona)
        
        print("\nSymulacja: Zwrot książki 'Clean Code'")
        update_book_availability(conn, 4, 1)  # dostepna = 1 (dostępna)
        print()
        
        # KROK 6: USUWANIE DANYCH (DELETE)
        print("\nKROK 6: Usuwanie danych (DELETE)")
        print("-" * 80)
        print("Symulacja: Zniszczenie książki 'Sapiens' - usunięcie z bazy")
        delete_book(conn, 3)
        print()
        
        # PODSUMOWANIE
        print("\nPODSUMOWANIE - Stan bazy po wszystkich operacjach:")
        print("-" * 80)
        display_all_books(conn)
        display_statistics(conn)
        
        # ZAMKNIĘCIE POŁĄCZENIA
        conn.close()
        print("✓ Połączenie zamknięte\n")
        
        print("="*80)
        print("✓ Program zakończony!")
        print("="*80 + "\n")
        
        print("""
PODSUMOWANIE - CO ZROBIŁEŚ:
===========================

KROK 1: POŁĄCZENIE
  → Nawiązałeś połączenie z bazą "moja_biblioteka.db"
  
KROK 2: TWORZENIE STRUKTURY (CREATE TABLE)
  → Stworzyłeś tabele: categories i books
  
KROK 3: DODAWANIE DANYCH (INSERT - CREATE)
  → Dodałeś 3 kategorie
  → Dodałeś 5 książek
  → Każda książka ma przypisaną kategorię (FOREIGN KEY)
  
KROK 4: POBIERANIE DANYCH (SELECT - READ)
  → Pobrałeś WSZYSTKIE książki (SELECT * + JOIN)
  → Pobrałeś książki z konkretnej kategorii (SELECT WHERE)
  → Policzyłeś ilość książek (COUNT)
  
KROK 5: AKTUALIZACJA DANYCH (UPDATE)
  → Zmieniłeś dostępność książki (UPDATE SET WHERE)
  → Symulowałeś wypożyczenie i zwrot
  
KROK 6: USUWANIE DANYCH (DELETE)
  → Usunąłeś książkę z bazy (DELETE WHERE)
  → Symulowałeś usunięcie zniszczonej książki

WSZYSTKIE OPERACJE CRUD:
✓ CREATE - dodawanie danych (INSERT)
✓ READ   - pobieranie danych (SELECT)
✓ UPDATE - zmiana danych (UPDATE)
✓ DELETE - usuwanie danych (DELETE)

Gratulacje! Opanowałeś pełny cykl pracy z bazami danych! 🎉
""")


"""
OPERACJE W BAZIE DANYCH - PODSUMOWANIE
=======================================

BAZA DANYCH: moja_biblioteka.db

TABELE:
  1. categories
     - id (PRIMARY KEY)
     - nazwa (NOT NULL, UNIQUE)
     - opis
  
  2. books
     - id (PRIMARY KEY)
     - tytul (NOT NULL)
     - autor (NOT NULL)
     - rok_wydania
     - category_id (FOREIGN KEY)
     - dostepna (BOOLEAN)

OPERACJE:
  ✓ CREATE - Insert data
  ✓ READ   - Select data
  ✓ UPDATE - Update data
  ✓ DELETE - Delete data

ZAPYTANIA SQL:
  INSERT INTO books VALUES (...)
  SELECT * FROM books
  SELECT * FROM books WHERE category_id = ?
  UPDATE books SET dostepna = ? WHERE id = ?
  DELETE FROM books WHERE id = ?
"""
