import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute("""SELECT * FROM FIGHTERS ORDER BY WINS DESC""")

most_wins = c.fetchall()
for i, fighter in enumerate(most_wins[:30]):
	print(i+1, fighter[1], fighter[2], fighter[17])
print(len(most_wins))


conn.close()