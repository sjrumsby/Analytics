import game
import HTMLParser
from HTMLParser import HTMLParser
from urllib2 import urlopen
import os
import schema
import settings
import sqlite3
import time

class playerParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.table = 0
		self.rec = 0
		self.player_data = []
		self.player = []
		self.count = 0

	def handle_starttag(self, tag, attributes):
		if tag == "table":
			for name, value in attributes:
				if name == "class" and value == "data stats":
					self.table = 1
					
		if self.table:
			if tag == 'tr':
				self.rec = 1
			if self.count == 1:
				for name, value in attributes:
					if name=='href':
						id = value.split('=')
						id = id[1]
						self.player_data.append(id)

	def handle_data(self, data):
		if self.rec:
			self.player_data.append(data)
			self.count = self.count + 1

	def handle_endtag(self, tag):
		if tag == 'tr' and self.rec:
			if '\nPlayer\n' not in self.player_data and ' | ' not in self.player_data:
				self.player.append(self.player_data)
			self.rec = 0
			self.player_data = []
			self.count = 0
		if tag == 'tbody':
			self.table = 0

seasonID = "02"
gameID = "0001"
yearID = "20132014"

startTime = time.time()
os.remove(settings.database)
con = sqlite3.connect(settings.database)
c = con.cursor()

st = time.time()
print "Building database..."

c.execute(schema.hockey_team_table)
c.execute(schema.skater_table)
c.execute(schema.miss_type_table)
c.execute(schema.penalty_type_table)
c.execute(schema.play_type_table)
c.execute(schema.shot_type_table)
c.execute(schema.stop_type_table)
c.execute(schema.zone_type_table)
c.execute(schema.strength_type_table)
c.execute(schema.game_table)
c.execute(schema.star_table)
c.execute(schema.team_table)
c.execute(schema.play_table)
c.execute(schema.face_off_table)
c.execute(schema.home_face_off_on_ice) 
c.execute(schema.away_face_off_on_ice) 
c.execute(schema.block_table)
c.execute(schema.home_block_on_ice)
c.execute(schema.away_block_on_ice)
c.execute(schema.shot_table)
c.execute(schema.home_shot_on_ice)
c.execute(schema.away_shot_on_ice)
c.execute(schema.hit_table)
c.execute(schema.home_hit_on_ice)
c.execute(schema.away_hit_on_ice)
c.execute(schema.stop_table)
c.execute(schema.home_stop_on_ice)
c.execute(schema.away_stop_on_ice)
c.execute(schema.miss_table)
c.execute(schema.home_miss_on_ice)
c.execute(schema.away_miss_on_ice)

for x in settings.hockey_teams:
	c.execute('INSERT INTO hockey_team(id, name, long_name) VALUES (%s, "%s", "%s")' % (x[0], x[1], x[2]))

for x in settings.miss_types:
	c.execute('INSERT INTO miss_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))

for x in settings.penl_types:
	c.execute('INSERT INTO penalty_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))
	
for x in settings.play_types:
	c.execute('INSERT INTO play_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))

for x in settings.shot_types:
	c.execute('INSERT INTO shot_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))

for x in settings.stop_types:
	c.execute('INSERT INTO stop_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))

for x in settings.strength_types:
	c.execute('INSERT INTO strength_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))

for x in settings.zone_types:
	c.execute('INSERT INTO zone_types(id, name) VALUES (%s, "%s")' % (x[0], x[1]))

con.commit()
print "Done. (%.3f s)" % float(time.time() - st)

st = time.time()
print "Adding all players from nhl.com..."

players = []
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
		players.append( [nhl_id, name, settings.shortNameToID[team], y[4]] )

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
		players.append( [nhl_id, name, settings.shortNameToID[team], 'G'] )

c.executemany('insert into skater (nhl_id, name, hockey_team_id, position) values (?, ?, ?, ?)', players)
con.commit()
print "Done. (%.3f s)" % float(time.time() - st)


for i in range(1, 101):
	st = time.time()
	print "Creating game: %s..." % i
	g = game.Game(str(i).zfill(4), yearID, seasonID)
	print "Done. (%.3f s)" % float(time.time() - st)

c.execute("SELECT * FROM game WHERE season_code = %s AND year_code = %s AND game_code = %s" % (seasonID, yearID, gameID))
generalRow = c.fetchone()

print "General Game Data:\n"
print "\tHome Team: %s" % settings.idToLongName[generalRow[4]]
print "\tHome Score: %s" % generalRow[5] 
print "\tAway Team: %s" % settings.idToLongName[generalRow[6]]
print "\tAway Score: %s" % generalRow[7] 
print "\tAttendance: %s" % generalRow[10]

print "\n"

c.execute("SELECT * FROM shot WHERE game_id = %s" % g.id)
rows = c.fetchall()
print "Shots Data:"
for x in rows:
	print x
	
print "All games added. (%.3f)" % float(time.time() - startTime)