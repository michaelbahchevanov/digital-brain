import logging
import multiprocessing as mp
from multiprocessing import Process, Queue
import sys
import gc

import cv2
from detectron2.data import MetadataCatalog
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer
import torch
# Disabling CUDA as it runs out of memory
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '2, 3'
gc.collect()
torch.cuda.empty_cache()

setup_logger()

# Setup logging
logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(asctime)s - %(message)s"
)

# Log number of processors
logging.info(f"Number of processors: {mp.cpu_count()} ")

# Look for an available GPU
gpu = torch.cuda.is_available()
logging.info(f"GPU available - {gpu}")

# Setup config
cfg = get_cfg()
cfg.merge_from_file(
    model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
)
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
    "COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
)
if not gpu:
    cfg.MODEL.DEVICE = "cpu"

predictor = DefaultPredictor(cfg)


def video_capture():
    """
    Initialize video capture with added multiprocessing
    """

    # Default video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Cannot open camera")
        exit()

    input_q = Queue()
    output_q = Queue()
    process = Process(target=object_detection, args=(input_q, output_q))
    process.start()
    processed_frame = None

    # Initialize capture windows
    cv2.namedWindow("main")
    cv2.namedWindow("object")

    while True:
        ret, frame = cap.read()

        # If a frame cannot be read ret is False
        if not ret:
            logging.error("Cannot receive frame. Exiting...")
            break

        if input_q.empty():
            input_q.put(frame)

        concat_frame = frame
        if not output_q.empty():
            processed_frame = output_q.get()
            cv2.imshow("object", processed_frame)

        cv2.imshow("main", frame)

        if cv2.waitKey(1) == ord('q'):
            input_q.close()
            output_q.close()
            input_q.join_thread()
            output_q.join_thread()
            process.terminate()
            break

    # Release capture if everything is successful
    cap.release()
    cv2.destroyAllWindows()


def object_detection(input_q, output_q):
    while True:
        if input_q.empty():
            continue

        frame = input_q.get()

        outputs = predictor(frame)
        logging.debug(outputs["instances"].pred_classes)
        logging.debug(outputs["instances"].pred_boxes)

        v = Visualizer(
            frame[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0])
        )
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        output_q.put(out.get_image()[:, :, ::-1])


def main():
    torch.multiprocessing.set_start_method('spawn')
    video_capture()


if __name__ == '__main__':
    main()
