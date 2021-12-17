import cv2


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


if __name__ == "__main__":
    pass
