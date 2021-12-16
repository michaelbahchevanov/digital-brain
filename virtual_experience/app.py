import sys
sys.path.insert(0, "../")

from digital_brain.computer_vision.model.facial_detector import FaceDetector
from digital_brain.computer_vision.model.utils.capture import Capture
from digital_brain.computer_vision.model.hand_detector import HandDetector
from digital_brain.computer_vision.common.constants import JOINTS_LANDMARKS


capture = Capture()
face_detector = FaceDetector()
hand_detector = HandDetector()

while True:
    capture.start()
    frame = capture.frame

    _, bbox_data = face_detector.find_faces(frame, draw_detections=False)
    detections, f = hand_detector.find_hands(frame, draw=True)

    if detections:
        det_lms = detections[0]["lms"]
        det_bbox = detections[0]["bbox"]
        distance, img = hand_detector.measure_distance(det_lms[JOINTS_LANDMARKS.THUMB_TIP], det_lms[JOINTS_LANDMARKS.PINKY_TIP], frame)

    capture.show()

    if capture.wait_exit():
        break

capture.cleanup()
