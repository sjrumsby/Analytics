from HTMLParser import HTMLParser
from urllib2 import urlopen
from threading import Thread
from Queue import Queue
from parsers import *
import datetime
import os
import sys
import time
import traceback
import vars
			
#These classes are used to increase speed of getting all players from NHL.com

class playerThreadHTML(object):
    def __init__(self, url):
        self.url = url
        self.html = ""
        self.players = []
    
    def getData(self):
		p = playerParser()
		p.feed(self.html)

		for y in p.player:
			nhl_id = int(y[1])
			name = y[2]

			if y[3].find(",") > 0:
				parts = y[3].split(", ")
				team = parts[-1]
			else:
				team = y[3]

			player = [nhl_id, name, vars.shortNameToID[team], y[4]]
			self.players.append(player)

class goalieThreadHTML(object):
    def __init__(self, url):
        self.url = url
        self.html = ""
        self.players = []

    def getData(self):
		p = playerParser()
		p.feed(self.html)

		for y in p.player:
			nhl_id = int(y[1])
			name = y[2]

			if y[3].find(",") > 0:
				parts = y[3].split(", ")
				team = parts[-1]
			else:
				team = y[3]

			player = [nhl_id, name, vars.shortNameToID[team], y[4]]
			self.players.append(player)

def playerWorker():
	while True:
		t = q.get()
		req = urlopen(t.url)
		t.html = req.read()
		t.getData()
		q.task_done()

def goalieWorker():
	while True:
		t = q.get()
		req = urlopen(t.url)
		t.html = req.read()
		t.getData()
		q.task_done()

#Helper functions for the parseGame function

def convertHockeyTeamName(team):
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

def convertZoneName(zone):
	if zone == "Neu":
		return vars.zone_types_reverse["Neutral"]
	elif zone == "Def":
		return vars.zone_types_reverse["Defensive"]
	elif zone == "Off":
		return vars.zone_types_reverse["Offensive"]
	else:
		print "An unknown error occured processing the zone: %s" % zone

def processFaceOff(play):
	parts = play.split(" - ")
	zone = parts[0][8:11]
	zone_id = convertZoneName(zone)
	players = parts[1].split(" vs ")

	playerOneParts = players[0].split("#")
	playerOneNumber = playerOneParts[1][0:2].strip()

	playerTwoParts = players[1].split("#")
	playerTwoNumber = playerTwoParts[1][0:2].strip()

	return [playerOneNumber, playerTwoNumber, zone_id]

def processBlock(play):
	parts = play.split(" BLOCKED BY ")
	shootingTeam = convertHockeyTeamName(parts[0][0:3])
	shooter = parts[0].split("#")[1][0:2].strip()
	parts = parts[1].split(", ")
	blocker = parts[0].split("#")[1][0:2].strip()
	shot_type_id = vars.shot_types_reverse[parts[1].strip()]
	zone_type_id = convertZoneName(parts[2].split(". ")[0].strip())

	return [shooter, blocker, shot_type_id, zone_type_id]

def processShot(play):
	team = play[0:3]

	parts = play.split('#')
	shooter = parts[1][0:2].strip()
	parts = parts[1].split(", ")

	if len(parts) == 4:
		shot_type_id = vars.shot_types_reverse[parts[1].strip()]
		zone_type_id = convertZoneName(parts[2].split(". ")[0].strip())
		distance = parts[3].split(" ")[0].strip()
	else:
		shot_type_id = vars.shot_types_reverse[parts[2].strip()]
		zone_type_id = convertZoneName(parts[3].split(". ")[0].strip())
		distance = parts[4].split(" ")[0].strip()

	return [shooter, shot_type_id, zone_type_id, distance]

