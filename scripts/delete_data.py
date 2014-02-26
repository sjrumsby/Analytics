import sqlite3, sys
from os import path

#Open up the database

db_path = "C:\\Users\\sjrumsby\\Documents\\Programming\\Python\\nhl_v5\\data.sqlite"
if path.exists(db_path):
	con = sqlite3.connect(db_path)
	c = con.cursor()
else:
	print "database doesn't exist... exiting"
	exit()

c.execute('SELECT tbl_name FROM sqlite_master WHERE type="table";')
rows = c.fetchall()

for x in rows:
	c.execute('DELETE FROM ' + x[0])

con.commit()
print "Complete"
con.close()