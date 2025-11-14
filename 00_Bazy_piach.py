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

#=======================================================
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
    
    #=======================================================
    # Dodawanie danych do tabeli warehouses    
def add_warehouse(conn, sensor_id, nazwa_magazynu, alejka, regał, polka, kuweta, ilosc_sztuk):
    """
    Dodaj nowy magazyn do tabeli warehouses
    :param conn: obiekt Connection
    :param sensor_id: id czujnika powiązanego z magazynem
    :param nazwa_magazynu: nazwa magazynu
    :param alejka: numer alejki
    :param regał: numer regału
    :param polka: numer półki
    :param kuweta: numer kuwety
    :param ilosc_sztuk: ilość sztuk w magazynie
    """
    sql = '''
    INSERT INTO warehouses(sensor_id, nazwa_magazynu, alejka, regał, polka, kuweta, ilosc_sztuk)
    VALUES(?,?,?,?,?,?,?)
    '''
    #=======================================================
    try:
        cur = conn.cursor()
        cur.execute(sql, (sensor_id, nazwa_magazynu, alejka, regał, polka, kuweta, ilosc_sztuk))
        conn.commit()
        print(f"✓ Nowy magazyn - {nazwa_magazynu} dodany do tabeli 'warehouses'")
        return cur.lastrowid # zwrócenie id nowo dodanego rekordu
    except Error as e:
            print(f"✗ Błąd dodawania magazynu: {e}")
            return None # zwrócenie None w przypadku błędu
    
    #SELECT czujników i magazynów
def get_sensors_in_warehouses(conn):
    """
    Pobierz listę czujników wraz z informacjami o magazynach
    :param conn: obiekt Connection
    """
    sql = """
SELECT
    s.id AS 'Sensor ID',
    s.model AS 'Model',
    s.typ AS 'Typ',
    s.piny AS 'Piny',
    w.nazwa_magazynu AS 'Magazyn',
    w.alejka AS 'Alejka',
    w.regał AS 'Regał', 
    w.polka AS 'Półka',
    w.kuweta AS 'Kuweta',
    w.ilosc_sztuk AS 'Ilość (szt.)'
FROM sensors s
INNER JOIN warehouses w ON s.id = w.sensor_id
ORDER BY w.nazwa_magazynu, w.alejka, w.regał, w.polka, w.kuweta
    """        
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(f"✗ Błąd pobierania danych: {e}")
        return []
    
#=======================================================
# Główna część skryptu
# ======================================================   
if __name__ == "__main__":
    conn = create_connection("sensors.db")
    print(f"✓ Połączenie utworzone {conn} - utworzone zostało sensors.db")
    
    # Krok 2 - tworzenie tabeli sensors i warehouses
    create_sensors_table(conn)
    create_warehouses_table(conn)

    # Krok 3 - dodawanie przykładowych danych do tabeli sensors
    print("\nDodawanie czujników do tabeli 'sensors':")
    print("-"*40)
    add_sensor(conn, "DHT11", "Temperatura i Wilgotność", 3) #sensor_id, model, typ, piny
    add_sensor(conn, "HC-SR04", "Odległość", 4)
    add_sensor(conn, "BMP180", "Ciśnienie i Temperatura", 2)
    add_sensor(conn, "MQ-2", "Gaz", 1)
    
    # Krok 4 - dodawanie przykładowych danych do tabeli warehouses
    print("\nDodawanie magazynów do tabeli 'warehouses':")
    print("-"*40)
    add_warehouse(conn, 1, "Magazyn A", 1, 1, 1, 1, 100) #sensor_id, nazwa_magazynu, alejka, regał, polka, kuweta, ilosc_sztuk
    add_warehouse(conn, 2, "Magazyn B", 1, 2, 1, 1, 50)
    add_warehouse(conn, 3, "Magazyn C", 2, 1, 1, 1, 75)
    add_warehouse(conn, 4, "Magazyn A", 2, 2, 1, 1, 200)

    # Krok 5 - pobieranie i wyświetlanie czujników wraz z informacjami o magazynach
    print("\nLista czujników wraz z informacjami o magazynach:")
    print("-"*70)

    data = get_sensors_in_warehouses(conn)

    # Tu zmienić czebaby

if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
        else:
            print("Brak danych w bazie do wyświetlenia.")

        print("\n" + "="*80)

if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
if data:
        counter = 1
        for row in data:
            print(f"\n🔹 CZUJNIK #{counter}:")
            print(f"   └─ ID czujnika:      {row[0]}")
            print(f"   └─ Model:            {row[1]}")
            print(f"   └─ Typ:              {row[2]}")
            print(f"   └─ Liczba pinów:     {row[3]}")
            print(f"   └─ Magazyn:          {row[4]}")
            print(f"   └─ Lokalizacja:")
            print(f"      ├─ Alejka:        {row[5]}")
            print(f"      ├─ Regał:         {row[6]}")
            print(f"      ├─ Półka:         {row[7]}")
            print(f"      └─ Kuweta:        {row[8]}")
            print(f"   └─ Ilość w magazynie: {row[9]} szt.")
            counter += 1
    else:
        print("Brak danych w bazie do wyświetlenia.")

    print("\n" + "="*80)
        
            
            
    # Krok 5 - zamknięcie połączenia
    if conn:
        conn.close()
        print("✓ Połączenie zamknięte - sensors.db zapisane na dysku")