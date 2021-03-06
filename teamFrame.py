from PyQt4 import QtCore
from PyQt4 import QtGui
import os
import vars

from django.conf import settings

settings.configure(	DATABASES = 	{ 'default': {
										'ENGINE': 'django.db.backends.sqlite3',
										'NAME': 'data.sqlite', 
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

class teamBox(QtGui.QDialog):
	con = None
	c = None
	
	def __init__(self, parent):
		super(teamBox, self).__init__()
		self.parent = parent
		
		if os.path.exists(vars.database):
				self.initUI()
		else:
			self.initNoDBUI()	
	
	def initNoDBUI(self):
		self.box = QtGui.QGroupBox("Teams")
		self.boxLayout = QtGui.QVBoxLayout()
		self.boxLayout.addWidget(QtGui.QLabel("Error, no database found. Please run 'Update Database' from the tools menu"), 0, QtCore.Qt.AlignHCenter)
		self.boxLayout.setAlignment(QtCore.Qt.AlignTop)
		self.box.setLayout(self.boxLayout)
		self.window = self.box
	
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
		
		for t in Hockey_Team.objects.all():
			self.teamDropDown.addItem(t.full_name, t.id)
			
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
		self.rosterTable = QtGui.QTableWidget()
		self.rosterTable.setColumnCount(2)
		self.rosterTable.setHorizontalHeaderLabels(rosterHeader)
		
		insertItems = []
		
		for x in roster:
			tempDict = {'name' : x[1], 'position' : x[2] }
			insertItems.append(tempDict)
		
		for t in insertItems:
			row = self.rosterTable.rowCount()
			self.rosterTable.insertRow(row)
			nameItem = QtGui.QTableWidgetItem(t['name'])
			self.rosterTable.setItem(row, 0, nameItem)
			self.rosterTable.setItem(row, 1, QtGui.QTableWidgetItem(t['position']))

		self.rosterTable.cellClicked.connect(self.rosterTableCellClicked)				
		rosterScroll.setWidget(self.rosterTable)
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
	
	def rosterTableCellClicked(self, row, column):
		if column == 0:
			skaterPopUp = QtGui.QDialog(self.parent)
			cell = self.rosterTable.item(row, column)
			skaterPopUpLayout = QtGui.QVBoxLayout()
			try:
				s = skater.Skater(str(cell.text()))

				teamWidget = QtGui.QWidget()
				teamRowLayout = QtGui.QHBoxLayout()
				teamLabel = QtGui.QLabel("Team")
				teamValueLabel = QtGui.QLabel(s.team)
				teamRowLayout.addWidget(teamLabel)
				teamRowLayout.addWidget(teamValueLabel)
				teamWidget.setLayout(teamRowLayout)

				positionWidget = QtGui.QWidget()
				positionRowLayout = QtGui.QHBoxLayout()
				positionLabel = QtGui.QLabel("Position")
				positionValueLabel = QtGui.QLabel(s.position)
				positionRowLayout.addWidget(positionLabel)
				positionRowLayout.addWidget(positionValueLabel)
				positionWidget.setLayout(positionRowLayout)

				gamesPlayedWidget = QtGui.QWidget()
				gamesPlayedRowLayout = QtGui.QHBoxLayout()
				gamesPlayedLabel = QtGui.QLabel("Games Played")
				gamesPlayedValueLabel = QtGui.QLabel(str(s.gamesPlayed))
				gamesPlayedRowLayout.addWidget(gamesPlayedLabel)
				gamesPlayedRowLayout.addWidget(gamesPlayedValueLabel)
				gamesPlayedWidget.setLayout(gamesPlayedRowLayout)

				goalsWidget = QtGui.QWidget()
				goalsRowLayout = QtGui.QHBoxLayout()
				goalsLabel = QtGui.QLabel("Goals")
				goalsValueLabel = QtGui.QLabel(str(s.goals))
				goalsRowLayout.addWidget(goalsLabel)
				goalsRowLayout.addWidget(goalsValueLabel)
				goalsWidget.setLayout(goalsRowLayout)

				assistsWidget = QtGui.QWidget()
				assistsRowLayout = QtGui.QHBoxLayout()
				assistsLabel = QtGui.QLabel("Assists")
				assistsValueLabel = QtGui.QLabel(str(s.assists))
				assistsRowLayout.addWidget(assistsLabel)
				assistsRowLayout.addWidget(assistsValueLabel)
				assistsWidget.setLayout(assistsRowLayout)

				pointsWidget = QtGui.QWidget()
				pointsRowLayout = QtGui.QHBoxLayout()
				pointsLabel = QtGui.QLabel("Points")
				pointsValueLabel = QtGui.QLabel(str(s.points))
				pointsRowLayout.addWidget(pointsLabel)
				pointsRowLayout.addWidget(pointsValueLabel)
				pointsWidget.setLayout(pointsRowLayout)

				plusMinusWidget = QtGui.QWidget()
				plusMinusRowLayout = QtGui.QHBoxLayout()
				plusMinusLabel = QtGui.QLabel("Plus Minus")
				plusMinusValueLabel = QtGui.QLabel(str(s.plusMinus))
				plusMinusRowLayout.addWidget(plusMinusLabel)
				plusMinusRowLayout.addWidget(plusMinusValueLabel)
				plusMinusWidget.setLayout(plusMinusRowLayout)

				skaterPopUpLayout.addWidget(teamWidget)
				skaterPopUpLayout.addWidget(positionWidget)
				skaterPopUpLayout.addWidget(gamesPlayedWidget)
				skaterPopUpLayout.addWidget(goalsWidget)
				skaterPopUpLayout.addWidget(assistsWidget)
				skaterPopUpLayout.addWidget(pointsWidget)
				skaterPopUpLayout.addWidget(plusMinusWidget)
			
			except Exception as e:
				errorWidget = QtGui.QWidget()
				errorLayout = QtGui.QHBoxLayout()
				errorLabel = QtGui.QLabel("Error creating skater")
				errorMsg = QtGui.QLabel(str(e))
				errorLayout.addWidget(errorLabel)
				errorLayout.addWidget(errorMsg)
				errorWidget.setLayout(errorLayout)
				skaterPopUpLayout.addWidget(errorWidget)
			
			skaterPopUp.setLayout(skaterPopUpLayout)
			skaterPopUp.setMinimumWidth(250)
			skaterPopUp.show()
			skaterPopUp.setWindowTitle(cell.text())
			skaterPopUp.activateWindow()