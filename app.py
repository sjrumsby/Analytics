from PyQt4 import Qt, QtCore, QtGui
from classes.frames import *
import settings

class Dialog(QtGui.QDialog):

	def __init__(self):
		super(Dialog, self).__init__()
		
		self.homeFrame = homeBox.homeBox(self)

		self.createMenu()
		self.createSideMenu()

		self.mainLayout = QtGui.QHBoxLayout()
		self.mainLayout.setMenuBar(self.menuBar)
		self.mainLayout.addWidget(self.sideMenuBox)
		self.mainLayout.addWidget(self.homeFrame.f)
		self.setLayout(self.mainLayout)

		self.setWindowTitle("NHL Analytics")
		self.resize(800,500)

	def createMenu(self):
		self.menuBar = QtGui.QMenuBar()
		
		exitAction = QtGui.QAction('&Exit', self)
		exitAction.setStatusTip('Exit NHL Analytics')
		exitAction.triggered.connect(QtGui.qApp.quit)
		
		aboutAction = QtGui.QAction('&About', self)
		aboutAction.setStatusTip('About NHL Analytics')
		aboutAction.triggered.connect(self.showAbout)

		fileMenu = self.menuBar.addMenu('&File')
		fileMenu.addAction(aboutAction)
		fileMenu.addAction(exitAction)
		
	def createSideMenu(self):
		box = QtGui.QWidget()
		layout = QtGui.QVBoxLayout()
		
		homeButton = QtGui.QPushButton("Home")
		homeButton.clicked.connect(self.homeClick)
		teamsButton = QtGui.QPushButton("Teams")
		teamsButton.clicked.connect(self.teamsClick)
		gamesButton = QtGui.QPushButton("Games")
		gamesButton.clicked.connect(self.gamesClick)
		skatersButton = QtGui.QPushButton("Skaters")
		skatersButton.clicked.connect(self.skatersClick)
		
		layout.addWidget(homeButton)
		layout.addWidget(teamsButton)
		layout.addWidget(gamesButton)
		layout.addWidget(skatersButton)
		
		layout.setAlignment(QtCore.Qt.AlignTop)
		box.setLayout(layout)
		box.setMaximumWidth(75)
		
		self.sideMenuBox = box

	def showAbout(self):
		msg = QtGui.QMessageBox()
		msg.setWindowTitle("About NHL Analytics")
		msg.resize(150,150)
		msg.setText("Version: %s\nAuthor: %s" % (settings.version, settings.author))
		msg.exec_();
		
	def homeClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = homeBox.homeBox(self)
		self.mainLayout.addWidget(newFrame.f)
		self.mainLayout.update()
		
	def gamesClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = gamesBox.gamesBox(self)
		self.mainLayout.addWidget(newFrame.f)
		self.mainLayout.update()
		
	def teamsClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = teamsBox.teamsBox(self)
		self.mainLayout.addWidget(newFrame.f)
		self.mainLayout.update()
		
	def skatersClick(self):
		widget = self.mainLayout.itemAt(1).widget()
		self.mainLayout.removeWidget(widget)
		widget.close()
		newFrame = skatersBox.skatersBox(self)
		self.mainLayout.addWidget(newFrame.f)
		self.mainLayout.update()

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec_())