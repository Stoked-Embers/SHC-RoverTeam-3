from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap #QPixmap is the library used for importing/displaying images in the UI
import sys
#This is the tutorial that I am following for loading the image:
# https://www.geeksforgeeks.org/pyqt5-how-to-add-image-in-window/
app = QApplication([])
window = QWidget()
xboxControllerMapImage = QPixmap('Xbox Controller Map.xlsx - EXPERIMENTAL_Pilot Controller conv 1.png')
label = QLabel('Rover Team 3 Base Station')
label.setPixmap(xboxControllerMapImage)
label.show()
app.exec()