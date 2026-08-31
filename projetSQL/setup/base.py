def creer_base(): 
    import sqlite3
    conn = sqlite3.connect("boutique.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()
    with open("setup/schema.sql") as f:
        contenu = f.read()
    cur.executescript(contenu) 
    conn.commit()
    print("base créer avec succès")
    conn.close()