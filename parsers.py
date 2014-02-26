#Contains all of the HTML parsers to pull data from NHL.com

from HTMLParser import HTMLParser

class boxParser(HTMLParser):
		def __init__(self):
			HTMLParser.__init__(self)
			
			self.rec = 0
			self.tr_rec = 0
			self.count = 0
			self.data = []
			self.home_skaters = []
			self.home_goalies = []
			self.away_skaters = []
			self.away_goalies = []
			
		def handle_starttag(self, tag, attributes):
			if tag == "table":
				for name,value in attributes:
					if name == "class" and value == "stats":
						self.rec += 1

			if self.rec > 0 and self.rec <= 4:
				if tag == "tr":
					self.tr_rec = 1
				if self.count > 0:
					for name, value in attributes:
						if name=='href':
							id = value.split('=')
							id = id[1]
							self.data.append(id)
		
		def handle_data(self, data):
			if self.tr_rec == 1:
				self.data.append(data)
				self.count += 1
		
		def handle_endtag(self, tag):
			if tag == "tr":
				if self.rec == 1:
					if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
						self.away_skaters.append(self.data)
				elif self.rec == 2:
					if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
						self.away_goalies.append(self.data)
				elif self.rec == 3:
					if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
						self.home_skaters.append(self.data)
				elif self.rec == 4:
					if "SH TOI" not in self.data and "Saves - Shots" not in self.data:
						self.home_goalies.append(self.data)
				self.data = []
				self.count = 0

			if tag == "table" and self.rec == 4:
				self.rec += 1

class playParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.plays 		= []
		self.home_ice	= []
		self.away_ice	= []
		self.play_data 	= []
		self.t_count 	= 0
		self.rec 		= 0
		self.on_ice_rec	= 0
		self.team		= 0
		self.td_rec		= 0
		self.td_count	= 0

	def handle_starttag(self, tag, attributes):
		if tag == "tr":
			for name,value in attributes:
				if name == "class" and value == "evenColor":
					self.rec = 1

		if tag == "table" and self.rec:
			self.t_count += 1
		
		if tag == "font":
			self.on_ice_rec = 1
			
		if tag == "td" and self.td_rec:
			self.td_count += 1
		
		if tag == "td":
			for name,value in attributes:
				if name == "class":
					if "rborder" in value:
						self.team = 0
						self.td_rec = 1
						self.td_count = 1
			
	def handle_data(self, data):
		if self.rec and self.t_count == 0:
			if data != '\r\n' and data != '\r\r\n':
				self.play_data.append(data)
		
		if self.on_ice_rec:
			if self.team == 0:
				self.away_ice.append(data)
			else:
				self.home_ice.append(data)

	def handle_endtag(self, tag):
		if tag == "table" and self.rec:
			self.t_count -= 1

		if tag == "tr" and self.rec:
			if self.play_data != []:
				if "Elapsed" not in self.play_data and "Description" not in self.play_data:
					tmp_dict = {'play' : self.play_data, 'home' : self.home_ice, 'away' : self.away_ice }
					self.plays.append(tmp_dict)
				self.play_data = []
				self.home_ice = []
				self.away_ice = []
		
		if tag == "font":
			self.on_ice_rec = 0
			
		if tag == "td" and self.td_rec:
			self.td_count -= 1
			
		if self.td_rec and self.td_count == 0:
			self.td_rec = 0
			self.team = 1

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
			
class summaryParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)

		self.summary_rec = 0
		self.summary_data = []
		self.append = 0

		self.goal_rec = 0
		self.goal_row = []
		self.goal_data = []

		self.on_ice_rec = 0
		self.on_ice_row = []

		self.penalty_rec = 0
		self.penalty_row = []
		self.away_penalty_data = []
		self.home_penalty_data = []
		self.penalty_header_count = 0

		self.goalie_rec = 0
		self.goalie_row = []
		self.goalie_data = []

		self.period_rec = 0
		self.period_row = []
		self.period_data = []

		self.stars_rec = 0
		self.stars_row = []
		self.stars_data = []

	def handle_starttag(self, tag, attributes):
		if tag == "table":
			for name,value in attributes:
				if name =="id" and value =="StdHeader":
					self.summary_rec = 1
		if self.goal_rec or self.on_ice_rec:
			if tag == "font":
				for name,value in attributes:
					if name == "title":
						self.on_ice_rec = 1
						self.on_ice_row.append(value.split(" - ")[-1])
						self.goal_rec = 0

	def handle_data(self, data):
		if self.summary_rec:
			if data != "\r\n" and data != "\r\r\n" and data != ", " and data != "Sommaire du Match":
				if self.append:
					end_row = self.summary_data.pop()
					end_row += data
					self.summary_data.append(end_row)
					self.append = 0
				else:
					self.summary_data.append(data)

		if self.stars_rec:
			if data != "\r\n" and data != "\r\r\n":
				self.stars_row.append(data)

		if "SCORING SUMMARY" in data:
			self.summary_rec = 0

		if "3 STARS" in data:
			self.stars_rec = 1
	
	def handle_endtag(self, tag):
		if self.on_ice_rec or self.goal_rec:
			if tag == "tr":
				if self.goal_row != [] and len(self.goal_row) > 2 and "Goal Scorer" not in self.goal_row:
					self.goal_row.append(self.on_ice_row)
					self.goal_data.append(self.goal_row)
				self.goal_row = []
				self.on_ice_row = []
				self.on_ice_rec = 0
				self.goal_rec = 1

		if self.penalty_rec:
			if tag == "tr":
				if "Player" in self.penalty_row:
					self.penalty_header_count += 1
				else:
					if self.penalty_row != [] and 'TOT' not in self.penalty_row and "Player" not in self.penalty_row:
						if self.penalty_header_count == 1:
							if len(self.penalty_row) == 2:
								temp_row = self.away_penalty_data.pop()
								for x in self.penalty_row:
									temp_row.append(x)
								self.away_penalty_data.append(temp_row)
							else:
								self.away_penalty_data.append(self.penalty_row)
						else:
							if len(self.penalty_row) == 2:
								temp_row = self.home_penalty_data.pop()
								for x in self.penalty_row:
									temp_row.append(x)
								self.home_penalty_data.append(temp_row)
							else:
								self.home_penalty_data.append(self.penalty_row)
				self.penalty_row = []

		if self.period_rec:
			if tag == "tr":
				if self.period_row != [] and len(self.period_row) > 1 and "Goals" not in self.period_row and "5v4" not in self.period_row and "5v5" not in self.period_row:
					self.period_data.append(self.period_row)
				self.period_row = []

		if self.goalie_rec:
			if tag == "tr":
				if self.goalie_row != [] and "BUTS-LANCERS" not in self.goalie_row and "DN/SH" not in self.goalie_row:
					self.goalie_data.append(self.goalie_row)
				self.goalie_row = []

		if self.stars_rec:
			if tag == "tr":
				if self.stars_row != [] and len(self.stars_row) == 4:
					self.stars_data.append(self.stars_row)
				self.stars_row = []
				
	def handle_entityref(self, name):
		if name == "amp":
			self.append = 1