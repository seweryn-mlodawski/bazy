# ============================================
# LOGIKA DZIAŁANIA KODU - UPDATE
# ============================================
# Instrukcja krok po kroku co się dzieje

"""
PRZEPŁYW LOGIKI - JAK DZIAŁA CAŁY KOD
=====================================

GŁÓWNY PRZEPŁYW:

1. Program się uruchamia
   ↓
2. if __name__ == "__main__": - sprawdza czy plik uruchamiana bezpośrednio
   ↓
3. conn = create_connection("database.db") - tworzy połączenie z bazą
   ↓
4. update(conn, "tasks", 2, status="started") - PIERWSZY UPDATE
   ↓
5. update(conn, "tasks", 2, stat="started") - DRUGI UPDATE (z błędem!)
   ↓
6. conn.close() - zamyka połączenie z bazą


TERAZ SZCZEGÓŁ PIERWSZEGO UPDATE:
==================================

Wywołanie:
----------
update(conn, "tasks", 2, status="started")

Co to oznacza?
- Aktualizuj (update) 
- w bazie (conn)
- tabelę "tasks"
- wiersz z id = 2
- zmień pole status na "started"


WEWNĄTRZ FUNKCJI update():
---========================

1. KROK 1: Przygotowanie parametrów
   ==========================================
   
   parameters = [f"{k} = ?" for k in kwargs]
   
   kwargs = {"status": "started"}  (to co przesłaliśmy)
   
   Lista: ["status = ?"]
   
   Wyjaśnienie:
   - k = "status"
   - f"{k} = ?" = "status = ?"  (f-string - wstawia wartość zmiennej k)
   - Tworzymy listę z jednym elementem: ["status = ?"]


2. KROK 2: Zamiana listy na string
   ==========================================
   
   parameters = ", ".join(parameters)
   
   Przed: ["status = ?"]
   Po:    "status = ?"
   
   Wyjaśnienie:
   - .join() - łączy elementy listy w jeden string
   - ", " - separator (przecinek + spacja)
   - Jeśli byłoby wiele pól: ["status = ?", "date = ?"]
     to by stało się: "status = ?, date = ?"


3. KROK 3: Ekstrakcja wartości ze słownika
   ==========================================
   
   values = tuple(v for v in kwargs.values())
   
   kwargs = {"status": "started"}
   
   Działanie:
   - kwargs.values() - pobiera wartości słownika
   - v for v in ... - iteruje po każdej wartości
   - tuple(...) - zamienia generator na tuplę
   
   Wynik: ("started",)
   
   Wyjaśnienie:
   - Tu mamy jedną wartość: "started"
   - Jeśli byłoby więcej: {"status": "started", "date": "2024-01-01"}
     to by było: ("started", "2024-01-01")


4. KROK 4: Dodanie ID do wartości (dla WHERE)
   ==========================================
   
   values += (id, )
   
   Przed: ("started",)
   Po:    ("started", 2)  gdzie id=2
   
   Wyjaśnienie:
   - += to dodawanie do tupli
   - (id, ) - tuplę z ID (przecinek jest ważny!)
   - Wynik: obie wartości razem
   
   Dlaczego tu ID?
   - SQL będzie mieć dwa znaki zapytania: ? i ?
   - Pierwszy ? to pole do aktualizacji
   - Drugi ? to warunek WHERE


5. KROK 5: Budowanie polecenia SQL
   ==========================================
   
   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   
   Wstawienie wartości:
   - {table} = "tasks"
   - {parameters} = "status = ?"
   
   Wynik:
   UPDATE tasks
   SET status = ?
   WHERE id = ?
   
   Wyjaśnienie:
   - f''' ''' - f-string z multi-line (trzy cudzysłowy)
   - UPDATE - polecenie SQL do aktualizacji
   - SET - ustawienie nowych wartości
   - WHERE - warunek którą linię aktualizować


6. KROK 6: Wykonanie polecenia
   ==========================================
   
   cur = conn.cursor()
   cur.execute(sql, values)
   
   Działanie:
   - Tworzenie kursora (pośrednik do bazy)
   - execute() - wykonuje SQL z wartościami
   
   Execute wstawia wartości w miejsce znaku zapytania:
   sql:    UPDATE tasks SET status = ? WHERE id = ?
   values: ("started", 2)
   
   Wynik:  UPDATE tasks SET status = 'started' WHERE id = 2
   
   Co to robi?
   - Szuka wiersza w tabeli tasks gdzie id=2
   - Zmienia pole status na "started"


7. KROK 7: Zatwierdzenie zmian
   ==========================================
   
   conn.commit()
   
   Wyjaśnienie:
   - commit() = "zatwierdź zmiany"
   - Bez tego zmiany byłyby w pamięci, ale nie zapisane w bazie!
   - Przesłanie danych z pamięci do dysku


8. KROK 8: Wyświetlenie wyniku
   ==========================================
   
   print("OK")
   
   Wyświetla: OK
   (jeśli wszystko poszło dobrze)


DRUGI UPDATE - Z BŁĘDEM:
========================

update(conn, "tasks", 2, stat="started")
                       ^^^
                   błąd! (powinno być "status")

Przepływ:
1. kwargs = {"stat": "started"}
2. parameters = ["stat = ?"]
3. parameters = "stat = ?"
4. values = ("started", 2)
5. sql = "UPDATE tasks SET stat = ? WHERE id = ?"
6. cur.execute(sql, values)  ← Błąd! Kolumna "stat" nie istnieje!

Wyłapanie błędu:
except sqlite3.OperationalError as e:
    print(e)

Wyświetli coś takiego:
no such column: stat


PODSUMOWANIE - CO SIĘ PO CZYM DZIEJE:
=====================================

Program główny:
  ↓
Łączenie z bazą
  ↓
Pierwszy update (poprawny) → Zmienia status na "started"
  ↓
Drugi update (błęd) → Próbuje zmienić kolumnę "stat" (nie istnieje!)
  ↓
Wyłapanie błędu i wyświetlenie
  ↓
Zamknięcie połączenia z bazą
  ↓
Program się kończy


DLACZEGO TO JEST TAKIE SPRYTNE?
================================

1. **Elastyczność** - funkcja aktualizuje dowolne pola
   - update(conn, "tasks", 2, status="started")
   - update(conn, "tasks", 2, status="started", date="2024-01-01")
   
2. **Bezpieczeństwo** - znaki zapytania (?) chronia przed SQL Injection
   - Zamiast: f"UPDATE {table} SET {key} = '{value}'"
   - Robimy: cur.execute(sql, (value,))
   
3. **Uniwersalność** - działa dla każdej tabeli
   - update(conn, "tasks", 2, status="started")
   - update(conn, "projects", 5, nazwa="Nowy projekt")


ANALOGIA DO CODZIENNEGO ŻYCIA:
==============================

Wyobraź sobie, że aktualizujesz danymi formularz w systemie:

1. Otwierasz plik bazy danych (create_connection)
2. Wypełniasz formularz (kwargs = {"status": "started"})
3. System sprawdza jakie pola chcesz zmienić (parameters)
4. System buduje polecenie do bazy (sql)
5. System wysyła polecenie z wartościami (execute)
6. System zapisuje zmiany na dysku (commit)
7. Zamykasz plik (close)
"""

