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
    detections = hand_detector.find_hands(frame, draw=False)


    if detections:
        det_lms = detections[0]["lms"]
        det_bbox = detections[0]["bbox"]
        thumb_tip, pinky_tip = det_lms[JOINTS_LANDMARKS.THUMB_TIP], det_lms[JOINTS_LANDMARKS.PINKY_TIP]

        hand_direction = hand_detector.direction_from_landmarks(thumb_tip, pinky_tip)
        is_grabbed = hand_detector.is_grabbed_from_landmarks(thumb_tip, pinky_tip)
        hand_detector.draw_direction_from_landmarks(frame, thumb_tip, pinky_tip)

        if hand_direction == 'left' and is_grabbed:
            print('grabbed, facing out')
        elif hand_direction == 'right' and is_grabbed:
            print('show cool tooltip here')

    capture.show()

    if capture.wait_exit():
        break

capture.cleanup()
