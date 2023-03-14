
## for expiring urls, see: https://github.com/yunojuno/django-request-token

import os
import magic
from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from custom_logger import CustomLogger

custom_logger = CustomLogger()

def upload(request, path, _type):
    file_obj = request.FILES['file']
    content_type = magic.from_buffer(file_obj.read(), mime=True)
    accepted_types = {
        "image": ["image/png", "image/tiff", "image/jpeg", "image/gif", "image/webp"],
        "document": [
            "text/richtext", "text/plain", "application/vnd.ms-excel", "application/msword"
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/epub+zip", "application/pdf"
        ]
    }

    if not content_type in accepted_types[_type]:
        return {"status": False, "message": "Uploaded file type is not allowed!"}
    if file_obj.size > 10*1000*1000: # 10mbs
        return {"status": False, "message": "Maximum allowed file size is 10mbs!"}

    try:
        _file = os.path.join(settings.STATICFILES_DIRS[0], path)
        path = default_storage.save(_file, content=file_obj)
        ## Looping over UploadedFile.chunks() instead of using read() ensures that large files don’t overwhelm your system’s memory.
        # with open(_file, 'wb+') as destination:
        #   for chunk in file_obj.chunks():
        #     destination.write(chunk)
        return {"status": True, "message": "File Uploaded successfully"}
    except Exception as e:
        print("ERROR: ",e)
        custom_logger.log_error("upload", str(e), request, "File_Upload")
        return {"status": False, "message": "File Upload error!"}
