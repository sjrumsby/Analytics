import os.path
import parsers
import settings
import sqlite3
import urllib2

def updateDatabase():
	uri = urllib2.urlopen("https://github.com/sjrumsby/Analytics/raw/master/data.sqlite")
	
	if os.path.exists(settings.database):
		print "deleting database"
		os.remove(settings.database)
		
	with open(settings.database, 'wb') as local_file:
		local_file.write(uri.read())
	
def removeAllData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }

	c.execute('SELECT tbl_name FROM sqlite_master WHERE type="table";')
	rows = c.fetchall()

	for x in rows:
		c.execute('DELETE FROM ' + x[0])

	con.commit()
	con.close()
	return 0