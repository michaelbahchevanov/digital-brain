import cv2 as cv


class Capture():
    """A layer of abstraction on top of OpenCV's camera I/O"""
    def __init__(self, src=None, dimensions=(640, 480)):

        if src:
            self.cap = cv.VideoCapture(src)
        self.cap = cv.VideoCapture(0)
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
        return self.cap.get(3), self.cap.get(4)

    def cleanup(self):
        self.cap.release()
        cv.destroyAllWindows()

    def show(self, name="Capture: "):
        cv.imshow(name, self.frame)

    def wait_exit(self, keybind='q'):
        if cv.waitKey(10) & 0xFF == ord('q'):
            return True
        return False


if __name__ == "__main__":
    pass
