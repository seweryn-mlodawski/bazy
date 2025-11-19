# sqlalchemy_ex_04_select.py
from sqlalchemy import create_engine, MetaData, Integer, String, Table, Column # importuje potrzebne komponenty SQLAlchemy

engine = create_engine('sqlite:///database.db', echo=True) # tworzy silnik połączony z bazą danych SQLite echo=True włącza logowanie SQL

meta = MetaData() # tworzenie obiektu MetaData do przechowywania definicji tabel

# definiowanie tabeli students
students = Table(
   'students', meta, 
   Column('id', Integer, primary_key=True),
   Column('name', String),
   Column('lastname', String),
)

conn = engine.connect() # utwórz połączenie z bazą danych
s = students.select().where(students.c.id > 2) # przygotuj instrukcję wyboru z warunkiem id > 2 
result = conn.execute(s) # wykonaj instrukcję wyboru

# wyświetl wyniki

for row in result:
   print(row)