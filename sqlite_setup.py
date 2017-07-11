import sqlite3

conn = sqlite3.connect('dashboard.db')
c = conn.cursor()
c.execute("CREATE TABLE token (token text, last_token real)")
c.execute("INSERT INTO token VALUES ('aa',0.0)")
conn.commit()

conn.close()
