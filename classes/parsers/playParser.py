from HTMLParser import HTMLParser

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