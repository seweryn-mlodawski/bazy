# ex_02_create_tables.py

import sqlite3
from sqlite3 import Error
from tkinter import INSERT

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
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
       c = conn.cursor()
       c.execute(sql)
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
       
       c = conn.cursor()
       for project in project_data:
           c.execute(insert_project_sql, project)
       conn.commit()
       #execute_sql(conn, insert_project_sql)
       #
       #conn.commit()
       #conn.close()