def processMiss(play):
	team = play[0:3]

	parts = play.split("#")
	shooter = parts[1][0:2].strip()
	parts = parts[1].split(", ")
	shot_type_id = vars.shot_types_reverse[parts[1].strip()]

	shot = parts[2].strip()

	if shot == "Wide of Net":
		miss_type_id = vars.miss_types_reverse["Wide"]
	elif shot == "Hit Crossbar":
		miss_type_id = vars.miss_types_reverse["Crossbar"]
	elif shot == "Goalpost":
		miss_type_id = vars.miss_types_reverse["Post"]
	elif shot == "Over Net":
		miss_type_id = vars.miss_types_reverse["Over"]
	else:
		raise Exception("An unknown miss type was found for play: %s" % play)

	zone_type_id = convertZoneName(parts[3].split(". ")[0].strip())
	distance = parts[4].split(" ")[0].strip()

	return [shooter, miss_type_id, shot_type_id, zone_type_id, distance]

def processHit(play):
	team = play[0:3]

	parts = play.split("#")
	hitter = parts[1][0:2].strip()
	hittee = parts[2][0:2].strip()
	zone_type_id = convertZoneName(parts[2].split(", ")[1].split(". ")[0].strip())

	return [hitter, hittee, zone_type_id]

def processStop(play):
	play = play.split(",")[0].strip()

	if play == "PUCK FROZEN":
		stop_type_id = vars.stop_types_reverse["Frozen"]
	elif play == "GOALIE STOPPED":
		stop_type_id = vars.stop_types_reverse["Goalie"]
	elif play == "ICING":
		stop_type_id = vars.stop_types_reverse["Icing"]
	elif play == "HAND PASS":
		stop_type_id = vars.stop_types_reverse["Hand Pass"]
	elif play == "HIGH STICK":
		stop_type_id = vars.stop_types_reverse["High Stick"]
	elif play == "PLAYER INJURY": 
		stop_type_id = vars.stop_types_reverse["Injury"]
	elif play == "PUCK IN BENCHES":
		stop_type_id = vars.stop_types_reverse["In Benches"]
	elif play == "PUCK IN CROWD":
		stop_type_id = vars.stop_types_reverse["In Crowd"]
	elif play == "PUCK IN NETTING":
		stop_type_id = vars.stop_types_reverse["In Netting"]
	elif play == "NET OFF":
		stop_type_id = vars.stop_types_reverse["Net Off"]
	elif play == "TV TIMEOUT":
		stop_type_id = vars.stop_types_reverse["TV Timeout"]
	elif play == "OFFICIAL INJURY":
		stop_type_id = vars.stop_types_reverse["Official Injury"]
	elif play == "OFFSIDE":
		stop_type_id = vars.stop_types_reverse["Offside"]
	elif play == "REFEREE OR LINESMAN":
		stop_type_id = vars.stop_types_reverse["Referee or Linesman"]
	elif play == "PLAYER EQUIPMENT":
		stop_type_id = vars.stop_types_reverse["Player Equipment"]
	elif play == "VISITOR TIMEOUT":
		stop_type_id = vars.stop_types_reverse["Visitor Timeout"]
	elif play == "HOME TIMEOUT":
		stop_type_id = vars.stop_types_reverse["Home Timeout"]
	elif play == "CLOCK PROBLEM":
		stop_type_id = vars.stop_types_reverse["Clock Problem"]
	elif play == "VIDEO REVIEW":
		stop_type_id = vars.stop_types_reverse["Video Review"]
	elif play == "RINK REPAIR":
		stop_type_id = vars.stop_types_reverse["Rink Repair"]
	else:
		raise Exception ("Unknown stop type for play: %s" % play)

	return [stop_type_id]

def processGoal(play):
	team = play[0:3]
	parts = play.split("#")
	shooter = parts[1][0:2].strip()

	return [shooter]

def processGoalShot(play):
	team = play[0:3]
	parts = play.split("#")
	shooter = parts[1][0:2].strip()

	parts = parts[1].split(", ")
	if len(parts) == 4:
		shot_type_id = vars.shot_types_reverse[parts[1].strip()]
		zone_type_id = convertZoneName(parts[2].split(". ")[0].strip())
		distance = parts[3].split(" ")[0].strip()
	elif len(parts) == 3:
		shot_type_id = vars.shot_types_reverse["Undefined"]
		zone_type_id = convertZoneName(parts[1].split(". ")[0].strip())
		distance = parts[2].split(" ")[0].strip()
	elif len(parts) == 5:
		shot_type_id = vars.shot_types_reverse[parts[2].strip()]
		zone_type_id = convertZoneName(parts[3].split(". ")[0].strip())
		distance = parts[4].split(" ")[0].strip()

	return [shooter, shot_type_id, zone_type_id, distance]

