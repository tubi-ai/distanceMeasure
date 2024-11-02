import sys
import serial
import cv2  # Import OpenCV
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
import pyqtgraph as pg  # Make sure you import pyqtgraph if you're using it

class MesafeOlcer(QWidget):
    def __init__(self):
        super().__init__()
        self.threshold = 50  # Default threshold value
        self.warning_history = []  # A list for alert history
        self.arduino = serial.Serial('/dev/cu.usbserial-1110', 9600)  # Check your Arduino port
        self.camera = cv2.VideoCapture(0)  # Open the Mac's built-in camera
        self.initUI()  # Call initUI after initializing attributes

    def initUI(self):
        self.setWindowTitle('Distance Meter and Warning System')
        self.setGeometry(100, 100, 800, 900)

        layout = QVBoxLayout()
        
        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(5, 100)
        self.slider.setValue(self.threshold)
        self.slider.valueChanged.connect(self.updateThreshold)
    
        # Graph
        self.graph = pg.PlotWidget()
        self.graph.setYRange(0, 200)
        self.data = []        
        self.distance_label = QLabel('Mesafe: -- cm')
        self.threshold_label = QLabel('Eşik: -- cm')
        self.warning_label = QLabel('Uyarı: --')
        
        # Alert history table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Mesafe (cm)", "Zaman"])        

        layout.addWidget(self.distance_label)
        layout.addWidget(self.threshold_label)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.graph)   
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Start the timer
        self.startTimer(500)
    
    def updateThreshold(self, value):
        self.threshold = value
        self.threshold_label.setText(f'Eşik: {self.threshold} cm')
    
    def timerEvent(self, event):
        if self.arduino.inWaiting() > 0:
            data = self.arduino.readline().decode().strip()
            try:
                #distance = float(data)
                distance, threshold = map(float, data.split(','))
                self.distance_label.setText(f'Distance: {distance:.2f} cm')
        
                # Update chart
                self.data.append(distance)
                if len(self.data) > 100:
                    self.data.pop(0)
                self.graph.plot(self.data, clear=True)
        
                # Warning control
                if distance < self.threshold:
                    self.warning_label.setText('Warning: Distance Too Short!')
                    self.warning_label.setStyleSheet('color: red;')
                    self.logWarning(distance)
                    self.capture_photo()  # Take a photo if the distance is too short
                else:
                    self.warning_label.setText('Warning: Safe')
                    self.warning_label.setStyleSheet('color: green;')
            except ValueError:
                pass

    def capture_photo(self):
        ret, frame = self.camera.read()  # Capture a frame from the camera
        if ret:
            # Save the photo with a timestamp
            filename = 'photo_capture.jpg'
            cv2.imwrite(filename, frame)
            print(f'Photo saved as {filename}')

    def closeEvent(self, event):
        # Release the camera when closing the application
        self.camera.release()
        super().closeEvent(event)
    
    def logWarning(self, distance):
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        self.warning_history.append((distance, current_time))
        self.table.insertRow(self.table.rowCount())
        self.table.setItem(self.table.rowCount()-1, 0, QTableWidgetItem(f"{distance:.2f} cm"))
        self.table.setItem(self.table.rowCount()-1, 1, QTableWidgetItem(current_time))    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MesafeOlcer()
    window.show()
    sys.exit(app.exec_())
