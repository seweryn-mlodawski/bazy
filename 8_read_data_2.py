SELECT * FROM tasks;
    Pobierz zadania dla danego projektu
        print(f"\n--- ZADANIA DLA PROJEKTU O ID {project_id} ---")
        for row in rows:
            print(row)
            In [2]: conn = create_connection("database.db")
In [3]: cur = conn.cursor()
In [4]: cur.execute("SELECT * FROM tasks")
Out[4]: <sqlite3.Cursor at 0x11088d5e0>
In [5]: rows = cur.fetchall()

In [6]: rows
Out[6]:
[(1,
  5,
  'Czasowniki regularne',
  'Zapamiętaj czasowniki ze strony 30',
  'started',
  '2020-05-11 12:00:00',
  '2020-05-11 15:00:00'),
 (2,
  6,
  'Czasowniki regularne',
  'Zapamiętaj czasowniki ze strony 30',
  'started',
  '2020-05-11 12:00:00',
  '2020-05-11 15:00:00'),
 (3,
  7,
  'Czasowniki regularne',
  'Zapamiętaj czasowniki ze strony 30',
  'started',
  '2020-05-11 12:00:00',
  '2020-05-11 15:00:00')]
In [8]: cur.execute("SELECT * FROM tasks")
Out[8]: <sqlite3.Cursor at 0x11088d5e0>

In [9]: cur.fetchone()
Out[9]:
(1,
 5,
 'Czasowniki regularne',
 'Zapamiętaj czasowniki ze strony 30',
 'started',
 '2020-05-11 12:00:00',
 '2020-05-11 15:00:00')

In [10]: cur.fetchone()
Out[10]:
(2,
 6,
 'Czasowniki regularne',
 'Zapamiętaj czasowniki ze strony 30',
 'started',
 '2020-05-11 12:00:00',
 '2020-05-11 15:00:00')

In [11]: cur.fetchone()
Out[11]:
(3,
 7,
 'Czasowniki regularne',
 'Zapamiętaj czasowniki ze strony 30',
 'started',
 '2020-05-11 12:00:00',
 '2020-05-11 15:00:00')

In [12]: cur.fetchone()

In [13]: