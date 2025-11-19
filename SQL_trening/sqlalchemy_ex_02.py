# sqlalchemy_ex_02.py
from sqlalchemy import Table, Column, Integer, String, MetaData # Import necessary SQLAlchemy components
from sqlalchemy import create_engine # Import create_engine to connect to the database

engine = create_engine('sqlite:///database.db', echo=True) # Create an engine connected to a SQLite database

meta = MetaData() # Tworzenie obiektu MetaData do przechowywania definicji tabel

students = Table(
   'tasks', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String),
   Column('lastname', String),
)

meta.create_all(engine) # Tworzenie tabeli w bazie danych
print(engine.table_names())