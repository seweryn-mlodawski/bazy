from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')

print("DRIVER", engine.driver)

print("TABLES", engine.table_names())
    
print("SELECT", engine.execute("SELECT * FROM tasks"))

results = engine.execute("SELECT * FROM tasks")

for r in results:
   print(r)