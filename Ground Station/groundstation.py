# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groundstation.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import time
import random
from enum import Enum
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import PyQt5
PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

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
        self.axes.plot(self.x_data, self.y_data, label="Accelration (m/s^2)")
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Acceleration (m/s^2)")
        self.axes.set_title("Acceleration Data")
        self.axes.legend(loc = "upper left")
        self.draw()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1071, 784)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        self.motorControlsFrame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.motorControlsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.motorControlsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.motorControlsFrame.setObjectName("motorControlsFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.motorControlsFrame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.motorControlsBackground = QtWidgets.QGraphicsView(self.motorControlsFrame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.motorControlsBackground.setFont(font)
        self.motorControlsBackground.setStyleSheet("background-color: rgb(0, 85, 255)\n"
"")
        self.motorControlsBackground.setObjectName("motorControlsBackground")
        self.gridLayout_2.addWidget(self.motorControlsBackground, 1, 1, 1, 1)
        self.motorControlsLayout = QtWidgets.QGridLayout()
        self.motorControlsLayout.setContentsMargins(200, 50, 200, 50)
        self.motorControlsLayout.setObjectName("motorControlsLayout")
        self.globalMotorSpeedSpinBox = QtWidgets.QSpinBox(self.motorControlsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.globalMotorSpeedSpinBox.sizePolicy().hasHeightForWidth())
        self.globalMotorSpeedSpinBox.setSizePolicy(sizePolicy)
        self.globalMotorSpeedSpinBox.setMaximum(100)
        self.globalMotorSpeedSpinBox.setObjectName("globalMotorSpeedSpinBox")
        self.motorControlsLayout.addWidget(self.globalMotorSpeedSpinBox, 2, 0, 1, 1)
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
        self.motorControlLabel.setStyleSheet("color: rgb(255, 255, 255)")
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
        self.gridLayout_2.addLayout(self.motorControlsLayout, 0, 0, 2, 2)
        self.gridLayout.addWidget(self.motorControlsFrame, 0, 0, 1, 1)
        self.graphFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphFrame.sizePolicy().hasHeightForWidth())
        self.graphFrame.setSizePolicy(sizePolicy)
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
        self.jointFrame.setMinimumSize(QtCore.QSize(500, 300))
        self.jointFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.jointFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.jointFrame.setObjectName("jointFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.jointFrame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.jointBackground = QtWidgets.QGraphicsView(self.jointFrame)
        self.jointBackground.setMinimumSize(QtCore.QSize(350, 200))
        self.jointBackground.setObjectName("jointBackground")
        self.gridLayout_3.addWidget(self.jointBackground, 0, 0, 1, 1)
        self.layoutWidget = QtWidgets.QWidget(self.jointFrame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 481, 281))
        self.layoutWidget.setObjectName("layoutWidget")
        self.jointDiagram = QtWidgets.QGridLayout(self.layoutWidget)
        self.jointDiagram.setContentsMargins(0, 0, 0, 0)
        self.jointDiagram.setObjectName("jointDiagram")
        self.jointControls = QtWidgets.QGridLayout()
        self.jointControls.setObjectName("jointControls")
        self.endButton = QtWidgets.QRadioButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endButton.sizePolicy().hasHeightForWidth())
        self.endButton.setSizePolicy(sizePolicy)
        self.endButton.setObjectName("endButton")
        self.jointControls.addWidget(self.endButton, 0, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.endSpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.endSpinBox.sizePolicy().hasHeightForWidth())
        self.endSpinBox.setSizePolicy(sizePolicy)
        self.endSpinBox.setMinimumSize(QtCore.QSize(0, 40))
        self.endSpinBox.setMaximum(100)
        self.endSpinBox.setObjectName("endSpinBox")
        self.jointControls.addWidget(self.endSpinBox, 1, 2, 1, 1)
        self.midButton = QtWidgets.QRadioButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.midButton.sizePolicy().hasHeightForWidth())
        self.midButton.setSizePolicy(sizePolicy)
        self.midButton.setObjectName("midButton")
        self.jointControls.addWidget(self.midButton, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.midSpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.midSpinBox.sizePolicy().hasHeightForWidth())
        self.midSpinBox.setSizePolicy(sizePolicy)
        self.midSpinBox.setMinimumSize(QtCore.QSize(0, 40))
        self.midSpinBox.setMaximum(100)
        self.midSpinBox.setObjectName("midSpinBox")
        self.jointControls.addWidget(self.midSpinBox, 1, 1, 1, 1)
        self.baseSpinBox = QtWidgets.QSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseSpinBox.sizePolicy().hasHeightForWidth())
        self.baseSpinBox.setSizePolicy(sizePolicy)
        self.baseSpinBox.setMinimumSize(QtCore.QSize(0, 40))
        self.baseSpinBox.setMaximum(100)
        self.baseSpinBox.setObjectName("baseSpinBox")
        self.jointControls.addWidget(self.baseSpinBox, 1, 0, 1, 1)
        self.baseButton = QtWidgets.QRadioButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baseButton.sizePolicy().hasHeightForWidth())
        self.baseButton.setSizePolicy(sizePolicy)
        self.baseButton.setObjectName("baseButton")
        self.jointControls.addWidget(self.baseButton, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.jointDiagram.addLayout(self.jointControls, 0, 0, 1, 1)
        self.armDiagram = QtWidgets.QLabel(self.layoutWidget)
        self.armDiagram.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.armDiagram.sizePolicy().hasHeightForWidth())
        self.armDiagram.setSizePolicy(sizePolicy)
        self.armDiagram.setMinimumSize(QtCore.QSize(0, 0))
        self.armDiagram.setText("")
        self.armDiagram.setPixmap(QtGui.QPixmap("images/armdiagram.png"))
        self.armDiagram.setScaledContents(True)
        self.armDiagram.setAlignment(QtCore.Qt.AlignCenter)
        self.armDiagram.setObjectName("armDiagram")
        self.jointDiagram.addWidget(self.armDiagram, 1, 0, 1, 1)
        self.jointBackground.raise_()
        self.layoutWidget.raise_()
        self.gridLayout.addWidget(self.jointFrame, 1, 0, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.controlsFrame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlsFrame.sizePolicy().hasHeightForWidth())
        self.controlsFrame.setSizePolicy(sizePolicy)
        self.controlsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controlsFrame.setObjectName("controlsFrame")
        self.controlsBackground = QtWidgets.QGraphicsView(self.controlsFrame)
        self.controlsBackground.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.controlsBackground.setStyleSheet("")
        self.controlsBackground.setObjectName("controlsBackground")
        self.controlsDiagram = QtWidgets.QLabel(self.controlsFrame)
        self.controlsDiagram.setGeometry(QtCore.QRect(0, 40, 501, 161))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlsDiagram.sizePolicy().hasHeightForWidth())
        self.controlsDiagram.setSizePolicy(sizePolicy)
        self.controlsDiagram.setText("")
        self.controlsDiagram.setTextFormat(QtCore.Qt.PlainText)
        self.controlsDiagram.setPixmap(QtGui.QPixmap("images/xboxmap.png"))
        self.controlsDiagram.setScaledContents(True)
        self.controlsDiagram.setAlignment(QtCore.Qt.AlignCenter)
        self.controlsDiagram.setObjectName("controlsDiagram")
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
        self.data1Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data1Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data1Frame.setObjectName("data1Frame")
        self.data1Background = QtWidgets.QGraphicsView(self.data1Frame)
        self.data1Background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.data1Background.setStyleSheet("background-color: rgb(168, 168, 168);")
        self.data1Background.setObjectName("data1Background")
        self.temperatureLabel = QtWidgets.QLabel(self.data1Frame)
        self.temperatureLabel.setGeometry(QtCore.QRect(100, 10, 71, 16))
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
        self.temperatureDisplay = QtWidgets.QTextEdit(self.data1Frame)
        self.temperatureDisplay.setGeometry(QtCore.QRect(10, 30, 241, 171))
        self.temperatureDisplay.setDocumentTitle("")
        self.temperatureDisplay.setReadOnly(True)
        self.temperatureDisplay.setObjectName("temperatureDisplay")
        self.dataFrameLayout.addWidget(self.data1Frame)
        self.data2Frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data2Frame.sizePolicy().hasHeightForWidth())
        self.data2Frame.setSizePolicy(sizePolicy)
        self.data2Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.data2Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.data2Frame.setObjectName("data2Frame")
        self.data2Background = QtWidgets.QGraphicsView(self.data2Frame)
        self.data2Background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.data2Background.setStyleSheet("background-color: rgb(168, 168, 168);")
        self.data2Background.setObjectName("data2Background")
        self.pressureLabel = QtWidgets.QLabel(self.data2Frame)
        self.pressureLabel.setGeometry(QtCore.QRect(110, 10, 41, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pressureLabel.sizePolicy().hasHeightForWidth())
        self.pressureLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pressureLabel.setFont(font)
        self.pressureLabel.setStyleSheet("color: rgb(255, 255, 255)")
        self.pressureLabel.setObjectName("pressureLabel")
        self.pressureDisplay = QtWidgets.QTextEdit(self.data2Frame)
        self.pressureDisplay.setGeometry(QtCore.QRect(10, 30, 241, 171))
        self.pressureDisplay.setReadOnly(True)
        self.pressureDisplay.setObjectName("pressureDisplay")
        self.dataFrameLayout.addWidget(self.data2Frame)
        self.gridLayout.addLayout(self.dataFrameLayout, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1071, 22))
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
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Rover Team 3 Base Station", "Rover Team 3 Base Station"))
        self.motorControlLabel.setText(_translate("Rover Team 3 Base Station", "Motor Controls"))
        self.globalMotorSpeedLabel.setText(_translate("Rover Team 3 Base Station", "Global Motor Speed"))
        self.endButton.setText(_translate("Rover Team 3 Base Station", "End"))
        self.midButton.setText(_translate("Rover Team 3 Base Station", "Mid"))
        self.baseButton.setText(_translate("Rover Team 3 Base Station", "Base"))
        self.temperatureLabel.setText(_translate("Rover Team 3 Base Station", "Temperature"))
        self.temperatureDisplay.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.875pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pressureLabel.setText(_translate("MainWindow", "Pressure"))
        self.pressureDisplay.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
        
        temperature = "No Data"             # Placeholder for now, but eventually will need a specific case where it prints no data if no data is recieved
        pressure = "No Data"                # also placeholder

        new_temperature = f"{format_time} - {temperature}"
        new_pressure = f"{format_time} - {pressure}"

        self.temperatureDisplay.append(new_temperature)
        self.pressureDisplay.append(new_pressure)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
