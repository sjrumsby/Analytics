from PyQt4 import Qt, QtCore, QtGui
from appFrames import *
import dataScripts
import settings
from time import sleep

class mainWindow(QtGui.QMainWindow):

	def __init__(self):
		super(mainWindow, self).__init__()
		
		self.app = QtGui.QWidget(self)
		self.setCentralWidget(self.app)
		
		self.menuBar = QtGui.QMenuBar()
		self.createFileMenu()
		self.createToolsMenu()
		self.createSideMenu()

		self.homeFrame = homeBox(self.app)
		
		self.mainLayout = QtGui.QHBoxLayout()
		self.mainLayout.setMenuBar(self.menuBar)
		self.mainLayout.addWidget(self.sideMenuBox)
		self.mainLayout.addWidget(self.homeFrame.window)
		self.app.setLayout(self.mainLayout)

		self.setWindowTitle("NHL Analytics")
		self.resize(800,500)
		self.show()

	def createFileMenu(self):
		exitAction = QtGui.QAction('&Exit', self)
		exitAction.setStatusTip('Exit NHL Analytics')
		exitAction.triggered.connect(QtGui.qApp.quit)
		
		aboutAction = QtGui.QAction('&About', self)
		aboutAction.setStatusTip('About NHL Analytics')
		aboutAction.triggered.connect(self.showAbout)

		fileMenu = self.menuBar.addMenu('&File')
		fileMenu.addAction(aboutAction)
		fileMenu.addAction(exitAction)
	
	def createToolsMenu(self):
		addDataAction = QtGui.QAction('&Add Data', self)
		addDataAction.setStatusTip('Add data into database')
		addDataAction.triggered.connect(self.addData)
		
		removeDataAction = QtGui.QAction('&Remove Data', self)
		removeDataAction.setStatusTip('Remove all data from the database')
		removeDataAction.triggered.connect(self.removeData)
		
		toolsMenu = self.menuBar.addMenu('&Tools')
		toolsMenu.addAction(addDataAction)
		toolsMenu.addAction(removeDataAction)
		
	def createSideMenu(self):
		box = QtGui.QWidget()
		layout = QtGui.QVBoxLayout()
		
		homeButton = QtGui.QPushButton("Home")
		homeButton.clicked.connect(self.homeClick)

		gamesButton = QtGui.QPushButton("Games")
		gamesButton.clicked.connect(self.gamesClick)
		
		teamsButton = QtGui.QPushButton("Teams")
		teamsButton.clicked.connect(self.teamsClick)
		
		skatersButton = QtGui.QPushButton("Skaters")
		skatersButton.clicked.connect(self.skatersClick)
		
		playButton = QtGui.QPushButton("Plays")
		playButton.clicked.connect(self.playClick)
		
		layout.addWidget(homeButton)
		layout.addWidget(teamsButton)
		layout.addWidget(gamesButton)
		layout.addWidget(skatersButton)
		layout.addWidget(playButton)
		
		layout.setAlignment(QtCore.Qt.AlignTop)
		box.setLayout(layout)
		box.setMaximumWidth(75)
		
		self.sideMenuBox = box

	def showAbout(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("About")
		msg.resize(200,200)
		msg.setText("Version: %s\nAuthor: %s" % (settings.version, settings.author))
		msg.exec_();

	def gamesClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = gamesBox(self)
		self.mainLayout.addWidget(newFrame.window)
		self.mainLayout.update()
		
	def homeClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = homeBox(self)
		self.mainLayout.addWidget(newFrame.window)
		self.mainLayout.update()

	def playClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = playBox(self)
		self.mainLayout.addWidget(newFrame.window)
		self.mainLayout.update()
		
	def skatersClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = skatersBox(self)
		self.mainLayout.addWidget(newFrame.window)
		self.mainLayout.update()

	def teamsClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = teamsBox(self)
		self.mainLayout.addWidget(newFrame.window)
		self.mainLayout.update()

	def addData(self):
		progress = QtGui.QProgressDialog("Please wait...", "Abort", 0, 100, self)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setAutoReset(True)
		progress.setAutoClose(True)
		progress.setMinimum(0)
		progress.setMaximum(100)
		progress.setWindowTitle("Adding Data...")
		progress.show()

		progress.setLabelText("Adding hockey team data...")
		dataScripts.addHockeyTeamData()
		progress.setValue(5)
		
		progress.setLabelText("Adding miss type data")
		dataScripts.addMissTypeData()
		progress.setValue(9)
		
		progress.setLabelText("Adding penalty type data")
		dataScripts.addPenaltyTypeData()
		progress.setValue(13)
		
		progress.setLabelText("Adding play type data")
		dataScripts.addPlayTypeData()
		progress.setValue(19)
		
		progress.setLabelText("Adding shot type data")
		dataScripts.addShotTypeData()
		progress.setValue(23)
		
		progress.setLabelText("Adding stop type data")
		dataScripts.addStopTypeData()
		progress.setValue(29)
		
		progress.setLabelText("Adding zone type data")
		dataScripts.addZoneTypeData()
		progress.setValue(34)
		
		progress.setLabelText("Adding skater data")
		progress.setValue(35)			#Has to be updated once to force update of label
		dataScripts.addSkaterData()
		progress.setValue(100)
	
	def removeData(self):
		progress = QtGui.QProgressDialog("Please wait...", "Abort", 0, 100, self)
		progress.setWindowModality(QtCore.Qt.WindowModal)
		progress.setAutoReset(True)
		progress.setAutoClose(True)
		progress.setMinimum(0)
		progress.setMaximum(100)
		progress.setWindowTitle("Removing Data...")
		progress.show()
		progress.setValue(1)

		dataScripts.removeAllData()
		progress.setValue(100)

if __name__ == '__main__':

	import sys

	app = QtGui.QApplication(sys.argv)
	window = mainWindow()
	sys.exit(app.exec_())