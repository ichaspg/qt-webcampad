import sys
from PySide6.QtCore import Qt, QTimer, QObject, Signal, Slot, QThread
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
import pygame

class JoyStickHandler(QObject):
  connection_status_changed = Signal(bool)
  button_pressed = Signal(int)
  button_released = Signal(int)
  axis_moved = Signal(int,float)

  def __init__(self):
    super().__init__()

  def run(self):
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
      print("No Joystick Found!")
      return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    self.emit_connection_status_changed(True)

    try:
      while True:
        for event in pygame.event.get():
          if event.type == pygame.JOYBUTTONDOWN:
              self.button_pressed.emit(event.button)
          elif event.type == pygame.JOYBUTTONUP:
              self.button_released.emit(event.button)
          elif event.type == pygame.JOYAXISMOTION:
                self.axis_moved.emit(event.axis, event.value)

        QThread.msleep(10)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
      pygame.quit()
      self.emit_connection_status_changed(False)
          
  def emit_connection_status_changed(self, connected):
    self.connection_status_changed.emit(connected)