def processGiveaway(play):
	parts = play.split("#")
	skater = parts[1][0:2].strip()

	return [ skater ]

def processTakeaway(play):
	parts = play.split("#")
	skater = parts[1][0:2].strip()

	return [ skater ]

def processPeriodStart(play):
	parts = play.split("Local time: ")
	time = parts[1][0:5]

	return time

def processPeriodEnd(play):
	parts = play.split("Local time: ")
	time = parts[1][0:5]

	return time

#Function to parse all the game and play-by-play data

def parseGame(seasonID, gameID, yearID):
	homeTeamSkaters = {}
	awayTeamSkaters = {}
	
	fp = "reports/" + yearID + "/GS/GS" + seasonID + gameID + ".HTML"
	if not os.path.exists(fp):
		url = "http://www.nhl.com/scores/htmlreports/" + yearID + "/GS" + seasonID + gameID + ".HTM"
		try:
			req = urlopen(url)
			sum_html = req.read()
		except:
			print url

	else:
		f = open(fp, 'r')
		sum_html = f.read()
		f.close()

	sumParse = summaryParser()
	sumParse.feed(sum_html)

	homeTeam = sumParse.home_team_data[2].strip()
	homeTeamShortName = vars.longNameToShortName[homeTeam]
	homeTeamID = vars.longNameToID[homeTeam]
	homeScore = sumParse.home_team_data[1]

	awayTeam = sumParse.away_team_data[2].strip()
	awayTeamShortName = vars.longNameToShortName[awayTeam]
	awayTeamID = vars.longNameToID[awayTeam]
	awayScore = sumParse.away_team_data[1]

	startTime = sumParse.summary_data[6]
	endTime = sumParse.summary_data[8]
	attendance = sumParse.summary_data[2].split(" ")[-1].replace(",", "")

	if not attendance.isdigit():
		attendance = 0
		print "No attendance found"
	
	date = datetime.datetime.strptime(sumParse.summary_data[1], '%A, %B %d, %Y')
	startTime = datetime.time(int(startTime.split(':')[0]), int(startTime.split(':')[1]))
	startTime = datetime.time(int(endTime.split(':')[0]), int(endTime.split(':')[1]))
	
	g = Game.objects.create(game_id=gameID,
						year_id=yearID,
						season_id=seasonID,
						date=date,
						home_team_id=homeTeamID,
						away_team_id=awayTeamID,
						home_score=homeScore,
						away_score=awayScore,
						attendance=attendance,
						start_time=startTime,
						end_time=endTime,
						)

	fp = "reports/" + yearID + "/BX/BX" + seasonID + gameID + ".HTML"
	if not os.path.exists(fp):
		url = "http://www.nhl.com/gamecenter/en/boxscore?id=" + yearID[0:4] + seasonID + gameID
		req = urlopen(url)
		box_html = req.read()
	else:
		f = open(fp, 'r')
		box_html = f.read()
		f.close()

	boxParse = boxParser()
	boxParse.feed(box_html)

	teamInsert = []

	for t in boxParse.away_skaters:
		teamInsert.append([t[1], t[0], awayTeamID])
		awayTeamSkaters[t[0]] = t[1]

	for t in boxParse.away_goalies:
		teamInsert.append([t[1], t[0], awayTeamID])
		awayTeamSkaters[t[0]] = t[1]

	for t in boxParse.home_skaters:
		teamInsert.append([t[1], t[0], homeTeamID])
		homeTeamSkaters[t[0]] = t[1]

	for t in boxParse.home_goalies:
		teamInsert.append([t[1], t[0], homeTeamID])
		homeTeamSkaters[t[0]] = t[1]

	Team.objects.bulk_create([Team(skater_id=x,game_id=g.id,hockey_team_id=y,number=z) for x,y,z in teamInsert])

	stars = []

	for x in sumParse.stars_data:
		number = x[3].split(" ")[0]
		hockey_team_name = convertHockeyTeamName(x[1])

		if homeTeamID == vars.shortNameToID[hockey_team_name]:
			stars.append(homeTeamSkaters[number])
		else:
			stars.append(awayTeamSkaters[number])	
	
	if len(stars) == 3:
		Stars.objects.create(game_id=g.id, first_star_id=stars[0],second_star_id=stars[1],third_star_id=stars[2])
	elif len(stars) == 1:
		Stars.objects.create(game_id=g.id, first_star_id=stars[0])
	elif len(stars) == 2:
		Stars.objects.create(game_id=g.id, first_star_id=stars[0],second_star_id=stars[1])
	else:
		print "An unknown error occurred with game: %s." % g.id
		return

	fp = "reports/" + yearID + "/PL/PL" + seasonID + gameID + ".HTML"

	if not os.path.exists(fp):
		url = "http://www.nhl.com/scores/htmlreports/" + yearID + "/PL" + seasonID + gameID + ".HTM"
		print url
		req = urlopen(url)
		play_html = req.read()
	else:
		f = open(fp, 'r')
		play_html = f.read()
		f.close()

	playParse = playParser()
	playParse.feed(play_html)

	insertPlay 		= []
	insertFaceOff		= []
	insertBlock	 		= []
	insertShot 			= []
	insertMiss 			= []
	insertHit 			= []
	insertStop 			= []
	insertGoal			= []
	insertTake			= []
	insertGive			= []
	insertPeriodEnd 	= []
	insertPeriodStart 	= []

	try:
		for p in playParse.plays:
			if p['play'][4] in ["PSTR", "STOP", "PEND", "GEND", "SOC", "EISTR", "EIEND"]:
				play_time = datetime.time(0,int(p['play'][2].split(':')[0]), int(p['play'][2].split(':')[1]))
				insertPlay.append(Play(game_id=g.id,event_id=vars.play_types_reverse[p['play'][4]],period=p['play'][1],time=play_time))
			else:
				play_time = datetime.time(0,int(p['play'][4].split(':')[0]), int(p['play'][4].split(':')[1]))
				insertPlay.append(Play(game_id=g.id,event_id=vars.play_types_reverse[p['play'][5]],period=p['play'][1],time=play_time,strength_id=vars.strength_types_reverse[p['play'][2]]))

	except Exception as e:
		if p['play'][4] != "GOFF":
			print "An unknown error occured: %s" % e.message
			print"\n"
			print sys.exc_info()
			print "\n"
			print traceback.print_tb(sys.exc_info()[2])
			print "\n"
			print p
	
	Play.objects.bulk_create(insertPlay)
