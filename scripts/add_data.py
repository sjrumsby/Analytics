import sqlite3, sys
from HTMLParser import HTMLParser
from urllib2 import urlopen
from os import path
from time import time

#HTMLParser for fetching players from NHL.com

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

#Open up the database

start_time = time()
db_path = "C:\\Users\\sjrumsby\\Documents\\Programming\\Python\\nhl_v5\\data.sqlite"
if path.exists(db_path):
	con = sqlite3.connect(db_path)
	c = con.cursor()
else:
	print "database doesn't exist... exiting (time elapsed: %.2f)" % float(time() - start_time)
	exit()
	
#Remove all data in the database

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
	
print "Importing data..."
error = 0
error_msg = []

try:
	from data import *
except:
	print "Unexpected error:", sys.exc_info()[0]
	
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
	
print "Fetching all player data from nhl.com..."

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
	print "Errors importing data:"
	for msg in error_msg:
		print "\t" + msg
	print "Exiting... (time elapsed: %.2f)" % float(time() - start_time)
	con.close()
	exit()
else:
	"Data import complete..."
	
#Insert all of our data

try:	
	print "Adding teams..."
	c.executemany('insert into hockey_team (name, long_name) values(?,?)', teams)
	con.commit()

	print "Adding miss types..."
	c.executemany('insert into miss_types (name) values(?)', miss_types)
	con.commit()

	print "Adding penalty types..."
	c.executemany('insert into penalty_types (name) values(?)', penl_types)
	con.commit()

	print "Adding play types..."
	c.executemany('insert into play_types (name) values(?)', play_types)
	con.commit()

	print "Adding shot types..."
	c.executemany('insert into shot_types (name) values(?)', shot_types)
	con.commit()

	print "Adding stop types..."
	c.executemany('insert into stop_types (name) values(?)', stop_types)
	con.commit()

	print "Adding zone types..."
	c.executemany('insert into zone_types (name) values(?)', zone_types)
	con.commit()

	print "Adding NHL players..."
	c.executemany('insert into skater (nhl_id, name, hockey_team_id, position) values (?, ?, ?, ?)', players)
	con.commit()

except sqlite3.Error as e:
	print "An unexpected error occured inserting data: ", e.args[0]

print "Complete. (time elapsed: %.2f)" % float(time() - start_time)
con.close()