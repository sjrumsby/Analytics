import os.path
import settings
import sqlite3

class Skater():
	nhlID = ""
	name = ""
	position = ""
	team = ""
	teamShort = ""
	gamesPlayed = 0
	goals = 0
	assists = 0
	points = 0
	plusMinus = 0
	
	def __init__(self, nhlID):
		print "Opening database"
		if os.path.exists(settings.database):
			self.con = sqlite3.connect(settings.database)
			self.c = self.con.cursor()
		else:
			exit ("Failed to open database")
			
		if nhlID.isdigit():
			self.nhlID = nhlID
		else:
			self.c.execute("SELECT nhl_id FROM skater WHERE name = '%s'" % nhlID)
			rows = self.c.fetchall()
			if len(rows) == 1:
				self.nhlID = rows[0][0]
			elif len(rows) == 0:
				raise Exception("No skater found with ID: %s" % self.nhlID)
			else:
				raise Exception("Too many skaters returned for ID: %s" % self.nhlID)
		
		self.c.execute("SELECT skater.name, skater.position, hockey_team.name, hockey_team.long_name FROM skater INNER JOIN hockey_team ON skater.hockey_team_id = hockey_team.id WHERE skater.nhl_id = %s" % self.nhlID)
		row = self.c.fetchone()
		self.name = row[0]
		self.position = row[1]
		self.teamShort = row[2]
		self.team = row[3]
	
	def printSelf(self):
		print "Name: %s" % self.name
		print "Position: %s" % self.position
		print "Team: %s" % self.team
		print "Games Played: %s" % self.gamesPlayed
		print "Goals: %s" % self.goals
		print "Assists: %s" % self.assists
		print "Points: %s" % self.points
		print "Plus Minus: %s" % self.plusMinus