'''
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

	for x in insertGoal:
		executeString = "INSERT INTO goal(game_id, play_id, scorer) VALUES (%s, %s, %s)" % (self.id, x['play'][0], x['play'][1])
		if settings.debug: print executeString
		self.c.execute(executeString)
		goal_id = self.c.lastrowid

		for y in x['home']:
			self.c.execute("INSERT INTO home_goal_on_ice (goal_id, skater_id) VALUES (%s, %s)" % (goal_id, y))

		for z in x['away']:
			self.c.execute("INSERT INTO away_goal_on_ice (goal_id, skater_id) VALUES (%s, %s)" % (goal_id, z))

	for x in insertGive:
		executeString = "INSERT INTO give(game_id, play_id, giver) VALUES (%s, %s, %s)" % (self.id, x['play'][0], x['play'][1])
		if settings.debug: print executeString
		self.c.execute(executeString)
		give_id = self.c.lastrowid

		for y in x['home']:
			self.c.execute("INSERT INTO home_give_on_ice (give_id, skater_id) VALUES (%s, %s)" % (give_id, y))

		for z in x['away']:
			self.c.execute("INSERT INTO away_give_on_ice (give_id, skater_id) VALUES (%s, %s)" % (give_id, z))

	for x in insertTake:
		executeString = "INSERT INTO take(game_id, play_id, taker) VALUES (%s, %s, %s)" % (self.id, x['play'][0], x['play'][1])
		if settings.debug: print executeString
		self.c.execute(executeString)
		take_id = self.c.lastrowid

		for y in x['home']:
			self.c.execute("INSERT INTO home_take_on_ice (take_id, skater_id) VALUES (%s, %s)" % (take_id, y))

		for z in x['away']:
			self.c.execute("INSERT INTO away_take_on_ice (take_id, skater_id) VALUES (%s, %s)" % (take_id, z))

	for x in insertPeriodStart:
		executeString = "INSERT INTO pstr(game_id, play_id, time) VALUES (%s, %s, %s)" % (self.id, x['play'][0], x['play'][1])
		if settings.debug: print executeString
		self.c.execute(executeString)
		pstr_id = self.c.lastrowid

		for y in x['home']:
			self.c.execute("INSERT INTO home_pstr_on_ice (pstr_id, skater_id) VALUES (%s, %s)" % (pstr_id, y))

		for z in x['away']:
			self.c.execute("INSERT INTO away_pstr_on_ice (pstr_id, skater_id) VALUES (%s, %s)" % (pstr_id, z))

	for x in insertPeriodEnd:
		executeString = "INSERT INTO pend(game_id, play_id, time) VALUES (%s, %s, %s)" % (self.id, x['play'][0], x['play'][1])
		if settings.debug: print executeString
		self.c.execute(executeString)
		pend_id = self.c.lastrowid

		for y in x['home']:
			self.c.execute("INSERT INTO home_pend_on_ice (pend_id, skater_id) VALUES (%s, %s)" % (pend_id, y))

		for z in x['away']:
			self.c.execute("INSERT INTO away_pend_on_ice (pend_id, skater_id) VALUES (%s, %s)" % (pend_id, z))
'''

