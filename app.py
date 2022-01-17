from digital_brain.computer_vision.model.utils import Capture
from digital_brain.computer_vision.model.facial_detector import FaceDetector

capture = Capture()
face_detector = FaceDetector()

while True:
    capture.start()

    _, bbox_data = face_detector.find_faces(capture.frame)

    capture.show()

    if capture.wait_exit():
        break

capture.cleanup()
