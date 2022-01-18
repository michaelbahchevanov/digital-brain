import sys
sys.path.insert(0, "../")
import os

from digital_brain.computer_vision.model.facial_detector import FaceDetector
from digital_brain.computer_vision.model.hand_detector import HandDetector
from digital_brain.computer_vision.common.constants import JOINTS_LANDMARKS
from digital_brain.computer_vision.model.utils import Draggable, Capture


capture = Capture(dimensions=(1280, 720))
face_detector = FaceDetector()
hand_detector = HandDetector()

assets_path = 'assets'
dir_list = os.listdir(assets_path)

img_list = []
for i, img_path in enumerate(dir_list):
    if 'png' in img_path:
        img_type = 'png'
    else:
        img_type = 'jpg'

    img_list.append(Draggable(f'{assets_path}/{img_path}', [100, 50 + i * 125], img_type))

while True:
    capture.start()
    frame = capture.frame

    _, bbox_data = face_detector.find_faces(frame, draw_detections=False)
    detections = hand_detector.find_hands(frame, draw=False, is_flipped=False)

    if detections:
        det_lms = detections[0]["lms"]
        det_bbox = detections[0]["bbox"]
        thumb_tip, pinky_tip = det_lms[JOINTS_LANDMARKS.THUMB_TIP], det_lms[JOINTS_LANDMARKS.PINKY_TIP]

        hand_direction = hand_detector.direction_from_landmarks(thumb_tip, pinky_tip)
        is_grabbed = hand_detector.is_grabbed_from_landmarks(thumb_tip, pinky_tip)
        
        distance = hand_detector.distance_from_landmarks(thumb_tip, pinky_tip)

        if is_grabbed:
            for img in img_list:
                img.update_hand_tracking(thumb_tip)
                if hand_direction == "in":
                    tooltip = Draggable(f"./Tooltip Prototype.png", [ox, oy], 'png')
                else:
                    tooltip = None

    try:
        for img in img_list:
            h, w = img.size
            ox, oy = img.origin

            if img.img_type == 'png':
                frame = img.overlay(frame, (ox, oy))
                if tooltip:
                    frame = tooltip.overlay(frame, (ox-400, oy-200))
                capture.set_frame(frame)
            else:
                # Not fully supported, keep to png
                frame[oy: oy + h, ox: ox + w] = img.img
                capture.set_frame(frame)
    except Exception as e:
        pass

    capture.show()

    if capture.wait_exit():
        break

capture.cleanup()
