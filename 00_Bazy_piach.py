import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """
    Nawiąż połączenie z bazą danych SQLite
    :param db_file: ścieżka do pliku bazy
    :return: obiekt połączenia lub None
    """
    conn = None # inicjalizacja zmiennej conn jako None
    try: 
        conn = sqlite3.connect(db_file) # próba połączenia z bazą danych
        return conn # zwrócenie obiektu połączenia
    except Error as e: # obsługa błędu połączenia
        print(f"✗ Błąd połączenia: {e}")
    return conn # zwrócenie obiektu połączenia lub None

# Krok 2 - tworzenie tabeli sensors

def create_sensors_table(conn):
    """
    Utwórz tabelę sensors w bazie danych
    """
    sql = """
     CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY,
            model TEXT NOT NULL,
            typ TEXT,
            piny INTEGER NOT NULL
        );
        """
    try:
        cur = conn.cursor() # utworzenie kursora
        cur.execute(sql)    # wykonanie polecenia SQL do utworzenia tabeli sensors
        conn.commit()   # zatwierdzenie zmian w bazie danych
        print("✓ Tabela 'sensors' utworzona")
    except Error as e:
        print(f"✗ Błąd tworzenia tabeli: {e}")

def create_warehouses_table(conn):
    """
    Utwórz tabelę warehouses w bazie danych
    """
    sql = """
     CREATE TABLE IF NOT EXISTS warehouses (
            id INTEGER PRIMARY KEY,
            sensor_id INTEGER NOT NULL,
            nazwa_magazynu TEXT NOT NULL,
            alejka INTEGER NOT NULL,
            regał INTEGER NOT NULL,
            polka INTEGER NOT NULL,
            kuweta INTEGER NOT NULL,
            ilosc_sztuk INTEGER NOT NULL,
            FOREIGN KEY (sensor_id) REFERENCES sensors (id)            
        );
        """
    try:
        cur = conn.cursor() # utworzenie kursora
        cur.execute(sql)    # wykonanie polecenia SQL do utworzenia tabeli warehouses
        conn.commit()   # zatwierdzenie zmian w bazie danych
        print("✓ Tabela 'warehouses' utworzona")
    except Error as e:
        print(f"✗ Błąd tworzenia tabeli: {e}")

# Dodawanie danych do tabeli sensors
def add_sensor(conn, model, typ, piny):
    """
    Dodaj nowy czujnik do tabeli sensors
    :param conn: obiekt Connection
    :param model: model czujnika
    :param typ: typ czujnika
    :param piny: liczba pinów czujnika
    """
    sql = '''
    INSERT INTO sensors(model, typ, piny)
    VALUES(?,?,?)
    '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (model, typ, piny))
        conn.commit()
        print(f"✓ Nowy czujnik - {model} dodany do tabeli 'sensors'")
        return cur.lastrowid # zwrócenie id nowo dodanego rekordu
    except Error as e:
        print(f"✗ Błąd dodawania czujnika: {e}")
        return None # zwrócenie None w przypadku błędu
     

# Główna część skryptu    
if __name__ == "__main__":
    conn = create_connection("sensors.db")
    print(f"✓ Połączenie utworzone {conn} - utworzone zostało sensors.db")
    
    # Krok 2 - tworzenie tabeli sensors i warehouses
    create_sensors_table(conn)
    create_warehouses_table(conn)
    # Krok 3 - zamknięcie połączenia
    if conn:
        conn.close()
        print("✓ Połączenie zamknięte - sensors.db zapisane na dysku")