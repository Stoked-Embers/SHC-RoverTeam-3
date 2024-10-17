import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.axes.legend(loc = "upper left")
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-Time IMU Data Plot")
        self.setGeometry(100, 100, 800, 600)

        # Set up the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Create the Matplotlib plot and add it to the layout
        self.plot = AccelerationGraph(self.central_widget, width=5, height=4, dpi=100)
        layout.addWidget(self.plot)

        # Create a QTimer to simulate real-time data updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second (1000 ms)

    def update_data(self):
        # Simulate receiving new data from IMU (replace with actual IMU data later)
        simulated_acceleration = random.uniform(-10, 10)  # Placeholder for IMU acceleration data
        self.plot.update_graph(simulated_acceleration)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())