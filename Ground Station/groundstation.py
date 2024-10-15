import sys
from PyQt5.QtWidgets import * #TODO: Change to imported methods when complete
from PyQt5.QtGui import * #TODO: Change to imported methods when complete
app = QApplication([])
app.setStyle('Fusion')
#QPixmap is the library used for importing/displaying images in the UI
#This is the tutorial that I am following for loading the image:
# https://www.geeksforgeeks.org/pyqt5-how-to-add-image-in-window/

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.setWindowTitle("Rover Team 3 Base Station")
        
     






app = QApplication(sys.argv)

window = MainWindow()
window.show()

class displayImage(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

    



app.exec()
window = MainWindow()
window.show()

