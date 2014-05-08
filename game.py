import os.path
import parsers
import settings
import sqlite3
from parsers import summaryParser, boxParser, playParser
from urllib2 import urlopen
import sys
import traceback

class Game():
	id = 0
	gameID = 0
	yearID = 0
	seasonID = 0
	homeTeam = ""
	homeTeamShortName = ""
	homeTeamID = 0
	awayTeam = 0
	awayTeamShortName = ""
	awayTeamID = 0
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
		row = self.c.fetchall()
		
		if row != None:
			if len(row) == 1:
				row = row[0]
				self.homeTeam = row[4]
				self.homeScore = row[5]
				self.awayTeam = row[6]
				self.awayScore = row[7]
				self.startTime = row[8]
				self.endTime = row[9]
				self.attendance = row[10]
			elif len(row) > 1:
				raise Exception("More than one game found")
			elif len(row) == 0:
				self.create()
			else:
				raise Exception("An unknown error occured creating game with gameID = %s, seasonID = %s, yearID = %s" % (self.gameID, self.seasonID, self.yearID))
		
		self.con.commit()

	def create(self):				
		fp = "reports/" + self.yearID + "/GS/GS" + self.seasonID + self.gameID + ".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/GS" + self.seasonID + self.gameID + ".HTM"
			try:
				req = urlopen(url)
				sum_html = req.read()
			except:
				print url
			
		else:
			f = open(fp, 'r')
			sum_html = f.read()
			f.close()

		sumParse = parsers.summaryParser()
		sumParse.feed(sum_html)

		self.homeTeam = sumParse.home_team_data[2].strip()
		self.homeTeamShortName = settings.longNameToShortName[self.homeTeam]
		self.homeTeamID = settings.longNameToID[self.homeTeam]
		self.homeScore = sumParse.home_team_data[1]
		
		self.awayTeam = sumParse.away_team_data[2].strip()
		self.awayTeamShortName = settings.longNameToShortName[self.awayTeam]
		self.awayTeamID = settings.longNameToID[self.awayTeam]
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
			hockey_team_name = self.convertHockeyTeamName(x[1])
				
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
			url = "http://www.nhl.com/scores/htmlreports/" + self.yearID + "/PL" + self.seasonID + self.gameID + ".HTM"
			print url
			req = urlopen(url)
			play_html = req.read()
		else:
			f = open(fp, 'r')
			play_html = f.read()
			f.close()
		
		playParse = parsers.playParser()
		playParse.feed(play_html)
		
		insertPlays 	= []
		insertFaceOff	= []
		insertBlock	 	= []
		insertShot 		= []
		insertMiss 		= []
		insertHit 		= []
		insertStop 		= []
		
		try:
			for p in playParse.plays:
				if p['play'][4] in ["PSTR", "STOP", "PEND", "GEND", "SOC", "EISTR", "EIEND"]:
					executeString = "INSERT INTO play(game_id, event_id, period, time) VALUES (%s, %s, %s, '%s')" % (self.id, settings.play_types_reverse[p['play'][4]], p['play'][1], p['play'][2])
					if settings.debug: print executeString
					self.c.execute(executeString)
					
					if p['play'][4] == "STOP":

						stopPlay = [self.c.lastrowid]

						for x in self.processStop(p['play'][5]):
							stopPlay.append(x)

						insertStop.append( { 'play' : stopPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )
				else:
					executeString = "INSERT INTO play(game_id, event_id, period, time, strength_id) VALUES (%s, %s, %s, '%s', %s)" % (self.id, settings.play_types_reverse[p['play'][5]], p['play'][1], p['play'][4], settings.strength_types_reverse[p['play'][2]] )
					if settings.debug: print executeString
					self.c.execute(executeString)

					if p['play'][5] == "FAC":
						faceOffPlay = [self.c.lastrowid] 

						for x in self.processFaceOff(p['play'][6]):
							faceOffPlay.append(x)

						insertFaceOff.append( { 'play' : faceOffPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )

					elif p['play'][5] == "BLOCK":
						blockPlay = [self.c.lastrowid]

						for x in self.processBlock(p['play'][6]):
							blockPlay.append(x)

						insertBlock.append( { 'play' : blockPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )

					elif p['play'][5] == "SHOT":
						shotPlay = [self.c.lastrowid]

						for x in self.processShot(p['play'][6]):
							shotPlay.append(x)

						insertShot.append( { 'play' : shotPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )

					elif p['play'][5] == "MISS":
						missPlay = [self.c.lastrowid]

						for x in self.processMiss(p['play'][6]):
							missPlay.append(x)

						insertMiss.append( { 'play' : missPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )

					elif p['play'][5] == "HIT":
						hitPlay = [self.c.lastrowid]

						for x in self.processHit(p['play'][6]):
							hitPlay.append(x)

						insertHit.append( { 'play' : hitPlay, 'home' : [self.homeTeamSkaters[x] for x in p['home'] ],  'away' : [self.awayTeamSkaters[x] for x in p['away'] ] } )

		except Exception as e:
			if p['play'][4] != "GOFF":
				print "An unknown error occured: %s" % e.message
				print"\n"
				print sys.exc_info()
				print "\n"
				print traceback.print_tb(sys.exc_info()[2])
				print "\n"
				print p

		for x in insertFaceOff:
			executeString = "INSERT INTO face_off(game_id, play_id, winner, loser, zone_id) VALUES (%s, %s, %s, %s, %s)" % (self.id, x['play'][0], x['play'][1], x['play'][2], x['play'][3])
			if settings.debug: print executeString
			self.c.execute(executeString)
			face_off_id = self.c.lastrowid
			
			for y in x['home']:
				self.c.execute("INSERT INTO home_face_off_on_ice (face_off_id, skater_id) VALUES (%s, %s)" % (face_off_id, y))
			
			for z in x['away']:
				self.c.execute("INSERT INTO away_face_off_on_ice (face_off_id, skater_id) VALUES (%s, %s)" % (face_off_id, z))
		
		for x in insertBlock:
			executeString = "INSERT INTO block(game_id, play_id, shooter, blocker, shot_type_id, zone_type_id) VALUES (%s, %s, %s, %s, %s, %s)" % (self.id, x['play'][0], x['play'][1], x['play'][2], x['play'][3], x['play'][4])
			if settings.debug: print executeString
			self.c.execute(executeString)
			block_id = self.c.lastrowid
			
			for y in x['home']:
				self.c.execute("INSERT INTO home_block_on_ice (block_id, skater_id) VALUES (%s, %s)" % (block_id, y))
			
			for z in x['away']:
				self.c.execute("INSERT INTO away_block_on_ice (block_id, skater_id) VALUES (%s, %s)" % (block_id, z))

		for x in insertShot:
			executeString = "INSERT INTO shot(game_id, play_id, shooter, shot_type_id, zone_type_id, distance) VALUES (%s, %s, %s, %s, %s, %s)" % (self.id, x['play'][0], x['play'][1], x['play'][2], x['play'][3], x['play'][4])
			if settings.debug: print executeString
			self.c.execute(executeString)
			shot_id = self.c.lastrowid

			for y in x['home']:
				self.c.execute("INSERT INTO home_shot_on_ice (shot_id, skater_id) VALUES (%s, %s)" % (shot_id, y))
			
			for z in x['away']:
				self.c.execute("INSERT INTO away_shot_on_ice (shot_id, skater_id) VALUES (%s, %s)" % (shot_id, z))
				
		for x in insertMiss:
			executeString = "INSERT INTO miss(game_id, play_id, shooter, miss_type_id, shot_type_id, zone_type_id, distance) VALUES (%s, %s, %s, %s, %s, %s, %s)" % (self.id, x['play'][0], x['play'][1], x['play'][2], x['play'][3], x['play'][4], x['play'][5])
			if settings.debug: print executeString
			self.c.execute(executeString)
			miss_id = self.c.lastrowid
			
			for y in x['home']:
				self.c.execute("INSERT INTO home_miss_on_ice (miss_id, skater_id) VALUES (%s, %s)" % (miss_id, y))
			
			for z in x['away']:
				self.c.execute("INSERT INTO away_miss_on_ice (miss_id, skater_id) VALUES (%s, %s)" % (miss_id, z))
				
		for x in insertHit:
			executeString = "INSERT INTO hit(game_id, play_id, hitter, hittee, zone_type_id) VALUES (%s, %s, %s, %s, %s)" % (self.id, x['play'][0], x['play'][1], x['play'][2], x['play'][3])
			if settings.debug: print executeString
			self.c.execute(executeString)
			hit_id = self.c.lastrowid
			
			for y in x['home']:
				self.c.execute("INSERT INTO home_hit_on_ice (hit_id, skater_id) VALUES (%s, %s)" % (hit_id, y))
			
			for z in x['away']:
				self.c.execute("INSERT INTO away_hit_on_ice (hit_id, skater_id) VALUES (%s, %s)" % (hit_id, z))
				
		for x in insertStop:
			executeString = "INSERT INTO stop(game_id, play_id, stop_type_id) VALUES (%s, %s, %s)" % (self.id, x['play'][0], x['play'][1])
			if settings.debug: print executeString
			self.c.execute(executeString)
			stop_id = self.c.lastrowid
			
			for y in x['home']:
				self.c.execute("INSERT INTO home_stop_on_ice (stop_id, skater_id) VALUES (%s, %s)" % (stop_id, y))
				
			for z in x['away']:
				self.c.execute("INSERT INTO away_stop_on_ice (stop_id, skater_id) VALUES (%s, %s)" % (stop_id, z))
				
#All of the functions for parsing the data out of individual plays

	def convertHockeyTeamName(self, team):
		if team == "S.J":
			return "SJS"
		elif team == "N.J":
			return "NJD"
		elif team == "T.B":
			return "TBL"
		elif team == "L.A":
			return "LAK"
		else:
			return team
			
	def convertZoneName(self, zone):
		if zone == "Neu":
			return settings.zone_types_reverse["Neutral"]
		elif zone == "Def":
			return settings.zone_types_reverse["Defensive"]
		elif zone == "Off":
			return settings.zone_types_reverse["Offensive"]
		else:
			print "An unknown error occured processing the zone: %s" % zone
		
	def processFaceOff(self, play):
		parts = play.split(" - ")
		winningTeam = self.convertHockeyTeamName(parts[0][0:3])
		zone = parts[0][8:11]
		
		zone_id = self.convertZoneName(zone)
		
		if settings.shortNameToID[self.convertHockeyTeamName(winningTeam)] == self.homeTeamID:
			winningTeamID = self.homeTeam
			losingTeamID = self.awayTeam
		else:
			winningTeamID = self.awayTeam
			winningTeamID = self.homeTeam

		players = parts[1].split(" vs ")

		playerOneParts = players[0].split("#")
		playerOneTeam = self.convertHockeyTeamName(playerOneParts[0][0:3].strip())
		playerOneNumber = playerOneParts[1][0:2].strip()

		playerTwoParts = players[1].split("#")
		playerTwoTeam = self.convertHockeyTeamName(playerTwoParts[0][0:3].strip())
		playerTwoNumber = playerTwoParts[1][0:2].strip()

		if self.homeTeamID == settings.shortNameToID[self.convertHockeyTeamName(playerOneTeam)]:
			winner = self.homeTeamSkaters[playerOneNumber]
			loser = self.awayTeamSkaters[playerTwoNumber]
		else:
			winner = self.homeTeamSkaters[playerTwoNumber]
			loser = self.awayTeamSkaters[playerOneNumber]

		return [winner, loser, zone_id]

	def processBlock(self, play):
		parts = play.split(" BLOCKED BY ")
		shootingTeam = self.convertHockeyTeamName(parts[0][0:3])
		shooter = parts[0].split("#")[1][0:2].strip()
		parts = parts[1].split(", ")
		blocker = parts[0].split("#")[1][0:2].strip()
		shot_type_id = settings.shot_types_reverse[parts[1].strip()]
		zone_type_id = self.convertZoneName(parts[2].split(". ")[0].strip())
				
		if self.homeTeamID == settings.shortNameToID[self.convertHockeyTeamName(shootingTeam)]:
			shooter = self.homeTeamSkaters[shooter]
			blocker = self.awayTeamSkaters[blocker]
		else:
			blocker = self.homeTeamSkaters[blocker]
			shooter = self.awayTeamSkaters[shooter]
		
		return [shooter, blocker, shot_type_id, zone_type_id]

	def processShot(self, play):
		team = play[0:3]
		
		parts = play.split('#')
		shooter = parts[1][0:2].strip()
		parts = parts[1].split(", ")
		
		if len(parts) == 4:
			shot_type_id = settings.shot_types_reverse[parts[1].strip()]
			zone_type_id = self.convertZoneName(parts[2].split(". ")[0].strip())
			distance = parts[3].split(" ")[0].strip()

		else:
#Gotta add some shit here to process penalty shots
			shot_type_id = settings.shot_types_reverse[parts[2].strip()]
			zone_type_id = self.convertZoneName(parts[3].split(". ")[0].strip())
			distance = parts[4].split(" ")[0].strip()

		if self.homeTeamID == settings.shortNameToID[ self.convertHockeyTeamName(team)]:
			shooter = self.homeTeamSkaters[shooter]
		else:
			shooter = self.awayTeamSkaters[shooter]
		
		return [shooter, shot_type_id, zone_type_id, distance]
		
	def processMiss(self, play):
		team = play[0:3]
		
		parts = play.split("#")
		shooter = parts[1][0:2].strip()
		parts = parts[1].split(", ")
		shot_type_id = settings.shot_types_reverse[parts[1].strip()]
		
		shot = parts[2].strip()
		
		if shot == "Wide of Net":
			miss_type_id = settings.miss_types_reverse["Wide"]
		elif shot == "Hit Crossbar":
			miss_type_id = settings.miss_types_reverse["Crossbar"]
		elif shot == "Goalpost":
			miss_type_id = settings.miss_types_reverse["Post"]
		elif shot == "Over Net":
			miss_type_id = settings.miss_types_reverse["Over"]
		else:
			raise Exception("An unknown miss type was found for play: %s" % play)
		
		zone_type_id = self.convertZoneName(parts[3].split(". ")[0].strip())
		distance = parts[4].split(" ")[0].strip()
		
		if self.homeTeamID == settings.shortNameToID[self.convertHockeyTeamName(team)]:
			shooter = self.homeTeamSkaters[shooter]
		else:
			shooter = self.awayTeamSkaters[shooter]
			
		return [shooter, miss_type_id, shot_type_id, zone_type_id, distance]

	def processHit(self, play):
		team = play[0:3]
		
		parts = play.split("#")
		hitter = parts[1][0:2].strip()
		hittee = parts[2][0:2].strip()
		zone_type_id = self.convertZoneName(parts[2].split(", ")[1].split(". ")[0].strip())
		
		if self.homeTeamID == settings.shortNameToID[self.convertHockeyTeamName(team)]:
			hitter = self.homeTeamSkaters[hitter]
			hittee = self.awayTeamSkaters[hittee]
		else:
			hitter = self.awayTeamSkaters[hitter]
			hittee = self.homeTeamSkaters[hittee]
		
		return [hitter, hittee, zone_type_id]
	
	def processStop(self,play):
		play = play.split(",")[0].strip()
	
		if play == "PUCK FROZEN":
			stop_type_id = settings.stop_types_reverse["Frozen"]
		elif play == "GOALIE STOPPED":
			stop_type_id = settings.stop_types_reverse["Goalie"]
		elif play == "ICING":
			stop_type_id = settings.stop_types_reverse["Icing"]
		elif play == "HAND PASS":
			stop_type_id = settings.stop_types_reverse["Hand Pass"]
		elif play == "HIGH STICK":
			stop_type_id = settings.stop_types_reverse["High Stick"]
		elif play == "PLAYER INJURY": 
			stop_type_id = settings.stop_types_reverse["Injury"]
		elif play == "PUCK IN BENCHES":
			stop_type_id = settings.stop_types_reverse["In Benches"]
		elif play == "PUCK IN CROWD":
			stop_type_id = settings.stop_types_reverse["In Crowd"]
		elif play == "PUCK IN NETTING":
			stop_type_id = settings.stop_types_reverse["In Netting"]
		elif play == "NET OFF":
			stop_type_id = settings.stop_types_reverse["Net Off"]
		elif play == "TV TIMEOUT":
			stop_type_id = settings.stop_types_reverse["TV Timeout"]
		elif play == "OFFICIAL INJURY":
			stop_type_id = settings.stop_types_reverse["Official Injury"]
		elif play == "OFFSIDE":
			stop_type_id = settings.stop_types_reverse["Offside"]
		elif play == "REFEREE OR LINESMAN":
			stop_type_id = settings.stop_types_reverse["Referee or Linesman"]
		elif play == "PLAYER EQUIPMENT":
			stop_type_id = settings.stop_types_reverse["Player Equipment"]
		elif play == "VISITOR TIMEOUT":
			stop_type_id = settings.stop_types_reverse["Visitor Timeout"]
		elif play == "HOME TIMEOUT":
			stop_type_id = settings.stop_types_reverse["Home Timeout"]
		elif play == "CLOCK PROBLEM":
			stop_type_id = settings.stop_types_reverse["Clock Problem"]
		elif play == "VIDEO REVIEW":
			stop_type_id = settings.stop_types_reverse["Video Review"]
		elif play == "RINK REPAIR":
			stop_type_id = settings.stop_types_reverse["Rink Repair"]
		else:
			raise Exception ("Unknown stop type for play: %s" % play)
		
		return [stop_type_id]







