from PySide6.QtCore import QObject, QThread, Signal,Slot
import sys
from PySide6.QtMultimedia import QImageCapture,QCamera, QMediaDevices, QMediaCaptureSession
from PySide6.QtMultimediaWidgets import QVideoWidget

class CameraHandler(QObject):
  camera_started = Signal(QMediaCaptureSession)
  camera_stopped = Signal()

  def __init__(self):
    super().__init__()
    
  def run(self):
    self._capture_session = None
    self._camera = None
    self._camera_info = None
    
    available_cameras = QMediaDevices.videoInputs()
    if available_cameras:
      self._camera_info = available_cameras[0]
      self._camera = QCamera(self._camera_info)
      self._capture_session = QMediaCaptureSession()
      self._capture_session.setCamera(self._camera)
    
    self._camera_viewFinder = QVideoWidget()
    self._capture_session.setVideoOutput(self._camera_viewFinder)
    self._camera.start()



    

  




    
    