# PRZYKŁAD W PRAKTYCE:
if __name__ == "__main__":
    import sqlite3
    from sqlite3 import Error
    
    # Funkcje z oryginalnego kodu
    
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
    
    
    def update(conn, table, id, **kwargs):
        """Funkcja do aktualizacji danych"""
        
        # KROK 1: Przygotuj listę parametrów
        parameters = [f"{k} = ?" for k in kwargs]
        print(f"1. Parametry (lista):    {parameters}")
        
        # KROK 2: Zamień listę na string
        parameters = ", ".join(parameters)
        print(f"2. Parametry (string):   {parameters}")
        
        # KROK 3: Ekstrakcja wartości
        values = tuple(v for v in kwargs.values())
        print(f"3. Wartości (bez ID):    {values}")
        
        # KROK 4: Dodaj ID
        values += (id, )
        print(f"4. Wartości (z ID):      {values}")
        
        # KROK 5: Budowanie SQL
        sql = f''' UPDATE {table}
                 SET {parameters}
                 WHERE id = ?'''
        print(f"5. SQL do wykonania:\n{sql}")
        
        # KROK 6-7: Wykonanie i zatwierdzenie
        try:
            cur = conn.cursor()
            print(f"6. Wykonuję polecenie...")
            cur.execute(sql, values)
            conn.commit()
            print(f"7. Zatwierdzenie - OK!\n")
        except sqlite3.OperationalError as e:
            print(f"7. Błąd: {e}\n")
    
    
    # URUCHOMIENIE
    print("="*70)
    print("DEMONSTRACJA LOGIKI UPDATE")
    print("="*70 + "\n")
    
    conn = create_connection("demo.db")
    
    print("PIERWSZY UPDATE (poprawny):")
    print("-" * 70)
    update(conn, "tasks", 2, status="started")
    
    print("\nDRUGI UPDATE (z błędem):")
    print("-" * 70)
    update(conn, "tasks", 2, stat="started")
    
    conn.close()
    print("\n" + "="*70)
    print("Program zakończony!")
    print("="*70)
