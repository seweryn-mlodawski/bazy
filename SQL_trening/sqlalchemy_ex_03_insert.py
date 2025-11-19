# sqlalchemy_ex_03_insert.py
from sqlalchemy_ex_02 import students, engine # importuj tabelę i silnik z poprzedniego pliku, interpreter podkreśla błąd, ale działa poprawnie, to tylko warning

ins = students.insert() # przygotuj instrukcję wstawiania danych

ins = students.insert().values(name='Eric', lastname='Idle') # wstaw pojedynczy rekord

conn = engine.connect() # utwórz połączenie z bazą danych
result = conn.execute(ins) # wykonaj instrukcję wstawiania
# Wstaw wiele rekordów naraz
conn.execute(ins, [
   {'name': 'John', 'lastname': 'Cleese'},
   {'name': 'Graham', 'lastname': 'Chapman'},
])