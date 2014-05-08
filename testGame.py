import game
import settings
import sqlite3
import schema
import os
import time

seasonID = "02"
gameID = "0001"
yearID = "20132014"

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

g = game.Game(gameID, yearID, seasonID)
print g.id

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