from PyQt4 import QtCore
from PyQt4 import QtGui
from models import *
import settings
import sqlite3
import os.path

class gamesBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(gamesBox, self).__init__()
		self.parent = parent

		if os.path.exists(settings.database):
			try:
				self.con = sqlite3.connect(settings.database)
				self.c = self.con.cursor()
				self.c.execute('select id, long_name from hockey_team')
				self.teams = self.c.fetchall()
				self.initUI()
			except:
				exit("Failure to connect to database")
		else:
			self.initNoDBUI()

	def initNoDBUI(self):
		self.box = QtGui.QGroupBox("Games")
		self.boxLayout = QtGui.QVBoxLayout()
		self.boxLayout.addWidget(QtGui.QLabel("Error, no database found. Please run 'Update Database' from the tools menu"), 0, QtCore.Qt.AlignHCenter)
		self.boxLayout.setAlignment(QtCore.Qt.AlignTop)
		self.box.setLayout(self.boxLayout)
		self.window = self.box

	def initUI(self):
		box = QtGui.QGroupBox("Games")
		self.window = box