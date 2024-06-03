import base64
from io import BytesIO

from PIL import Image

from washer_server.services.connection_manager import connection_manager
from washer_server.services.ml_model import find_person_and_draw_box


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

        person_has_spotted = find_person_and_draw_box(image)

        image_base64 = _format_image_to_base64(image)
        await connection_manager.send_image_to_client(image_base64)
        if person_has_spotted:
            await connection_manager.send_message_to_cleaner("spotted")
