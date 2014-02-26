from PyQt4 import Qt
from PyQt4 import QtCore
from PyQt4 import QtGui

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

		box = QtGui.QGroupBox("Teams")
		
#Add in all of the Teams tab frame

		self.window = box