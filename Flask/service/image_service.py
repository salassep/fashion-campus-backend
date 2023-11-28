import base64
import re
from multiprocessing import Process
from string import ascii_letters
from random import choices
# from util.cloud_storage import get_bucket
from util.firebase_storage import get_bucket

class ImageService:
    def __init__(self):
        self.bucket = get_bucket()

    def get_image(self, filename:str):
        blob = self.bucket.blob(filename)

        if not blob:
            return
           
        image = {
            'blob': blob.download_as_string(),
            'contentType': blob._properties.get("contentType"),
        }

        return image
    
    def async_upload_image(self, image_data: dict):
        blob = self.bucket.blob(image_data["filename"])
        base64_image = base64.b64decode(image_data["base64_image"])
        format_image = image_data["format_image"]
        
        blob.upload_from_string(base64_image, content_type=format_image)
    
    def upload_image(self, file):

        if "base64" not in file:
            return file[7:]

        base64_splitted = file.split('base64')

        format_image = re.findall("(?<=data:)(.*)(?=;)", base64_splitted[0])[0]

        filename = ''.join(choices(ascii_letters, k=10)) + f".{format_image.split('/')[1]}"

        image_data = {
            "filename": filename,
            "base64_image": base64_splitted[1],
            "format_image": format_image
        }
        
        # proc = Process(target=self.async_upload_image, args=(image_data,))
        # proc.start()

        self.async_upload_image(image_data)

        return filename
    
    def delete_image(self, filename:str):
        blob = self.bucket.get_blob(filename)

        if not blob:
            return
        
        blob.delete()
        return True