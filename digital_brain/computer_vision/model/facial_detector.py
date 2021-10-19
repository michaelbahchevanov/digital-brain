import mediapipe as mp
import cv2 as cv


class FaceDetector:
    """"Facial detection using MediaPipe's BlazeFace solution"""
    def __init__(self, min_detection_confidence=0.5):

        self.min_detection_confidence = min_detection_confidence
        self.mp_solution = mp.solutions.face_detection
        self.detector = self.mp_solution.FaceDetection(self.min_detection_confidence)
        self.results = []

    def find_faces(self, image, draw_detections=False):

        def draw_detection(img, det, offset=20):
            cv.rectangle(img, bbox, (255, 0, 255), 2)
            cv.putText(image, f'{int(det.score[0] * 100)}%', (bbox[0], bbox[1] - offset),
                       cv.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 0, 255), 2)

        img_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.results = self.detector.process(img_rgb)

        bboxes = []
        if self.results.detections:
            for i, detection in enumerate(self.results.detections):
                relative_bbox = detection.location_data.relative_bounding_box
                h, w = image.shape[:2]
                bbox = int(relative_bbox.xmin * w), int(relative_bbox.ymin * h), \
                       int(relative_bbox.width * w), int(relative_bbox.height * h)
                center_x, center_y = bbox[0] + (bbox[2] // 2), \
                                     bbox[1] + (bbox[3] // 2)
                bbox_data = {"seq_num": i, "bounding_box": bbox,
                             "detection_score": detection.score, "center_points": (center_x, center_y)}
                bboxes.append(bbox_data)
                if draw_detections:
                    draw_detection(image, detection)

        return image, bboxes