#Now we'll actually start with data

if os.path.exists(vars.database):
	if len(sys.argv) == 2:
		if sys.argv[1] == "clear":
			try:
				os.remove(vars.database)
				os.system('python manage.py syncdb')

			except Exception:
				print("Could not remove database. Exiting...")
				exit()
else:
	os.system('python manage.py syncdb')

from django.conf import settings

settings.configure(	DATABASES = 	{ 'default': {
										'ENGINE': 'django.db.backends.sqlite3',
										'NAME': vars.database, 
										'USER': '',
										'PASSWORD': '',
										'HOST': '',
										'PORT': '',
									}
								},
					INSTALLED_APPS = ('data',),
					)

from django.db import models
from data.models import *

seasonID = "02"
gameID = "0001"
yearID = "20132014"

startTime = time.time() 
st = time.time()
sys.stdout.write("Clearing the database... ")
returnCode = os.system('python manage.py flush --noinput -v 0')

if returnCode != 0:
	sys.stdout.write("Clearing data manually... ")
	Home_Period_Start_On_Ice.objects.all().delete()
	Away_Period_Start_On_Ice.objects.all().delete()
	Home_Period_End_On_Ice.objects.all().delete()
	Away_Period_End_On_Ice.objects.all().delete()
	Home_Giveaway_On_Ice.objects.all().delete()
	Away_Giveaway_On_Ice.objects.all().delete()
	Home_Takeaway_On_Ice.objects.all().delete()
	Away_Takeaway_On_Ice.objects.all().delete()
	Home_Goal_On_Ice.objects.all().delete()
	Away_Goal_On_Ice.objects.all().delete()
	Home_Face_Off_On_Ice.objects.all().delete()
	Away_Face_Off_On_Ice.objects.all().delete()
	Home_Block_On_Ice.objects.all().delete()
	Away_Block_On_Ice.objects.all().delete()
	Home_Shot_On_Ice.objects.all().delete()
	Away_Shot_On_Ice.objects.all().delete()
	Home_Hit_On_Ice.objects.all().delete()
	Away_Hit_On_Ice.objects.all().delete()
	Home_Stop_On_Ice.objects.all().delete()
	Away_Stop_On_Ice.objects.all().delete()
	Home_Miss_On_Ice.objects.all().delete()
	Away_Miss_On_Ice.objects.all().delete()
	Period_Start.objects.all().delete()
	Period_End.objects.all().delete()
	Goal.objects.all().delete()
	Giveaway.objects.all().delete()
	Takeaway.objects.all().delete()
	Face_Off.objects.all().delete()
	Block.objects.all().delete()
	Shot.objects.all().delete()
	Hit.objects.all().delete()
	Stop.objects.all().delete()
	Miss.objects.all().delete()
	Play.objects.all().delete()
	Team.objects.all().delete()
	Stars.objects.all().delete()
	Miss_Type.objects.all().delete()
	Penalty_Type.objects.all().delete()
	Play_Type.objects.all().delete()
	Shot_Type.objects.all().delete()
	Stop_Type.objects.all().delete()
	Strength_Type.objects.all().delete()
	Zone_Type.objects.all().delete()
	Skater.objects.all().delete()
	Game.objects.all().delete()
	Hockey_Team.objects.all().delete()

