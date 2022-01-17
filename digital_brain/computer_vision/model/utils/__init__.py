"""Utilities for the models"""
import cv2
import numpy as np

class Draggable():
    """Class for creating draggable objects via 2D coordinate position"""

    def __init__(self, path, origin, img_type):
        """
        Args:
            path: the path to the image
            origin: the origin 2D coordinate position of the image
            img_type: the type of image; supports png and jpg
        Returns:
            a draggable image
        Raises:
            -
        """

        self.origin = origin
        self.path = path
        self.img_type = img_type

        if self.img_type == 'png':
            self.img = cv2.imread(self.path, cv2.IMREAD_UNCHANGED)
        else:
            self.img = cv2.imread(self.path)

        self.size = self.img.shape[:2]

        if self.size[0] > 512 or self.size[1] > 512:
            self.img = cv2.resize(self.img, (512, 512), interpolation=cv2.INTER_AREA)
            self.size = self.img.shape[:2]

        if self.size[0] > 150 or self.size[1] > 150:
            scale_percent = 70 if self.size[0] >= 250 and self.size[1] >= 250 else 60
            width = int(self.size[1] * scale_percent / 100)
            height = int(self.size[0] * scale_percent / 100)
            new_dims = (width, height)
            self.img = cv2.resize(self.img, new_dims, interpolation=cv2.INTER_AREA)

    def overlay(self, frame, pos=(0, 0)):
        """Overlays transparent images on a canvas/frame
        Args:
            self: the reference to the object
            frame: the frame for overlaying the image on
            pos: the 2D coordinates of the image
        Returns:
            a frame with an overlayed image
        Raises:
            -
        """
        h_img, w_img, _ = self.img.shape
        h_frame, w_frame, c_frame = frame.shape
        # Get mask
        *_, mask = cv2.split(self.img)
        # Create 2 masks: with and without alpha for the frame
        maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
        maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        # Overlay img on mask
        imgBGRA = cv2.bitwise_and(self.img, maskBGRA)
        # Convert to BGR
        imgBGR = cv2.cvtColor(imgBGRA, cv2.COLOR_BGRA2BGR)

        # Create image mask
        imgMaskFull = np.zeros((h_frame, w_frame, c_frame), np.uint8)
        imgMaskFull[pos[1]:h_img + pos[1], pos[0]:w_img + pos[0], :] = imgBGR
        imgMaskFull2 = np.ones((h_frame, w_frame, c_frame), np.uint8) * 255
        maskBGRInv = cv2.bitwise_not(maskBGR)
        imgMaskFull2[pos[1]:h_img + pos[1], pos[0]:w_img + pos[0], :] = maskBGRInv

        # Overlay image on frame
        frame = cv2.bitwise_and(frame, imgMaskFull2)
        frame = cv2.bitwise_or(frame, imgMaskFull)

        return frame

    def update_hand_tracking(self, tracker):
        """Updates the location of the image based on a chosen landmark tracker (anchor)
        Args:
            tracker: the landmark used as anchor point
        Returns:
            None
        Raises:
            -
        """
        ox, oy = self.origin
        h, w = self.size

        if ox < tracker[0] < ox + w and oy < tracker[1] < oy + h:
            self.origin = tracker[0] - w // 2, tracker[1] - h // 2

class Capture:
    """A layer of abstraction on top of Opencv2's camera I/O"""
    def __init__(self, src=0, dimensions=(640, 480)):
        self.cap = cv2.VideoCapture(src)
        self.set_dimensions(dimensions)
        self.isSuccess = False
        self.frame = None

    def start(self):
        self.isSuccess, self.frame = self.cap.read()
        return self

    def set_dimensions(self, dimensions):
        width, height = dimensions
        self.cap.set(3, width)
        self.cap.set(4, height)

    def get_dimensions(self):
        return int(self.cap.get(3)), int(self.cap.get(4))

    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def show(self, name="Capture"):
        cv2.imshow(name, self.frame)

    def wait_exit(self, key='q'):
        if cv2.waitKey(10) & 0xFF == ord(key):
            return True
        return False
    
    def flip(self):
        cv2.flip(self.frame, 1)
        return self
    
    def set_frame(self, val):
        self.frame = val

def draw_tooltip(frame, origin=(0, 0), item_name="", description=""):
    w, h = frame.shape[:2]
    cv2.rectangle(frame, (origin[0] + 50, origin[1] + 50),
                                  (origin[0] - 175, origin[1] - 250),
                                  (0, 255, 25), 2)
    return frame



if __name__ == "__main__":
    pass
