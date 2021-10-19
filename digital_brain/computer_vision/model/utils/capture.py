import cv2 as cv


class Capture:
    """A layer of abstraction on top of OpenCV's camera I/O"""
    def __init__(self, src=0, dimensions=(640, 480)):
        self.cap = cv.VideoCapture(src)
        self.set_dimensions(dimensions)
        self.isSuccess = False
        self.frame = None

    def start(self):
        self.isSuccess, self.frame = self.cap.read()

    def set_dimensions(self, dimensions):
        width, height = dimensions
        self.cap.set(3, width)
        self.cap.set(4, height)

    def get_dimensions(self):
        return int(self.cap.get(3)), int(self.cap.get(4))

    def cleanup(self):
        self.cap.release()
        cv.destroyAllWindows()

    def show(self, name="Capture"):
        cv.imshow(name, self.frame)

    def wait_exit(self, key='q'):
        if cv.waitKey(10) & 0xFF == ord(key):
            return True
        return False


if __name__ == "__main__":
    pass
