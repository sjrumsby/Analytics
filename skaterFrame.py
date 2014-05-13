from PyQt4 import QtCore
from PyQt4 import QtGui
import os
import vars

class skaterBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(skaterBox, self).__init__()
		self.parent = parent

		if os.path.exists(vars.database):
				self.initUI()
		else:
			self.initNoDBUI()	

	def initNoDBUI(self):
		self.box = QtGui.QGroupBox("Skaters")
		self.boxLayout = QtGui.QVBoxLayout()
		self.boxLayout.addWidget(QtGui.QLabel("Error, no database found. Please run 'Update Database' from the tools menu"), 0, QtCore.Qt.AlignHCenter)
		self.boxLayout.setAlignment(QtCore.Qt.AlignTop)
		self.box.setLayout(self.boxLayout)
		self.window = self.box

	def initUI(self):
		box = QtGui.QGroupBox("Skaters")
		self.window = box