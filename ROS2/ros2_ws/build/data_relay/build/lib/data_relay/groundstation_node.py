#!/usr/bin/env python3
import sys
import time
import PyQt5
import random
from PyQt5.QtCore import QResource
# import diagrams_rc
from enum import Enum
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class AccelerationGraph(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        fig = Figure(figsize = (width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(AccelerationGraph, self).__init__(fig)

        self.setParent(parent)

        #Placeholder variables for IMU data
        self.x_data = [] # time variable
        self.y_data= [] # acceleration data

        self.axes.set_title("Acceleration Data")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Acceleration (m/s^2)")

    def update_graph(self, new_data):
        # update x data (time)
        self.x_data.append(len(self.x_data))
        # update y data (acceleration)
        self.y_data.append(len(self.y_data))

        #clear plot and plot new data
        self.axes.clear()
        self.axes.plot(self.x_data, self.y_data, label="Acceleration (m/s^2)")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Acceleration (m/s^2)")
        self.axes.set_title("Acceleration Data")
        self.axes.legend(loc = "upper left")
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(949, 487)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.motorControlsFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.motorControlsFrame.sizePolicy().hasHeightForWidth())
        self.motorControlsFrame.setSizePolicy(sizePolicy)
        self.motorControlsFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.motorControlsFrame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.motorControlsFrame.setStyleSheet("background-color: rgb(0, 85, 255)")
        self.motorControlsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.motorControlsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.motorControlsFrame.setObjectName("motorControlsFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.motorControlsFrame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.motorControlsLayout = QtWidgets.QGridLayout()
        self.motorControlsLayout.setContentsMargins(0, 0, 0, 0)
        self.motorControlsLayout.setSpacing(0)
        self.motorControlsLayout.setObjectName("motorControlsLayout")
        self.motorControlLabel = QtWidgets.QLabel(self.motorControlsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.motorControlLabel.sizePolicy().hasHeightForWidth())
        self.motorControlLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.motorControlLabel.setFont(font)
        self.motorControlLabel.setStyleSheet("color: rgb(255, 255, 255)\n"
"")
        self.motorControlLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.motorControlLabel.setObjectName("motorControlLabel")
        self.motorControlsLayout.addWidget(self.motorControlLabel, 0, 0, 1, 1)
        self.globalMotorSpeedLabel = QtWidgets.QLabel(self.motorControlsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.globalMotorSpeedLabel.sizePolicy().hasHeightForWidth())
        self.globalMotorSpeedLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.globalMotorSpeedLabel.setFont(font)
        self.globalMotorSpeedLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.globalMotorSpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.globalMotorSpeedLabel.setObjectName("globalMotorSpeedLabel")
        self.motorControlsLayout.addWidget(self.globalMotorSpeedLabel, 1, 0, 1, 1)
        self.globalMotorSpeedSpinBox = QtWidgets.QSpinBox(self.motorControlsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.globalMotorSpeedSpinBox.sizePolicy().hasHeightForWidth())
        self.globalMotorSpeedSpinBox.setSizePolicy(sizePolicy)
        self.globalMotorSpeedSpinBox.setMinimumSize(QtCore.QSize(150, 0))
        self.globalMotorSpeedSpinBox.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.globalMotorSpeedSpinBox.setSuffix("")
        self.globalMotorSpeedSpinBox.setMinimum(-1)
        self.globalMotorSpeedSpinBox.setMaximum(100)
        self.globalMotorSpeedSpinBox.setObjectName("globalMotorSpeedSpinBox")
        self.globalMotorSpeedSpinBox.setRange(0, 100)
        self.motorControlsLayout.addWidget(self.globalMotorSpeedSpinBox, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_2.addLayout(self.motorControlsLayout, 0, 0, 2, 2)
        self.gridLayout.addWidget(self.motorControlsFrame, 0, 0, 1, 1)
        self.graphFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphFrame.sizePolicy().hasHeightForWidth())
        self.graphFrame.setSizePolicy(sizePolicy)
        self.graphFrame.setMinimumSize(QtCore.QSize(200, 200))
        self.graphFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.graphFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.graphFrame.setObjectName("graphFrame")
        self.gridLayout.addWidget(self.graphFrame, 0, 1, 2, 1)
        self.jointFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jointFrame.sizePolicy().hasHeightForWidth())
        self.jointFrame.setSizePolicy(sizePolicy)
        self.jointFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.jointFrame.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.jointFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.jointFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.jointFrame.setObjectName("jointFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.jointFrame)
        self.gridLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.jointDiagram = QtWidgets.QGridLayout()
        self.jointDiagram.setObjectName("jointDiagram")
        self.jointControls = QtWidgets.QGridLayout()
        self.jointControls.setObjectName("jointControls")
        self.endButton = QtWidgets.QRadioButton(self.jointFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endButton.sizePolicy().hasHeightForWidth())
        self.endButton.setSizePolicy(sizePolicy)
        self.endButton.setObjectName("endButton")
        self.jointControls.addWidget(self.endButton, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.endSpinBox = QtWidgets.QSpinBox(self.jointFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endSpinBox.sizePolicy().hasHeightForWidth())
        self.endSpinBox.setSizePolicy(sizePolicy)
        self.endSpinBox.setMinimumSize(QtCore.QSize(0, 0))
        self.endSpinBox.setMaximum(100)
        self.endSpinBox.setObjectName("endSpinBox")
        self.jointControls.addWidget(self.endSpinBox, 1, 2, 1, 1)
        self.midButton = QtWidgets.QRadioButton(self.jointFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.midButton.sizePolicy().hasHeightForWidth())
        self.midButton.setSizePolicy(sizePolicy)
        self.midButton.setObjectName("midButton")
        self.jointControls.addWidget(self.midButton, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.midSpinBox = QtWidgets.QSpinBox(self.jointFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.midSpinBox.sizePolicy().hasHeightForWidth())
        self.midSpinBox.setSizePolicy(sizePolicy)
        self.midSpinBox.setMinimumSize(QtCore.QSize(0, 0))
        self.midSpinBox.setMaximum(100)
        self.midSpinBox.setObjectName("midSpinBox")
        self.jointControls.addWidget(self.midSpinBox, 1, 1, 1, 1)
        self.baseSpinBox = QtWidgets.QSpinBox(self.jointFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseSpinBox.sizePolicy().hasHeightForWidth())
        self.baseSpinBox.setSizePolicy(sizePolicy)
        self.baseSpinBox.setMinimumSize(QtCore.QSize(0, 40))
        self.baseSpinBox.setMaximum(100)
        self.baseSpinBox.setObjectName("baseSpinBox")
        self.jointControls.addWidget(self.baseSpinBox, 1, 0, 1, 1)
        self.baseButton = QtWidgets.QRadioButton(self.jointFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseButton.sizePolicy().hasHeightForWidth())
        self.baseButton.setSizePolicy(sizePolicy)
        self.baseButton.setObjectName("baseButton")
        self.jointControls.addWidget(self.baseButton, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.jointDiagram.addLayout(self.jointControls, 0, 0, 1, 1)
        self.armDiagram = QtWidgets.QLabel(self.jointFrame)
        self.armDiagram.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.armDiagram.sizePolicy().hasHeightForWidth())
        self.armDiagram.setSizePolicy(sizePolicy)
        self.armDiagram.setMinimumSize(QtCore.QSize(200, 75))
        self.armDiagram.setMaximumSize(QtCore.QSize(1667467, 1667467))
        self.armDiagram.setText("")
        self.armDiagram.setTextFormat(QtCore.Qt.AutoText)
        self.armDiagram.setPixmap(QtGui.QPixmap("armdiagram.png"))
        self.armDiagram.setScaledContents(True)
        self.armDiagram.setAlignment(QtCore.Qt.AlignCenter)
        self.armDiagram.setObjectName("armDiagram")
        self.jointDiagram.addWidget(self.armDiagram, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.jointDiagram, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.jointFrame, 1, 0, 1, 1)
        self.controlsFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlsFrame.sizePolicy().hasHeightForWidth())
        self.controlsFrame.setSizePolicy(sizePolicy)
        self.controlsFrame.setMinimumSize(QtCore.QSize(0, 0))
        self.controlsFrame.setMaximumSize(QtCore.QSize(1666456, 166646))
        self.controlsFrame.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.controlsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controlsFrame.setObjectName("controlsFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.controlsFrame)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.controlsDiagram = QtWidgets.QLabel(self.controlsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlsDiagram.sizePolicy().hasHeightForWidth())
        self.controlsDiagram.setSizePolicy(sizePolicy)
        self.controlsDiagram.setMinimumSize(QtCore.QSize(512, 143))
        self.controlsDiagram.setText("")
        self.controlsDiagram.setTextFormat(QtCore.Qt.PlainText)
        self.controlsDiagram.setPixmap(QtGui.QPixmap(":/xboxmap.png"))
        self.controlsDiagram.setScaledContents(True)
        self.controlsDiagram.setAlignment(QtCore.Qt.AlignCenter)
        self.controlsDiagram.setObjectName("controlsDiagram")
        self.gridLayout_4.addWidget(self.controlsDiagram, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.controlsFrame, 2, 0, 1, 1)
        self.dataFrameLayout = QtWidgets.QHBoxLayout()
        self.dataFrameLayout.setSpacing(0)
        self.dataFrameLayout.setObjectName("dataFrameLayout")
        self.data1Frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data1Frame.sizePolicy().hasHeightForWidth())
        self.data1Frame.setSizePolicy(sizePolicy)
        self.data1Frame.setMinimumSize(QtCore.QSize(200, 0))
        self.data1Frame.setStyleSheet("background-color: rgb(168, 168, 168)")
        self.data1Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data1Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data1Frame.setObjectName("data1Frame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.data1Frame)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.imuLabel = QtWidgets.QLabel(self.data1Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imuLabel.sizePolicy().hasHeightForWidth())
        self.imuLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.imuLabel.setFont(font)
        self.imuLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.imuLabel.setObjectName("imuLabel")
        self.gridLayout_5.addWidget(self.imuLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.imuDisplay = QtWidgets.QTextEdit(self.data1Frame)
        self.imuDisplay.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.imuDisplay.setDocumentTitle("")
        self.imuDisplay.setReadOnly(True)
        self.imuDisplay.setObjectName("imuDisplay")
        self.gridLayout_5.addWidget(self.imuDisplay, 1, 0, 1, 1)
        self.dataFrameLayout.addWidget(self.data1Frame)
        self.data2Frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data2Frame.sizePolicy().hasHeightForWidth())
        self.data2Frame.setSizePolicy(sizePolicy)
        self.data2Frame.setMinimumSize(QtCore.QSize(200, 0))
        self.data2Frame.setStyleSheet("background-color: rgb(168, 168, 168)")
        self.data2Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data2Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data2Frame.setObjectName("data2Frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.data2Frame)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.temperatureLabel = QtWidgets.QLabel(self.data2Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temperatureLabel.sizePolicy().hasHeightForWidth())
        self.temperatureLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.temperatureLabel.setFont(font)
        self.temperatureLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.gridLayout_6.addWidget(self.temperatureLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.temperatureDisplay = QtWidgets.QTextEdit(self.data2Frame)
        self.temperatureDisplay.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.temperatureDisplay.setReadOnly(True)
        self.temperatureDisplay.setObjectName("temperatureDisplay")
        self.gridLayout_6.addWidget(self.temperatureDisplay, 1, 0, 1, 1)
        self.dataFrameLayout.addWidget(self.data2Frame)
        self.gridLayout.addLayout(self.dataFrameLayout, 2, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 949, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.motorControlLabel.raise_()
        self.globalMotorSpeedSpinBox.raise_()
        self.globalMotorSpeedLabel.raise_()

        # Timer which determines when to update graphs and feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.timeout.connect(self.update_feed)
        self.timer.start(1000)

        self.graphLayout = QtWidgets.QVBoxLayout(self.graphFrame)
        self.graphLayout.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.graphLayout.setObjectName("graphLayout")
        self.graph = AccelerationGraph(self.graphFrame, width = 5, height = 4, dpi = 100)
        self.graphLayout.addWidget(self.graph)

        self.start_time = time.time()

        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)

        
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 2)
        self.gridLayout.setRowStretch(2, 1)

        
        self.jointFrame.setMinimumHeight(300)  
        self.graphFrame.setMinimumHeight(400)  

        self.motorControlsFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.graphFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.jointFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.controlsFrame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.data1Frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.data2Frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #checks if the global speed box has changed and if it has updates the other joints to reflect
        self.globalMotorSpeedSpinBox.valueChanged.connect(self.update_joint_speeds)
        
        #checks if any one of the three individual joint speeds has changed and if so clears the global speed box to reflect
        self.baseSpinBox.valueChanged.connect(self.clear_global_speed)
        self.midSpinBox.valueChanged.connect(self.clear_global_speed)
        self.endSpinBox.valueChanged.connect(self.clear_global_speed)

        # Maximize the window to ensure full scaling on start
        MainWindow.showMaximized()
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Rover Team 3 Base Station", "Rover Team 3 Base Station"))
        self.motorControlLabel.setText(_translate("Rover Team 3 Base Station", "Motor Controls"))
        self.globalMotorSpeedLabel.setText(_translate("Rover Team 3 Base Station", "Global Motor Speed"))
        self.endButton.setText(_translate("Rover Team 3 Base Station", "End"))
        self.midButton.setText(_translate("Rover Team 3 Base Station", "Mid"))
        self.baseButton.setText(_translate("Rover Team 3 Base Station", "Base"))
        self.imuLabel.setText(_translate("Rover Team 3 Base Station", "IMU Data Feed"))
        self.imuDisplay.setHtml(_translate("Rover Team 3 Base Station", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.temperatureLabel.setText(_translate("Rover Team 3 Base Station", "Temperature Data Feed"))
        self.temperatureDisplay.setHtml(_translate("Rover Team 3 Base Station", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def update_data(self):
        simulation = random.uniform(-10, 10) # placeholder, will later be IMU data
        self.graph.update_graph(simulation)

    def update_feed(self):
        elapsed_time = int(time.time() - self.start_time)
        format_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time)) #Formatting for how time prints out
        
        imuData = "No Data"             # Placeholder for now, but eventually will need a specific case where it prints no data if no data is recieved
        temperature = "No Data"         # also placeholder

        new_imuData = f"{format_time} - {imuData}"
        new_temperature = f"{format_time} - {temperature}"

        self.imuDisplay.append(new_imuData)
        self.temperatureDisplay.append(new_temperature)

    # Functions that retrieve the motor speed set in the spinbox for global, base, mid, and end
    def get_global_speed(self):
        global_speed = self.globalMotorSpeedSpinBox.value()
        return global_speed
    
    def get_base_speed(self):
        base_speed = self.baseSpinBox.value()
        return base_speed
    
    def get_mid_speed(self):
        mid_speed = self.midSpinBox.value()
        return mid_speed
    
    def get_end_speed(self):
        end_speed = self.endSpinBox.value()
        return end_speed
    

    def update_joint_speeds(self):
        global_speed = self.globalMotorSpeedSpinBox.value()
        self.globalMotorSpeedSpinBox.setRange(0, 100)

        #prevent triggering self.clear_global_speed
        self.baseSpinBox.blockSignals(True)
        self.midSpinBox.blockSignals(True)
        self.endSpinBox.blockSignals(True)

        self.baseSpinBox.setValue(global_speed)
        self.midSpinBox.setValue(global_speed)
        self.endSpinBox.setValue(global_speed)

        #re-enable signals for spinboxes
        self.baseSpinBox.blockSignals(False)
        self.midSpinBox.blockSignals(False)
        self.endSpinBox.blockSignals(False)

    def clear_global_speed(self):
        self.globalMotorSpeedSpinBox.blockSignals(True)
        self.globalMotorSpeedSpinBox.setRange(-1, 100)
        self.globalMotorSpeedSpinBox.setValue(-1)
        self.globalMotorSpeedSpinBox.blockSignals(False)


    # Enum class for joints on the arm
    class Joint(Enum):
        BASE = 0
        MID = 1
        END = 2

    # Initialize currentJoint
    currentJoint = None

    # Check which joint is selected
    def check_current_joint(self):
        if self.baseButton.isChecked():
            currentJoint = self.Joint.BASE
        elif self.midButton.isChecked():
            currentJoint = self.Joint.MID
        elif self.endButton.isChecked():
            currentJoint = self.Joint.END

class TalkerNode(Node):

    def __init__(self, ui):
        super().__init__("talker_node")
        self.publisher_ = self.create_publisher(String, 'motor_speed', 10)
        self.global_speed_ = 0
        self.ui = ui
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        self.global_speed_ = self.ui.globalMotorSpeedSpinBox.value()
        msg.data = "Test message " + str(self.global_speed_)
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: " + msg.data)

def main(args=None):
    rclpy.init(args=args)       # Initializes ROS2 communications & features
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    node = TalkerNode(ui)
    rclpy.spin(node)            # keeps the node alive
    rclpy.shutdown()            # Ends ROS2 communications

    sys.exit(app.exec_())

if __name__ == "__main__":
        main()