print "Done. (%.2f s)" % float(time.time() - st)
sys.stdout.write("Adding Types... ")
st = time.time()

Hockey_Team.objects.bulk_create([Hockey_Team(id=x, name=y, full_name=z) for x,y,z in vars.hockey_teams])
Miss_Type.objects.bulk_create([Miss_Type(id=x, name=y) for x,y in vars.miss_types])
Penalty_Type.objects.bulk_create([Penalty_Type(id=x, name=y) for x,y in vars.penl_types])
Play_Type.objects.bulk_create([Play_Type(id=x, name=y) for x,y in vars.play_types])
Shot_Type.objects.bulk_create([Shot_Type(id=x, name=y) for x,y in vars.shot_types])
Stop_Type.objects.bulk_create([Stop_Type(id=x, name=y) for x,y in vars.stop_types])
Strength_Type.objects.bulk_create([Strength_Type(id=x, name=y) for x,y in vars.strength_types])
Zone_Type.objects.bulk_create([Zone_Type(id=x, name=y) for x,y in vars.zone_types])
	

print "Done. (%.2f s)" % float(time.time() - st)

st = time.time()
sys.stdout.write("Adding all players from nhl.com... ")

players = []
playerURL = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLSASALL&viewName=rtssPlayerStats&sort=gamesPlayed&pg="
goalieURL = "http://www.nhl.com/ice/playerstats.htm?fetchKey=20142ALLGAGALL&viewName=summary&sort=wins&pg="
playerHTML = []
goalieHTML = []

q = Queue()

playerHTMLItems = [playerThreadHTML(playerURL + str(i)) for i in range(1,32)]

for i in range(vars.concurrent):
	t = Thread(target=playerWorker)
	t.daemon=True
	t.start()

for x in playerHTMLItems:
	q.put(x)

q.join()

goalieHTMLItems = [goalieThreadHTML(goalieURL + str(i)) for i in range(1,5)]

for i in range(vars.concurrent):
	t = Thread(target=goalieWorker)
	t.daemon=True
	t.start()

for x in goalieHTMLItems:
	q.put(x)

q.join()

for x in playerHTMLItems:
	for y in x.players:
		if y not in players:
			players.append(y)

for x in goalieHTMLItems:
	for y in x.players:
		if y not in players:
			players.append(y)
	
Skater.objects.bulk_create([Skater(nhl_id=w,name=x,hockey_team_id=y,position=z) for w,x,y,z in players])
print "Done. (%.2f s)" % float(time.time() - st)
st = time.time()
sys.stdout.write("Adding game play-by-play... ")

for i in range(1,2):
	seasonID = "02"
	gameID = "0001"
	yearID = "20132014"
	
	parseGame(seasonID, gameID, yearID)
	

print "Done. (%.3f s)" % float(time.time() - st)

print "All games added. (%.2f)" % float(time.time() - startTime)