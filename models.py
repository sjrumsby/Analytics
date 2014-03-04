import os.path
import parsers
import settings
import sqlite3
from parsers import summaryParser
from urllib2 import urlopen

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

class Game():
	id = 0
	gameID = 0
	yearID = 0
	seasonID = 0
	homeTeam = 0
	awayTeam = 0
	startTime = 0
	endTime = 0
	attendance = 0
	homeTeamSkaters = {}
	awayTeamSkaters = {}
	
	def __init__(self, gameID, yearID, seasonID):
		if os.path.exists(settings.database):
			self.con = sqlite3.connect(settings.database)
			self.c = self.con.cursor()
		else:
			exit ("Failed to open database")
		
		self.gameID = gameID
		self.yearID = yearID
		self.seasonID = seasonID
		
		self.c.execute("SELECT * FROM game WHERE season_code = %s AND year_code = %s AND game_code = %s" % (seasonID, yearID, gameID))
		row = self.c.fetchone()
		
		if row != None:
			if len(row) == 1:
				self.homeTeam = row[4]
				self.homeScore = row[5]
				self.awayTeam = row[6]
				self.awayScore = row[7]
				self.startTime = row[8]
				self.endTime = row[9]
				self.attendance = row[10]
			else:
				raise Exception("More than one game found")
		else:
			self.create()
		
		self.con.commit()

	def create(self):
		fp = "reports/" + self.yearID + "/GS/GS" + self.seasonID + self.gameID + ".HTML"
		if not os.path.exists(fp):
			print "Pulling summary data from NHL.com for game: %s" % self.gameID
			url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/GS" + self.seasonID + self.gameID + ".HTM"
			try:
				req = urlopen(url)
			except:
				print url
			sum_html = req.read()
		else:
			f = open(fp, 'r')
			sum_html = f.read()
			f.close()

		sumParse = parsers.summaryParser()
		sumParse.feed(sum_html)

		self.homeTeamID = settings.longNameToID[sumParse.home_team_data[2]]
		self.homeScore = sumParse.home_team_data[1]
		self.awayTeamID = settings.longNameToID[sumParse.away_team_data[2]]
		self.awayScore = sumParse.away_team_data[1]
		self.startTime = sumParse.summary_data[6]
		self.endTime = sumParse.summary_data[8]
		self.attendance = sumParse.summary_data[2].split(" ")[-1].replace(",", "")
		
		if not self.attendance.isdigit():
			self.attendance = 0
		
		executeString = "INSERT INTO game(season_code, year_code, game_code, home_team_id, home_score, away_team_id, away_score, start_time, end_time, attendance) VALUES (%s, %s, %s, %s, %s, %s, %s, '%s', '%s', %s)" % (self.seasonID, self.yearID, self.gameID, self.homeTeamID, self.homeScore, self.awayTeamID, self.awayScore, self.startTime, self.endTime, self.attendance)
		self.c.execute(executeString)
		executeString = "SELECT id FROM game WHERE season_code = '%s' AND year_code = '%s' AND game_code = '%s'" % (int(self.seasonID), int(self.yearID), int(self.gameID))
		self.c.execute(executeString)
		row = self.c.fetchone()
		self.id = row[0]

		fp = "reports/" + self.yearID + "/BX/BX" + self.seasonID + self.gameID + ".HTML"
		if not os.path.exists(fp):
			print "Pulling boxscore data from NHL.com for game: %s" % gameID
			url = "http://www.nhl.com/gamecenter/en/boxscore?id=" + self.yearID[0:4] + self.seasonID + self.gameID
			req = urlopen(url)
			box_html = req.read()
		else:
			f = open(fp, 'r')
			box_html = f.read()
			f.close()

		boxParse = parsers.boxParser()
		boxParse.feed(box_html)
		
		teamInsert = []
		
		for t in boxParse.away_skaters:
			teamInsert.append([t[1], self.id, t[0], self.awayTeamID])
			self.awayTeamSkaters[t[0]] = t[1]

		for t in boxParse.away_goalies:
			teamInsert.append([t[1], self.id, t[0], self.awayTeamID])
			self.awayTeamSkaters[t[0]] = t[1]
			
		for t in boxParse.home_skaters:
			teamInsert.append([t[1], self.id, t[0], self.awayTeamID])
			self.homeTeamSkaters[t[0]] = t[1]
			
		for t in boxParse.home_goalies:
			teamInsert.append([t[1], self.id, t[0], self.awayTeamID])
			self.homeTeamSkaters[t[0]] = t[1]

		executeString = "INSERT INTO team(skater_id, game_id, number, hockey_team_id) VALUES (?, ?, ?, ?)"
		self.c.executemany("INSERT INTO team(skater_id, game_id, number, hockey_team_id) VALUES (?, ?, ?, ?)", teamInsert)

		stars = []
		
		for x in sumParse.stars_data:
			number = x[3].split(" ")[0]
			if x[1] == "S.J":
				hockey_team_name = "SJS"
			elif x[1] == "N.J":
				hockey_team_name = "NJD"
			elif x[1] == "T.B":
				hockey_team_name = "TBL"
			elif x[1] == "L.A":
				hockey_team_name = "LAK"
			else:
				hockey_team_name = x[1]
				
			if self.homeTeamID == settings.shortNameToID[hockey_team_name]:
				stars.append(self.homeTeamSkaters[number])
			else:
				stars.append(self.awayTeamSkaters[number])	
		if len(stars) == 3:
			self.c.execute("INSERT INTO stars(game_id, first_id, second_id, third_id) VALUES (%s, %s, %s, %s)" % (self.id, stars[0], stars[1], stars[2]))
		elif len(stars) == 1:
			self.c.execute("INSERT INTO stars(game_id, first_id) VALUES (%s, %s)" % (self.id, stars[0]))
		elif len(stars) == 2:
			self.c.execute("INSERT INTO stars(game_id, first_id, second_id) VALUES (%s, %s, %s)" % (self.id, stars[0], stars[1]))

		fp = "reports/" + self.yearID + "/PL/PL" + self.seasonID + self.gameID + ".HTML"

		if not os.path.exists(fp):
			print "Pulling play-by-play data from NHL.com for game: %s" % self.gameID
			url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/PL" + self.seasonID + self.gameID + ".HTM"
			print url
			req = urlopen(url)
			play_html = req.read()
		else:
			f = open(fp, 'r')
			play_html = f.read()
			f.close()
		
		print "parsing play data"
		playParse = parsers.playParser()
		playParse.feed(play_html)
		
		insertPlays = []
		insertFaceOff = []
		
		for p in playParse.plays:
			if p['play'][4] in ["PSTR", "STOP", "PEND", "GEND", "SOC", "EISTR", "EIEND"]:
				self.c.execute("INSERT INTO play("") VALUES ()")
				insertPlays.append([self.id, settings.play_types_reverse[p['play'][4]], p['play'][1], p['play'][2], ""]) 
			else:
				insertPlays.append([self.id, settings.play_types_reverse[p['play'][5]], p['play'][1], p['play'][3], settings.strength_types_reverse[p['play'][2]]]) 

			if p['play'][5] == "FAC":
				faceOffPlay = [self.c.lastrowid] 
				faceOffPlay.append(x for x in self.processFaceOff(p) )
				insertFaceOff.append( { 'play' : faceOffPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )
		
		for x in insertFaceOff:
			print x
			print "\n\n"
			
		print "parsed"
		
	def processFaceOff(self, play):
		parts = play.split(" - ")
		winningTeam = parts[0][0:3]
		zone = parts[0][8:11]

		if zone == "Neu":
			zone_id = zone_types_reverse["Neutral"]
		elif zone == "Def":
			zone_id = settings.zone_types_reverse["Defensive"]
		elif zone == "Off":
			zone_id = settings.zone_types_reverse["Offensive"]
		else:
			print "An unknown error occured processing the play: %s" % play
		
		if settings.shortNameToID[winningTeam] == self.homeTeam:
			winningTeamID = self.homeTeam
			losingTeamID = self.awayTeam
		else:
			winningTeamID = self.awayTeam
			winningTeamID = self.homeTeam

		players = parts[1].split(" vs ")

		playerOneParts = players[0].split("#")
		playerOneTeam = playerOneParts[0][0:3]
		playerOneNumber = playerOneParts[1][0:2]

		playerTwoParts = players[1].split("#")
		playerTwoTeam = playerTwoParts[0][0:3]
		playerTwoNumber = playerTwoParts[1][0:2]

		if self.homeTeam == settings.shortNameToID[playerOneTeam]:
			winner = self.homeTeamSkaters[playerOneNumber]
			loser = self.awayTeamSkaters[playerTwoNumber]
		else:
			winner = self.homeTeamSkaters[playerTwoNumber]
			loser = self.awayTeamSkaters[playerOneNumber]

		return [winner, loser, zone_id]
















