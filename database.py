import sqlite3

conn = sqlite3.connect("mydatabase.db")
# conn.row_factory = sqlite3.Row
cursor = conn.cursor()



sql = "SELECT * FROM stocks WHERE ticker = 'mtss'"
cursor.execute(sql)

print(cursor.fetchall()[0][2])