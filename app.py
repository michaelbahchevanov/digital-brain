from digital_brain.computer_vision.model.utils.capture import Capture
import cv2 as cv


capture = Capture()

while True:
    capture.start()

    capture.show()

    if capture.wait_exit():
        break

capture.cleanup()