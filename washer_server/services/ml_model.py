from typing import Optional

from PIL import Image, ImageDraw
from ultralytics import YOLO


class YoloModel:
    _instance: Optional["YoloModel"] = None

    def __new__(cls) -> "YoloModel":
        if cls._instance is None:
            cls._instance = super(YoloModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.model = YOLO("yolov8n.pt")


def draw_rectangle(image: Image, cords: tuple[float, float, float, float]) -> None:
    draw = ImageDraw.Draw(image)
    draw.rectangle(cords, width=1, outline="#0000ff")


def find_person_and_draw_box(image: Image) -> bool:
    model: YOLO = YoloModel().model
    results = model(image, verbose=True)
    if len(results) == 0:
        return False
    else:
        for res_i in results[0]:
            class_num = int(res_i.boxes.cls)
            if class_num == 0:
                boxes = res_i.boxes.xyxy
                draw_rectangle(image, boxes.tolist()[0])
    return True
