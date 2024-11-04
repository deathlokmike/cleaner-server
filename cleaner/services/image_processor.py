import base64
from io import BytesIO

from PIL import Image

from cleaner.services.connection_manager import (CleanerStatus,
                                                 connection_manager)
from cleaner.services.ml_model import YoloModel


def _format_image_to_base64(image: Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{img_str}"


class ImageProcessor:
    @classmethod
    async def find_person_and_notify_all(cls, image_raw_bytes: bytes):
        image = Image.frombuffer('RGB', (160, 120), image_raw_bytes, 'raw', 'RGB;16')
        image = image.rotate(angle=270, resample=0, expand=True)

        person_boxes = YoloModel().find_person(image)

        if len(person_boxes) > 0:
            await connection_manager.send_message_to_cleaner(CleanerStatus.suspended)
            YoloModel().draw_rectangle(image, person_boxes)
        else:
            await connection_manager.send_message_to_cleaner(CleanerStatus.resumed)

        image_base64 = _format_image_to_base64(image)
        await connection_manager.send_data_to_client(image_base64)
