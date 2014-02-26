import data
import parsers
import settings

def addData():
	#Open up the database

	start_time = time()
	db_path = "C:\\Users\\sjrumsby\\Documents\\Programming\\Python\\nhl_v5\\data.sqlite"
	if path.exists(db_path):
		con = sqlite3.connect(db_path)
		c = con.cursor()
	else:
		return {"status" : 1, "message" : "database doesn't exist... exiting (time elapsed: %.2f)" % float(time() - start_time) }

	#Remove all user-defined data in the database

	c.execute("Delete from hockey_team")
	c.execute("Delete from miss_types")
	c.execute("Delete from penalty_types")
	c.execute("Delete from play_types")
	c.execute("Delete from shot_types")
	c.execute("Delete from stop_types")
	c.execute("Delete from zone_types")
	con.commit()

	#Define all of our variables before importing

	teams 		= None
	miss_types 	= None
	penl_types 	= None
	play_types 	= None
	shot_types 	= None
	stop_types 	= None
	zone_types 	= None
	team_ids	= None
	players		= []

	#Import all of our data, and check that it imported correctly

	error = 0
	error_msg = []

	if teams is None:
		error = 1
		error_msg.append("No teams data found from import.")

	if miss_types is None:
		error = 1
		error_msg.append("No miss data found from import.")

	if penl_types is None:
		error = 1
		error_msg.append("No penalty data found from import.")

	if play_types is None:
		error = 1
		error_msg.append("No play data found from import.")

	if shot_types is None:
		error = 1
		error_msg.append("No shot data found from import.")

	if stop_types is None:
		error = 1
		error_msg.append("No stop data found form import.")

	if zone_types is None:
		error = 1
		error_msg.append("No zone data found from import.")

	if team_ids is None:
		error = 1
		error_msg.append("No team ID data found from import.")

	skater_urls = []
	goalie_urls = []

	url = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLSASALL&viewName=rtssPlayerStats&sort=gamesPlayed&pg="

	for i in range(1,29):
		uri = url + str(i)
		p = playerParser()
		req = urlopen(uri)
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
			players.append( [nhl_id, name, team_ids[team], y[4]] )

	url = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLGAGALL&viewName=summary&sort=wins&pg="

	for i in range(1,4):
		uri = url + str(i)
		p = playerParser()
		req = urlopen(uri)
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
			players.append( [nhl_id, name, team_ids[team], 'G'] )

	if error:
		for msg in error_msg:
			print "\t" + msg

		con.close()
		return {"status" : 1, "message" : "Exiting... (time elapsed: %.2f)" % float(time() - start_time) }
	else:
		"Data import complete..."

	try:	
		c.executemany('insert into hockey_team (name, long_name) values(?,?)', teams)
		c.executemany('insert into miss_types (name) values(?)', miss_types)
		c.executemany('insert into penalty_types (name) values(?)', penl_types)
		c.executemany('insert into play_types (name) values(?)', play_types)
		c.executemany('insert into shot_types (name) values(?)', shot_types)
		c.executemany('insert into stop_types (name) values(?)', stop_types)
		c.executemany('insert into zone_types (name) values(?)', zone_types)
		c.executemany('insert into skater (nhl_id, name, hockey_team_id, position) values (?, ?, ?, ?)', players)
		
		con.commit()

	except sqlite3.Error as e:
		con.close()
		return {"status" : 1, "message" : "An unexpected error occured inserting data: %s" % e.args[0] }
		
	con.close()
	return {"status" : 0, "message" :  "Complete. (time elapsed: %.2f)" % float(time() - start_time) }