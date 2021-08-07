# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Jay\Google Drive\Projects\anima\old files\mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1190, 724)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.playMIDI = QtWidgets.QPushButton(self.centralwidget)
        self.playMIDI.setGeometry(QtCore.QRect(140, 640, 101, 31))
        self.playMIDI.setObjectName("playMIDI")
        self.displayMusic = QtWidgets.QGraphicsView(self.centralwidget)
        self.displayMusic.setGeometry(QtCore.QRect(140, 50, 1011, 581))
        self.displayMusic.setObjectName("displayMusic")
        self.header = QtWidgets.QLabel(self.centralwidget)
        self.header.setGeometry(QtCore.QRect(620, -10, 91, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.header.setFont(font)
        self.header.setObjectName("header")
        self.Export = QtWidgets.QPushButton(self.centralwidget)
        self.Export.setGeometry(QtCore.QRect(250, 640, 101, 31))
        self.Export.setObjectName("Export")
        self.generate = QtWidgets.QLabel(self.centralwidget)
        self.generate.setGeometry(QtCore.QRect(30, 40, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.generate.setFont(font)
        self.generate.setObjectName("generate")
        self.newMelody = QtWidgets.QPushButton(self.centralwidget)
        self.newMelody.setGeometry(QtCore.QRect(20, 180, 101, 31))
        self.newMelody.setObjectName("newMelody")
        self.newChord = QtWidgets.QPushButton(self.centralwidget)
        self.newChord.setGeometry(QtCore.QRect(20, 220, 101, 31))
        self.newChord.setObjectName("newChord")
        self.newProgression = QtWidgets.QPushButton(self.centralwidget)
        self.newProgression.setGeometry(QtCore.QRect(20, 260, 101, 31))
        self.newProgression.setObjectName("newProgression")
        self.newSingleNote = QtWidgets.QPushButton(self.centralwidget)
        self.newSingleNote.setGeometry(QtCore.QRect(20, 80, 101, 31))
        self.newSingleNote.setObjectName("newSingleNote")
        self.play_7 = QtWidgets.QPushButton(self.centralwidget)
        self.play_7.setGeometry(QtCore.QRect(20, 120, 101, 31))
        self.play_7.setObjectName("play_7")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1190, 21))
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.newFile = QtWidgets.QAction(mainWindow)
        self.newFile.setObjectName("newFile")
        self.saveFile = QtWidgets.QAction(mainWindow)
        self.saveFile.setObjectName("saveFile")
        self.copy = QtWidgets.QAction(mainWindow)
        self.copy.setObjectName("copy")
        self.paste = QtWidgets.QAction(mainWindow)
        self.paste.setObjectName("paste")
        self.menuMenu.addAction(self.newFile)
        self.menuMenu.addAction(self.saveFile)
        self.menuEdit.addAction(self.copy)
        self.menuEdit.addAction(self.paste)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.playMIDI.setText(_translate("mainWindow", "PLAY"))
        self.header.setText(_translate("mainWindow", "AnimA"))
        self.Export.setText(_translate("mainWindow", "Export"))
        self.generate.setText(_translate("mainWindow", "GENERATE"))
        self.newMelody.setText(_translate("mainWindow", "New Melody"))
        self.newChord.setText(_translate("mainWindow", "New Chord"))
        self.newProgression.setText(_translate("mainWindow", "New Progression"))
        self.newSingleNote.setText(_translate("mainWindow", "Note"))
        self.play_7.setText(_translate("mainWindow", "Rhythm"))
        self.menuMenu.setTitle(_translate("mainWindow", "Menu"))
        self.menuEdit.setTitle(_translate("mainWindow", "Edit"))
        self.newFile.setText(_translate("mainWindow", "New"))
        self.newFile.setStatusTip(_translate("mainWindow", "Create a new variation"))
        self.newFile.setShortcut(_translate("mainWindow", "Ctrl+N"))
        self.saveFile.setText(_translate("mainWindow", "Save"))
        self.saveFile.setStatusTip(_translate("mainWindow", "Save your creation"))
        self.saveFile.setShortcut(_translate("mainWindow", "Ctrl+S"))
        self.copy.setText(_translate("mainWindow", "Copy"))
        self.copy.setStatusTip(_translate("mainWindow", "Copy"))
        self.copy.setShortcut(_translate("mainWindow", "Ctrl+C"))
        self.paste.setText(_translate("mainWindow", "Paste"))
        self.paste.setStatusTip(_translate("mainWindow", "Paste"))
        self.paste.setShortcut(_translate("mainWindow", "Ctrl+V"))