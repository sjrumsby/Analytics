import os.path
import parsers
import settings
import sqlite3
import urllib2
from time import time

def addHockeyTeamData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }

	c.execute("Delete from hockey_team")
	con.commit()

	error = 0
	
	if settings.hockey_teams is None:
		error = 1
		error_msg= "No teams data found from import."

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
	
	try:
		c.executemany('insert into hockey_team (id, name, long_name) values(?,?,?)', settings.hockey_teams)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
def addMissTypeData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }
		
	c.execute("Delete from miss_types")
	con.commit()

	error = 0

	if settings.miss_types is None:
		error = 1
		error_msg = "No miss data found from import."

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
	
	try:
		c.executemany('insert into miss_types (id, name) values(?, ?)', settings.miss_types)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
def addPenaltyTypeData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }
		
	c.execute("Delete from penalty_types")
	con.commit()

	error = 0

	if settings.penl_types is None:
		error = 1
		error_msg = "No penalty data found from import."

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
	
	try:
		c.executemany('insert into penalty_types (id, name) values(?, ?)', settings.penl_types)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
def addPlayTypeData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }
		
	c.execute("Delete from play_types")
	con.commit()
	
	error = 0

	if settings.play_types is None:
		error = 1
		error_msg = "No play data found from import."

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
		
	try:
		c.executemany('insert into play_types (id, name) values(?, ?)', settings.play_types)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }

def addShotTypeData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }

	c.execute("Delete from shot_types")
	con.commit()

	error = 0

	if settings.shot_types is None:
		error = 1
		error_msg = "No shot data found from import."

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
		
	try:
		c.executemany('insert into shot_types (id, name) values(?, ?)', settings.shot_types)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
def addStopTypeData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }
	
	c.execute("Delete from stop_types")
	con.commit()

	error = 0

	if settings.stop_types is None:
		error = 1
		error_msg = "No stop data found form import."
	
	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
	
	try:
		c.executemany('insert into stop_types (id, name) values(?, ?)', settings.stop_types)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
def addZoneTypeData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }
	
	c.execute("Delete from zone_types")
	con.commit()
	
	error = 0
	error_msg = []

	if settings.zone_types is None:
		error = 1
		error_msg = "No zone data found from import."

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }
	
	try:
		c.executemany('insert into zone_types (id, name) values(?, ?)', settings.zone_types)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
def addSkaterData():
	if os.path.exists(settings.database):
		con = sqlite3.connect(settings.database)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting." }
	
	error = 0
	
	if settings.hockey_team_ids is None:
		error = 1
		error_msg = "No team ID data found from import."

	players = []

	url = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLSASALL&viewName=rtssPlayerStats&sort=gamesPlayed&pg="

	for i in range(1,29):
		uri = url + str(i)
		p = parsers.playerParser()
		
		try:
			req = urllib2.urlopen(uri)
		except urllib2.HTTPError as e:
			con.close()
			return {"status" : 1, "message" : "HTTP Error raised for URL: %s\nError Code: %s" % (uri, e.code) }

		html = req.read()
		p.feed(html)

		for y in p.player:
			nhl_id = int(y[1])
			name = y[2]

			if y[3].find(",") > 0:
				parts = y[3].split(", ")
				team = parts[-1]
			else:
				team = y[3]
			players.append( [nhl_id, name, settings.hockey_team_ids[team], y[4]] )

	url = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLGAGALL&viewName=summary&sort=wins&pg="

	for i in range(1,4):
		uri = url + str(i)
		p = parsers.playerParser()

		try:
			req = urllib2.urlopen(uri)
		except urllib2.HTTPError as e:
			con.close()
			return {"status" : 1, "message" : "HTTP Error raised for URL: %s\nError Code: %s" % (uri, e.code) }
			
		html = req.read()
		p.feed(html)
		data = []

		for y in p.player:
			nhl_id = int(y[1])
			name = y[2]

			if y[3].find(",") > 0:
				parts = y[3].split(", ")
				team = parts[-1]
			else:
				team = y[3]
			players.append( [nhl_id, name, settings.hockey_team_ids[team], 'G'] )

	if error:
		con.close()
		return {"status" : 1, "message" : error_msg }

	try:	
		c.executemany('insert into skater (nhl_id, name, hockey_team_id, position) values (?, ?, ?, ?)', players)
		con.commit()
	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
			
	con.close()
	return {"status" : 0, "message" :  "Complete." }
	
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