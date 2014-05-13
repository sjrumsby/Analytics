from PyQt4 import QtCore
from PyQt4 import QtGui
import os
import vars

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
		
		self.window = box