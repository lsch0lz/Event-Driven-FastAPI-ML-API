import base64
from io import BytesIO

from PIL import Image


img = Image.open("/Users/lukasscholz/Downloads/lukas.jpg")
buffered = BytesIO()
img.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue())
print(img_str)
