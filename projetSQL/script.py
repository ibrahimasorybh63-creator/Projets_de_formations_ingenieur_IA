import sqlite3
conn = sqlite3.connect("boutique.db")
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()
with open("schema.sql") as f:
    contenu = f.read()
cur.executescript(contenu) #ordre1
conn.commit()
cur.execute("select name from sqlite_master where type='table';") #ordre2
view = cur.fetchall()
print(view)
conn.close()