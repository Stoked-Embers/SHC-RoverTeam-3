# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groundstation.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import PyQt5
PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

#app = QApplication([])

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        screen = QApplication.primaryScreen()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(screen.size())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.motorControlsFrame = QtWidgets.QFrame(self.centralwidget)
        self.motorControlsFrame.setGeometry(QtCore.QRect(-1, -1, 501, 150))
        self.motorControlsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.motorControlsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.motorControlsFrame.setObjectName("motorControlsFrame")
        self.motorControlLabel = QtWidgets.QLabel(self.motorControlsFrame)
        self.motorControlLabel.setGeometry(QtCore.QRect(200, 10, 100, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.motorControlLabel.setFont(font)
        self.motorControlLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.motorControlLabel.setObjectName("motorControlLabel")
        self.motorControlsBackground = QtWidgets.QGraphicsView(self.motorControlsFrame)
        self.motorControlsBackground.setGeometry(QtCore.QRect(0, 0, 501, 150))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.motorControlsBackground.setFont(font)
        self.motorControlsBackground.setStyleSheet("background-color: rgb(0, 85, 255)\n"
"")
        self.motorControlsBackground.setObjectName("motorControlsBackground")
        self.globalMotorSpeedSpinBox = QtWidgets.QSpinBox(self.motorControlsFrame)
        self.globalMotorSpeedSpinBox.setGeometry(QtCore.QRect(180, 70, 140, 40))
        self.globalMotorSpeedSpinBox.setMaximum(100)
        self.globalMotorSpeedSpinBox.setObjectName("globalMotorSpeedSpinBox")
        self.globalMotorSpeedLabel = QtWidgets.QLabel(self.motorControlsFrame)
        self.globalMotorSpeedLabel.setGeometry(QtCore.QRect(203, 50, 96, 16))
        self.globalMotorSpeedLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.globalMotorSpeedLabel.setObjectName("globalMotorSpeedLabel")
        self.motorControlsBackground.raise_()
        self.motorControlLabel.raise_()
        self.globalMotorSpeedSpinBox.raise_()
        self.globalMotorSpeedLabel.raise_()
        self.jointFrame = QtWidgets.QFrame(self.centralwidget)
        self.jointFrame.setGeometry(QtCore.QRect(-1, 149, 500, 240))
        self.jointFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.jointFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.jointFrame.setObjectName("jointFrame")
        self.jointBackground = QtWidgets.QGraphicsView(self.jointFrame)
        self.jointBackground.setGeometry(QtCore.QRect(0, -1, 501, 251))
        self.jointBackground.setObjectName("jointBackground")
        self.baseSpinBox = QtWidgets.QSpinBox(self.jointFrame)
        self.baseSpinBox.setGeometry(QtCore.QRect(50, 30, 70, 40))
        self.baseSpinBox.setMaximum(100)
        self.baseSpinBox.setObjectName("baseSpinBox")
        self.midSpinBox = QtWidgets.QSpinBox(self.jointFrame)
        self.midSpinBox.setGeometry(QtCore.QRect(215, 30, 70, 40))
        self.midSpinBox.setMaximum(100)
        self.midSpinBox.setObjectName("midSpinBox")
        self.endSpinBox = QtWidgets.QSpinBox(self.jointFrame)
        self.endSpinBox.setGeometry(QtCore.QRect(380, 30, 70, 40))
        self.endSpinBox.setMaximum(100)
        self.endSpinBox.setObjectName("endSpinBox")
        self.baseLabel = QtWidgets.QLabel(self.jointFrame)
        self.baseLabel.setGeometry(QtCore.QRect(73, 10, 25, 15))
        self.baseLabel.setObjectName("baseLabel")
        self.midLabel = QtWidgets.QLabel(self.jointFrame)
        self.midLabel.setGeometry(QtCore.QRect(240, 10, 20, 15))
        self.midLabel.setObjectName("midLabel")
        self.endLabel = QtWidgets.QLabel(self.jointFrame)
        self.endLabel.setGeometry(QtCore.QRect(405, 10, 20, 15))
        self.endLabel.setObjectName("endLabel")
        self.armDiagram = QtWidgets.QLabel(self.jointFrame)
        self.armDiagram.setGeometry(QtCore.QRect(100, -60, 311, 441))
        self.armDiagram.setText("")
        self.armDiagram.setPixmap(QtGui.QPixmap("images/armdiagram.png"))
        self.armDiagram.setScaledContents(True)
        self.armDiagram.setObjectName("armDiagram")
        self.jointBackground.raise_()
        self.baseSpinBox.raise_()
        self.endSpinBox.raise_()
        self.baseLabel.raise_()
        self.endLabel.raise_()
        self.armDiagram.raise_()
        self.midSpinBox.raise_()
        self.midLabel.raise_()
        self.controlsFrame = QtWidgets.QFrame(self.centralwidget)
        self.controlsFrame.setGeometry(QtCore.QRect(0, 390, 500, 171))
        self.controlsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controlsFrame.setObjectName("controlsFrame")
        self.controlsBackground = QtWidgets.QGraphicsView(self.controlsFrame)
        self.controlsBackground.setGeometry(QtCore.QRect(0, 0, 500, 171))
        self.controlsBackground.setStyleSheet("")
        self.controlsBackground.setObjectName("controlsBackground")
        self.controlsDiagram = QtWidgets.QLabel(self.controlsFrame)
        self.controlsDiagram.setGeometry(QtCore.QRect(0, 10, 501, 151))
        self.controlsDiagram.setText("")
        self.controlsDiagram.setPixmap(QtGui.QPixmap("images/xboxmap.png"))
        self.controlsDiagram.setScaledContents(True)
        self.controlsDiagram.setObjectName("controlsDiagram")
        self.graphFrame = QtWidgets.QFrame(self.centralwidget)
        self.graphFrame.setGeometry(QtCore.QRect(500, 0, 500, 390))
        self.graphFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.graphFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.graphFrame.setObjectName("graphFrame")
        self.graphBackground = QtWidgets.QGraphicsView(self.graphFrame)
        self.graphBackground.setGeometry(QtCore.QRect(0, 0, 500, 390))
        self.graphBackground.setStyleSheet("background-color: rgb(118, 118, 118)")
        self.graphBackground.setObjectName("graphBackground")
        self.data1Frame = QtWidgets.QFrame(self.centralwidget)
        self.data1Frame.setGeometry(QtCore.QRect(500, 390, 247, 171))
        self.data1Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data1Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data1Frame.setObjectName("data1Frame")
        self.data1Background = QtWidgets.QGraphicsView(self.data1Frame)
        self.data1Background.setGeometry(QtCore.QRect(0, 0, 250, 170))
        self.data1Background.setStyleSheet("background-color: rgb(168, 168, 168);")
        self.data1Background.setObjectName("data1Background")
        self.data1Label = QtWidgets.QLabel(self.data1Frame)
        self.data1Label.setGeometry(QtCore.QRect(10, 10, 31, 16))
        self.data1Label.setStyleSheet("color: rgb(255, 255, 255)")
        self.data1Label.setObjectName("data1Label")
        self.data2Frame = QtWidgets.QFrame(self.centralwidget)
        self.data2Frame.setGeometry(QtCore.QRect(753, 390, 247, 171))
        self.data2Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data2Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data2Frame.setObjectName("data2Frame")
        self.data2Background = QtWidgets.QGraphicsView(self.data2Frame)
        self.data2Background.setGeometry(QtCore.QRect(0, 0, 250, 170))
        self.data2Background.setStyleSheet("background-color: rgb(168, 168, 168);")
        self.data2Background.setObjectName("data2Background")
        self.data2Label = QtWidgets.QLabel(self.data2Frame)
        self.data2Label.setGeometry(QtCore.QRect(10, 10, 32, 13))
        self.data2Label.setStyleSheet("color: rgb(255, 255, 255)")
        self.data2Label.setObjectName("data2Label")
        self.dataSeparator = QtWidgets.QGraphicsView(self.centralwidget)
        self.dataSeparator.setGeometry(QtCore.QRect(747, 390, 7, 170))
        self.dataSeparator.setStyleSheet("background-color: rgb(0, 0, 0)")
        self.dataSeparator.setObjectName("dataSeparator")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ground Station"))
        self.motorControlLabel.setText(_translate("MainWindow", "Motor Controls"))
        self.globalMotorSpeedLabel.setText(_translate("MainWindow", "Global Motor Speed"))
        self.baseLabel.setText(_translate("MainWindow", "Base"))
        self.midLabel.setText(_translate("MainWindow", "Mid"))
        self.endLabel.setText(_translate("MainWindow", "End"))
        self.data1Label.setText(_translate("MainWindow", "Data 1"))
        self.data2Label.setText(_translate("MainWindow", "Data 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
