import cv2
import mediapipe as mp
import math as m


class HandDetector:

    def __init__(self, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon, 
                                        min_tracking_confidence = self.minTrackCon)
        self.draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True, is_flipped=True):
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frameRGB)
        hands = []
        h, w = frame.shape[:2]
        if  self.results.multi_hand_landmarks:
            for handType,handLms in zip(self.results.multi_handedness,self.results.multi_hand_landmarks):
                detected_hand={}
                lms = []
                x_coords = []
                y_coords = []
                for _, lm in enumerate(handLms.landmark):
                    px, py = int(lm.x * w), int(lm.y * h)
                    lms.append([px, py])
                    x_coords.append(px)
                    y_coords.append(py)

                xmin, xmax = min(x_coords), max(x_coords)
                ymin, ymax = min(y_coords), max(y_coords)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                detected_hand["lms"] = lms
                detected_hand["bbox"] = bbox
                detected_hand["center"] =  (cx, cy)

                if is_flipped:
                    if handType.classification[0].label == "Right":
                        detected_hand["type"] = "Left"
                    else:
                        detected_hand["type"] = "Right"
                else: detected_hand["type"] = handType.classification[0].label
                hands.append(detected_hand)

                if draw:
                    self.draw.draw_landmarks(frame, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(frame, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(frame,detected_hand["type"],(bbox[0] - 30, bbox[1] - 30),cv2.FONT_HERSHEY_PLAIN,
                                2,(255, 0, 255),2)
        return hands
        
    def distance_from_landmarks(self, lm1, lm2):
        x1, y1 = lm1
        x2, y2 = lm2
        distance = m.hypot(x2 - x1, y2 - y1)
        return distance

    def direction_from_landmarks(self, lm1, lm2):
        x1, y1 = lm1
        x2, y2 = lm2
        direction = 'out' if x1 > x2 else 'in'
        return direction

    def is_grabbed_from_landmarks(self, lm1, lm2):
        distance = self.distance_from_landmarks(lm1, lm2)
        if distance < 250:
            return True
        return False

    def draw_direction_from_landmarks(self, frame, lm1, lm2):
        x1, y1 = lm1
        x2, y2 = lm2
        distance = self.distance_from_landmarks(lm1, lm2)

        cv2.arrowedLine(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.putText(frame,str(int(distance)),(100, 150), cv2.FONT_HERSHEY_PLAIN,
                            2,(255, 0, 255),2)

    def draw_state(self, frame, lm1, lm2):
        is_grabbed = self.is_grabbed_from_landmarks(lm1, lm2)
        hand_direction = self.direction_from_landmarks(lm1, lm2)
        
        if is_grabbed:
            cv2.putText(frame, "grabbed", (100, 200), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        if hand_direction == "left":
            cv2.putText(frame, "facing out", (100, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        elif hand_direction == "right":
            cv2.putText(frame, "facing in", (100, 250), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

