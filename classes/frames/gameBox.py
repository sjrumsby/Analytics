#################################################################################
#																				#
# 	All widgets definte all of their structures, and assign the struct			#
#	to self.f, in order to be easily imported within main application			#
#																				#
#################################################################################


from PyQt4 import Qt, QtCore, QtGui

class gameBox(QtGui.QDialog):
	
	def __init__(self, parent):
		super(gameBox, self).__init__()
		self.parent = parent

		self.f = QtGui.QGroupBox("Games")