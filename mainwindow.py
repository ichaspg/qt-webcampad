# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from pad import JoyStickHandler
import pygame
from PySide6.QtCore import Qt, QTimer, QObject, Signal, Slot, QThread
from camera import CameraHandler
from PySide6.QtMultimedia import QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Create and start the gamepad handler thread
        self.gamepad_handler = JoyStickHandler()
        self.gamepad_thread = QThread()
        self.gamepad_handler.moveToThread(self.gamepad_thread)
        self.gamepad_thread.started.connect(self.gamepad_handler.run)
        self.gamepad_thread.start()

        # Connect signals from the gamepad handler
        self.gamepad_handler.button_pressed.connect(self.on_button_pressed)
        self.gamepad_handler.button_released.connect(self.on_button_released)
        self.gamepad_handler.axis_moved.connect(self.on_axis_moved)
        self.gamepad_handler.connection_status_changed.connect(self.connection_stat)
        

        #Camera Thread
        self.camera_handler = CameraHandler()
        self.camera_thread = QThread()
        self.camera_handler.moveToThread(self.camera_thread)
        self.camera_thread.started.connect(self.camera_handler.run)
        self.video_widget = QVideoWidget()
        self.ui.tabWidget.addTab(self.video_widget,"Camera")
        self.camera_thread.start()

        #Signal Camera Handler
        self.camera_handler.camera_started.connect(self.camera_connected)

    @Slot(int)
    def on_button_pressed(self, button):
        print(f"Button {button} pressed")
        self.ui.button_label.setText(f"Button Input: {button}")

    @Slot(int)
    def on_button_released(self, button):
        print(f"Button {button} released")
        # Add your custom logic here

    @Slot(int, float)
    def on_axis_moved(self, axis, value):
        print(f"Axis {axis} moved, value: {value}")
        self.ui.analog_label.setText(f"Analog Input : Axis : {axis}, Value: {value:.2f}")

    @Slot(bool)
    def connection_stat(self, connected):
        if connected :
            self.ui.connect_status.setText("Connection Status : Connected")
        else :
            self.ui.connect_status.setText("Connection Status : Disconnect")
    
    @Slot(QMediaCaptureSession)
    def camera_connected(self, session):
        session.setVideoOutput(self.video_widget)

        
    def closeEvent(self, event):
        pygame.quit()
        self.gamepad_thread.quit()
        self.gamepad_thread.wait()  # Wait for the gamepad thread to finish
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
