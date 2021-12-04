# Courtesy of https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
import cv2
import collections
import struct
import six
import subprocess as sp
import json
import numpy
import time
from matplotlib import colors
from threading import Thread


class HLSVideoStream:
    def __init__(self, src):
        # initialize the video camera stream and read the first frame
        # from the stream

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

        FFMPEG_BIN = "ffmpeg"

        metadata = {}

        while "streams" not in metadata.keys():
            print('ERROR: Could not access stream. Trying again.')

            info = sp.Popen(["ffprobe",
                             "-v", "quiet",
                             "-print_format", "json",
                             "-show_format",
                             "-show_streams", src],
                            stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            out, err = info.communicate(
                b"ffprobe -v quiet -print_format json -show_format -show_streams http://52.91.28.88:8080/hls/live.m3u8")

            metadata = json.loads(out.decode('utf-8'))
            time.sleep(5)

        print('SUCCESS: Retrieved stream metadata.')

        self.WIDTH = metadata["streams"][0]["width"]
        self.HEIGHT = metadata["streams"][0]["height"]

        self.pipe = sp.Popen([FFMPEG_BIN, "-i", src,
                              "-loglevel", "quiet",  # no text output
                              "-an",  # disable audio
                              "-f", "image2pipe",
                              "-pix_fmt", "bgr24",
                              "-vcodec", "rawvideo", "-"],
                             stdin=sp.PIPE, stdout=sp.PIPE)
        print('WIDTH: ', self.WIDTH)

        raw_image = self.pipe.stdout.read(self.WIDTH * self.HEIGHT * 3)  # read 432*240*3 bytes (= 1 frame)
        self.frame = numpy.fromstring(raw_image, dtype='uint8').reshape((self.HEIGHT, self.WIDTH, 3))
        self.grabbed = self.frame is not None

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        # if the thread indicator variable is set, stop the thread

        while True:
            if self.stopped:
                return

            raw_image = self.pipe.stdout.read(self.WIDTH * self.HEIGHT * 3)  # read 432*240*3 bytes (= 1 frame)
            self.frame = numpy.fromstring(raw_image, dtype='uint8').reshape((self.HEIGHT, self.WIDTH, 3))
            self.grabbed = self.frame is not None

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class WebcamVideoStream:
    def __init__(self, src, width, height):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def standard_colors():
    return [
        'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
        'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
        'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
        'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
        'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
        'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
        'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
        'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
        'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
        'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
        'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
        'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
        'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
        'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
        'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
        'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
        'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
        'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
        'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
        'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
        'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
        'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
        'WhiteSmoke', 'Yellow', 'YellowGreen'
    ]


def color_name_to_rgb():
    colors_rgb = []
    for key, value in colors.cnames.items():
        colors_rgb.append((key, struct.unpack('BBB', bytes.fromhex(value.replace('#', '')))))
    return dict(colors_rgb)


def draw_boxes_and_labels(
        boxes,
        classes,
        scores,
        category_index,
        instance_masks=None,
        keypoints=None,
        max_boxes_to_draw=20,
        min_score_thresh=.5,
        agnostic_mode=False):
    """Returns boxes coordinates, class names and colors
    Args:
    boxes: a numpy array of shape [N, 4]
    classes: a numpy array of shape [N]
    scores: a numpy array of shape [N] or None.  If scores=None, then
    this function assumes that the boxes to be plotted are groundtruth
    boxes and plot all boxes as black with no classes or scores.
    category_index: a dict containing category dictionaries (each holding
    category index `id` and category name `name`) keyed by category indices.
    instance_masks: a numpy array of shape [N, image_height, image_width], can
    be None
    keypoints: a numpy array of shape [N, num_keypoints, 2], can
    be None
    max_boxes_to_draw: maximum number of boxes to visualize.  If None, draw
    all boxes.
    min_score_thresh: minimum score threshold for a box to be visualized
    agnostic_mode: boolean (default: False) controlling whether to evaluate in
    class-agnostic mode or not.  This mode will display scores but ignore
    classes.
    """
    # Create a display string (and color) for every box location, group any boxes
    # that correspond to the same location.
    box_to_display_str_map = collections.defaultdict(list)
    box_to_color_map = collections.defaultdict(str)
    box_to_instance_masks_map = {}
    box_to_keypoints_map = collections.defaultdict(list)
    if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
    for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
            box = tuple(boxes[i].tolist())
            if instance_masks is not None:
                box_to_instance_masks_map[box] = instance_masks[i]
            if keypoints is not None:
                box_to_keypoints_map[box].extend(keypoints[i])
            if scores is None:
                box_to_color_map[box] = 'black'
            else:
                if not agnostic_mode:
                    if classes[i] in category_index.keys():
                        class_name = category_index[classes[i]]['name']
                    else:
                        class_name = 'N/A'
                    display_str = '{}: {}%'.format(
                        class_name,
                        int(100 * scores[i]))
                else:
                    display_str = 'score: {}%'.format(int(100 * scores[i]))
                box_to_display_str_map[box].append(display_str)
                if agnostic_mode:
                    box_to_color_map[box] = 'DarkOrange'
                else:
                    box_to_color_map[box] = standard_colors()[
                        classes[i] % len(standard_colors())]

    # Store all the coordinates of the boxes, class names and colors
    color_rgb = color_name_to_rgb()
    rect_points = []
    class_names = []
    class_colors = []
    for box, color in six.iteritems(box_to_color_map):
        ymin, xmin, ymax, xmax = box
        rect_points.append(dict(ymin=ymin, xmin=xmin, ymax=ymax, xmax=xmax))
        class_names.append(box_to_display_str_map[box])
        class_colors.append(color_rgb[color.lower()])
    return rect_points, class_names, class_colors