from os import path, mkdir
from urllib2 import urlopen, HTTPError

base_url = "http://www.nhl.com/scores/htmlreports/"
box_url = "http://www.nhl.com/gamecenter/en/boxscore?id="
base_path = "reports/"

games = [{'year':'20132014', 'games' : 1230}, { 'year' : '20122013', 'games' : 720}, {'year' : '20112012', 'games' : 1230}]

for x in games:
	if not path.exists(base_path + x['year']):
		mkdir(base_path + x['year'])
		
	if not path.exists(base_path + x['year'] + "/BX"):
		mkdir(base_path + x['year'] + "/BX")
			
	if not path.exists(base_path + x['year'] + "/PL"):
		mkdir(base_path + x['year'] + "/PL")
			
	if not path.exists(base_path + x['year'] + "/GS"):
		mkdir(base_path + x['year'] + "/GS")
		
	for i in range(1, x['games']+1):
		game_uri = base_url + x['year'] + "/GS02" + str(i).zfill(4) + ".HTM"
		play_uri = base_url + x['year']  + "/PL02" + str(i).zfill(4) + ".HTM"
		box_uri = box_url + x['year'][0:4] + "02" + str(i).zfill(4) + "&navid=sb:boxscore"
		
		game_path = base_path + x['year']  + "/GS/GS02" + str(i).zfill(4) + ".HTML"
		play_path = base_path + x['year']  + "/PL/PL02" + str(i).zfill(4) + ".HTML"
		box_path = base_path + x['year']  + "/BX/BX02" + str(i).zfill(4) + ".HTML"

		try:
			if not path.exists(game_path):
				req = urlopen(game_uri)
				html = req.read()
				f = open( game_path, 'w')
				for line in html:
					f.write(line)
				f.close()
				
		except HTTPError as e:
			print 'Error code: ', e.code
			print 'URLs: %s' % game_uri

		try:
			if not path.exists(play_path):
				req = urlopen(play_uri)
				html = req.read()
				f = open( play_path, 'w')
				for line in html:
					f.write(line)
				f.close()
				
		except HTTPError as e:
			print 'Error code: ', e.code
			print 'URLs: %s' % play_uri

		try:
			if not path.exists(box_path):
				req = urlopen(box_uri)
				html = req.read()
				f = open( box_path, 'w')
				for line in html:
					f.write(line)
				f.close()
				
		except HTTPError as e:
			print 'Error code: ', e.code
			print 'URLs: %s' % box_uri