#################################################################################
#																				#
# 	All widgets define all of their innerds as box, and assign the box			#
#	to self.f, in order to be easily imported within main application			#
#																				#
#################################################################################


from PyQt4 import Qt, QtCore, QtGui

class teamsBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(teamsBox, self).__init__()
		self.parent = parent

		box = QtGui.QGroupBox("Teams")
		
		self.f = box