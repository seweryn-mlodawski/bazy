# ex_02_create_tables.py

import sqlite3 # import the sqlite3 library
from sqlite3 import Error # import the Error class
from tkinter import INSERT # import INSERT constant - 

def create_connection(db_file): 
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None # inicjalizacja zmiennej conn jako None
   try:
       conn = sqlite3.connect(db_file) # próba połączenia z bazą danych
       return conn
   except Error as e:
       print(e)

   return conn

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor() # utworzenie kursora
       c.execute(sql) # kursor wykonana zapytania SQL
   except Error as e:
       print(e)

if __name__ == "__main__":

   create_projects_sql = """
   -- projects table
   CREATE TABLE IF NOT EXISTS projects (
      id integer PRIMARY KEY,
      nazwa text NOT NULL,
      start_date text,
      end_date text
   );
   """

   create_tasks_sql = """
   -- zadanie table
   CREATE TABLE IF NOT EXISTS tasks (
      id integer PRIMARY KEY,
      project_id integer NOT NULL,
      nazwa VARCHAR(250) NOT NULL,
      opis TEXT,
      status VARCHAR(15) NOT NULL,
      start_date text NOT NULL,
      end_date text NOT NULL,
      FOREIGN KEY (project_id) REFERENCES projects (id)
   );
   """

   db_file = "database.db"

   conn = create_connection(db_file)
   if conn is not None:
       execute_sql(conn, create_projects_sql)
       execute_sql(conn, create_tasks_sql)
       
       insert_project_sql = """
       INSERT INTO projects (id, nazwa, start_date, end_date)
       VALUES (?, ?, ?, ?);
       """
       # powyżej i poniżej - jest to lepszy sposób wstawiania danych niż bezpośrednie wpisywanie wartości w SQL
       # ze względu na bezpieczeństwo przed SQL Injection

       project_data = [
           (1, "Zrób to dobrze", "2024-01-01 00:00:00", "2024-06-30 23:59:59"),
            (2, "Naucz się Pythona", "2024-02-01 00:00:00", "2024-07-31 23:59:59"),
            (3, "Zbuduj aplikację", "2024-03-01 00:00:00", "2024-08-31 23:59:59")
       ]
       
       c = conn.cursor() # utworzenie kursora
       # dla każdego projektu w liście project_data wykonaj zapytanie insert_project_sql z danymi projektu
       for project in project_data:
           c.execute(insert_project_sql, project) # wykonanie zapytania z danymi z listy
       conn.commit() # zatwierdzenie zmian w bazie danych
       
       ## Krok po kroku, co się dzieje:
    #    1. **`c.execute(sql, project)`** — kursor wysyła zapytanie SQL do bazy z danymi z krotki `project`
    #    2. Kursor wstawia każdy projekt do tabeli `projects`
    #    3. **`conn.commit()`** — zatwierdza wszystkie zmiany (bez tego nic się nie zapisze!)
       
       
       