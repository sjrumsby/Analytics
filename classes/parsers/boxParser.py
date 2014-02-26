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