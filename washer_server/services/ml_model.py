from PIL import Image, ImageDraw
from ultralytics import YOLO
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from os import path


class YoloModel:
    _instance: Optional["YoloModel"] = None

    def __new__(cls) -> "YoloModel":
        if cls._instance is None:
            cls._instance = super(YoloModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.model = YOLO("yolov8n.pt")


def find_person(frame: Image) -> dict:
    # https://kamalrajjairam.medium.com/image-detection-and-analysis-using-yolo5-db1b00b1a13c
    model = YoloModel().model
    results = model(frame, verbose=True)
    persons_count = 0
    persons_boxes = []
    if len(results) == 0:
        return {"persons_num": persons_count, "persons_boxes": persons_boxes}
    else:
        for res_i in results[0]:
            class_num = int(res_i.boxes.cls)
            if class_num == 0:
                boxes = res_i.boxes.xyxy
                # boxes_coord = [int(round(el_i, 0)) for el_i in boxes.tolist()[0]]
                boxes_coord = boxes.tolist()[0]
                draw = ImageDraw.Draw(frame)
                draw.rectangle(boxes_coord, width=1, outline="#0000ff")
                persons_boxes.append([int(round(el_i, 0)) for el_i in boxes_coord])
                persons_count += 1

    return {"persons_num": persons_count, "persons_boxes": persons_boxes}
