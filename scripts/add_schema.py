import sqlite3, sys
from os import path

#Open up the database

db_path = "C:\\Users\\sjrumsby\\Documents\\Programming\\Python\\nhl_v5\\data.sqlite"
if path.exists(db_path):
	con = sqlite3.connect(db_path)
	c = con.cursor()
else:
	print "database doesn't exist... exiting"
	exit()
	
#Define all our table strings

hockey_team_tbl = None
skat_tbl 		= None
miss_tbl 		= None
penl_tbl 		= None
play_tbl 		= None
shot_tbl 		= None
stop_tbl 		= None
zone_tbl 		= None
game_tbl		= None
star_tbl		= None
team_tbl		= None
	
from schema import *

error = 0
error_msg = []

if hockey_team_tbl is None:
	error = 1
	error_msg.append("Hockey_team table schema not defined in schema.py")
	
if skat_tbl is None:
	error = 1
	error_msg.append("Skater table schema not deinfed in schema.py")
	
if miss_tbl is None:
	error = 1
	error_msg.append("miss_type table schema not defined in schema.py")
	
if penl_tbl is None:
	error = 1
	error_msg.append("penalty_type table schema not defined in schema.py")
	
if play_tbl is None:
	error = 1
	error_msg.append("play_type table schema not defined in schema.py")
	
if shot_tbl is None:
	error = 1
	error_msg.append("shot_type table schema not defined in schema.py")
	
if stop_tbl is None:
	error = 1
	error_msg.append("stop_type table schema not defined in schema.py")
	
if zone_tbl is None:
	error = 1
	error_msg.append("zone_type table schema not definde in schema.py")
	
if game_tbl is None:
	error = 1
	error_msg.append("game table schema not defined in schema.py")
	
if star_tbl is None:
	error = 1
	error_msg.append("star table schema not defined in schema.py")

if team_tbl is None:
	error = 1
	error_msg.append("team table schema not defined in schema.py")

if error:
	print "Errors importing data:"
	for msg in error_msg:
		print "\t" + msg
	print "Exiting..."
	con.close()
	exit()
else:
	"Data import complete..."

print "Adding tables..."

try:
	c.execute(hockey_team_tbl)
	c.execute(skat_tbl)
	c.execute(miss_tbl)
	c.execute(penl_tbl)
	c.execute(play_tbl)
	c.execute(shot_tbl)
	c.execute(stop_tbl)
	c.execute(zone_tbl)
	c.execute(game_tbl)
	c.execute(star_tbl)
	c.execute(team_tbl)
except sqlite3.Error as e:
	print "An unexpected error occured creating tables: " + e.args[0]

con.commit()
print "Complete"
con.close()