from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui
import settings
import sqlite3
import os.path

class gamesBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(gamesBox, self).__init__()
		self.parent = parent

		box = QtGui.QGroupBox("Games")

#Add in all of the Games tab frame

		self.window = box

class homeBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(homeBox, self).__init__()
		self.parent = parent

		box = QtGui.QGroupBox("Home")
		
		self.boxLayout = QtGui.QVBoxLayout()
		self.title = QtGui.QLabel("Welcome to NHL Anayltics!")
		self.text = QtGui.QLabel("This application doesn't really do shit right now, but that will change soon!")
		self.boxLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter)
		self.boxLayout.addWidget(self.text, 0, QtCore.Qt.AlignHCenter)
		self.boxLayout.setAlignment(QtCore.Qt.AlignTop)

		box.setLayout(self.boxLayout)
		
#Add in all of the Home tab frame

		self.window = box

class playBox(QtGui.QDialog):

	def __init__(self, parent):
		super(playBox, self).__init__()
		self.parent = parent
		box = QtGui.QGroupBox("Plays")
		
#Add in all of the Play tab frame

		self.window = box

class skatersBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(skatersBox, self).__init__()
		self.parent = parent

		box = QtGui.QGroupBox("Skaters")

#Add in all of the Skaters tab frame

		self.window = box

class teamsBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(teamsBox, self).__init__()
		self.parent = parent
		
		if os.path.exists(settings.database):
			try:
				self.con = sqlite3.connect(settings.database)
				self.c = self.con.cursor()
			except:
				exit("Failure")
			
		self.c.execute('select id, long_name from hockey_team')
		self.teams = self.c.fetchall()
	
	def initUI(self):
		self.box = QtGui.QGroupBox("Teams")
		self.boxLayout = QtGui.QHBoxLayout()
		
		self.createSideBox()
		self.createReportBox()
		
		self.boxLayout.addWidget(self.sideBox)
		self.boxLayout.addWidget(self.reportBox)

		self.boxLayout.setAlignment(QtCore.Qt.AlignLeft)
		self.box.setLayout(self.boxLayout)
		
		self.window = self.box
	
	def createSideBox(self):
#I dont know why I have to do this, for some reason the button won't connect directly to self.reportClick
#So we have to go through this helper function instead

		def helperFunc():
			self.reportClick()
			
		self.sideBox = QtGui.QGroupBox()
		self.sideBoxLayout = QtGui.QVBoxLayout()
		self.teamLabel = QtGui.QLabel("Select Team")
		self.sideBoxLayout.addWidget(self.teamLabel)
		self.teamDropDown = QtGui.QComboBox()
		
		for t in self.teams:
			self.teamDropDown.addItem(t[1], t[0])
			
		self.sideBoxLayout.addWidget(self.teamDropDown)
		
		self.goButton = QtGui.QPushButton("Go!")
		self.goButton.clicked.connect(helperFunc)
		self.sideBoxLayout.addWidget(self.goButton)
		
		self.sideBoxLayout.setAlignment(QtCore.Qt.AlignTop)
		self.sideBox.setLayout(self.sideBoxLayout)
		
		self.sideBox.setMaximumWidth(200)
	
	def createReportBox(self):
		self.reportBox = QtGui.QGroupBox()
		self.reportBoxLayout = QtGui.QVBoxLayout()
		
		self.reportBoxLabel = QtGui.QLabel("Report Frame")
		self.reportBoxLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
		self.reportBoxLayout.addWidget(self.reportBoxLabel)
		self.reportBoxLayout.setAlignment(QtCore.Qt.AlignTop)
		
		self.reportBox.setLayout(self.reportBoxLayout)
		
	def reportClick(self):
		teamName = self.teamDropDown.itemData(self.teamDropDown.currentIndex()).toString()
		result = self.c.execute("SELECT nhl_id, name, position FROM skater WHERE hockey_team_id = %s" % teamName)
		roster = result.fetchall()
		
		rosterHeader = QtCore.QStringList()
		rosterHeader.insert(0, "Name")
		rosterHeader.insert(1, "Position")
				
		rosterScroll = QtGui.QScrollArea()
		rosterTable = QtGui.QTableWidget()
		rosterTable.setColumnCount(2)
		rosterTable.setHorizontalHeaderLabels(rosterHeader)
		
		insertItems = []
		
		for x in roster:
			tempDict = {'name' : x[1], 'position' : x[2] }
			insertItems.append(tempDict)
		
		for t in insertItems:
			row = rosterTable.rowCount()
			rosterTable.insertRow(row)
			rosterTable.setItem(row, 0, QtGui.QTableWidgetItem(t['name']))
			rosterTable.setItem(row, 1, QtGui.QTableWidgetItem(t['position']))
		
		rosterScroll.setWidget(rosterTable)
		rosterScroll.setWidgetResizable(True)
		rosterScroll.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
		
		widget = self.reportBoxLayout.itemAt(1)
		if widget == None:
			self.reportBoxLayout.addWidget(rosterScroll)
		else:
			widget = widget.widget()
			self.reportBoxLayout.removeWidget(widget)
			widget.close()
			self.reportBoxLayout.addWidget(rosterScroll)
			self.reportBoxLayout.update()