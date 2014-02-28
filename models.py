import os.path
import parsers
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
			else:
				exit("Invalid NHL_ID for skater: %s" % nhlID)
		
		self.c.execute("SELECT skater.name, skater.position, hockey_team.name, hockey_team.long_name FROM skater INNER JOIN hockey_team ON skater.hockey_team_id = hockey_team.id WHERE skater.nhl_id = %s" % self.nhlID)
		row = self.c.fetchone()
		self.name = row[0]
		self.position = row[1]
		self.teamShort = row[2]
		self.team = row[3]

'''
class Game():
	gameID = 0
	yearID = 0
	seasonID = 0
	home_players = []
	away_players = []
	Game = None
	sum_parse = None
	box_parse = None
	play_parse = None
	
	def __init__(self, gameID, yearID, seasonID):
		self.gameID = gameID
		self.yearID = yearID
		self.seasonID = seasonID
		self.sum_parse = summaryParser.summaryParser()
		self.box_parse = boxParser.boxParser()
		self.play_parse = playParser.playParser()
		
				
		if Game.objects.filter(game_code=gameID).count() == 0:
			self.Game = Game.objects.create(game_code=gameID, season_code=seasonID, year_code=yearID)
		else:
			self.Game = Game.objects.filter(season_code=seasonID).filter(game_code=gameID).filter(year_code=yearID)[0]
			
		fp = "reports/"+str(self.yearID)+"/BX/BX"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/gamecenter/en/boxscore?id="+str(self.yearID)[0:4]+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)
			print url
			req = urlopen(url)
			html = req.read()
		else:
			f = open(fp, 'r')
			html = f.read()
			f.close()
		
		self.box_parse.feed(html)
		
		fp = "reports/"+str(self.yearID)+"/GS/GS"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/scores/htmlreports/"+str(self.yearID)+"/GS"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTM"
			print url
			req = urlopen(url)
			html = req.read()
		else:
			f = open(fp, 'r')
			html = f.read()
			f.close()
			
		self.sum_parse.feed(html)
		
		fp = "reports/"+str(self.yearID)+"/PL/PL"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/scores/htmlreports/"+str(self.yearID)+"/PL"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTM"
			print url
			req = urlopen(url)
			html = req.read()
		else:
			f = open(fp, 'r')
			html = f.read()
			f.close()
			
		self.play_parse.feed(html)
		
		if len(self.sum_parse.summary_data) != 21:
			print "Error in summary parsing."
			for x in self.sum_parse.summary_data:
				print x
			exit()

	def __str__(self):
		return "Game id: %s" % self.id
		
	def get_player(self, x):
		return Skater.objects.get(nhl_id=x[1])
		
	def get_team_skater(self, number, team):
		if team == "home":
			t = Team.objects.filter(number=number, hockey_team=self.Game.home_team)
		else:
			t = Team.objects.filter(number=number, hockey_team=self.Game.away_team)
		if t.count() == 1:
			return t[0]
		else:
			return None
		
	def game_save(self):
		self.Game.save()
		
	def parse_game(self):
		self.Game.home_team = Hockey_Team.objects.filter(long_name=self.sum_parse.summary_data[18])[0]
		self.Game.away_team = Hockey_Team.objects.filter(long_name=self.sum_parse.summary_data[2])[0]
		attendance_parts = self.sum_parse.summary_data[6].split(" ")
		self.Game.attendance = re.sub(",", "", attendance_parts[-1])
		self.Game.start_time = self.sum_parse.summary_data[10]
		self.Game.end_time = self.sum_parse.summary_data[12]
		
		Team.objects.filter(game=self.Game).delete()
		
		for x in self.box_parse.away_skaters:
			t= Team.objects.create(skater=self.get_player(x), game=self.Game, number = int(x[0]), hockey_team=self.Game.away_team)
			t.save()
			
		for x in self.box_parse.away_goalies:
			t= Team.objects.create(skater=self.get_player(x), game=self.Game, number = int(x[0]), hockey_team=self.Game.away_team)
			t.save()
			
		for x in self.box_parse.home_skaters:
			t= Team.objects.create(skater=self.get_player(x), game=self.Game, number = int(x[0]), hockey_team=self.Game.home_team)
			t.save()
			
		for x in self.box_parse.home_goalies:
			t= Team.objects.create(skater=self.get_player(x), game=self.Game, number = int(x[0]), hockey_team=self.Game.home_team)
			t.save()

		stars = []
		
		for x in self.sum_parse.stars_data:
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
			error = 0
			
			if self.Game.home_team.name == hockey_team_name:
				t = Team.objects.filter(game=self.Game, number=number, hockey_team=self.Game.home_team)
				if len(t) == 1:
					stars.append(t[0])
				else:
					error = 1
			if self.Game.away_team.name == hockey_team_name:
				t = Team.objects.filter(game=self.Game, number=number, hockey_team=self.Game.away_team)
				if len(t) == 1:
					stars.append(t[0])
				else:
					error = 1
					
			if error == 1:
				print "Something went wrong with parameters:"
				print "GameID: %s" % self.gameID
				print "seasonID: %s" % self.seasonID
				print "yearID: %s" % self.yearID
				print x
				print "Summary data crap for testing:"
				for y in self.sum_parse:
					print y
				exit()
		
		if len(stars) == 3:
			if Stars.objects.filter(game=self.Game).count() == 0:
				s = Stars.objects.create(game=self.Game, first = stars[0].skater, second = stars[1].skater, third = stars[2].skater)
			else:
				s = Stars.objects.filter(game=self.Game)[0]
				s.first = stars[0].skater
				s.second = stars[1].skater
				s.third = stars[2].skater
			s.save()
		self.Game.save()
		
		for x in self.play_parse.plays:
			print "Processing play: %s" % x['play']
			if Play_Type.objects.filter(name=x['play'][5]).count() == 1:
				p = Play_Type.objects.filter(name=x['play'][5])[0]
				p = Play.objects.create(game=self.Game, type=p, description = x['play'][6])
				p.save()
				for y in x['home']:
					p.on_ice.add(self.get_team_skater(y, "home"))
				for y in x['away']:
					p.on_ice.add(self.get_team_skater(y, "away"))
			
	def parse_plays(self):
		fp = "reports/"+str(self.yearID)+"/PL/PL"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTML"
		if not os.path.exists(fp):
			url = "http://www.nhl.com/scores/htmlreports/"+str(self.yearID)+"/PL"+str(self.seasonID).zfill(2)+str(self.gameID).zfill(4)+".HTM"
			print url
			req = urlopen(url)
			html = req.read()
		else:
			f = open(fp, 'r')
			html = f.read()
			f.close()
			
		self.play_parse.feed(html)
		
		for x in self.play_parse.plays:
			print x['play']
			print x['home']
			print x['away']
'''