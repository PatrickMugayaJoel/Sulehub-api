import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from custom_logger import CustomLogger


def upload(request, path):
    file_obj = request.FILES['file']

    try:
        _file = os.path.join(settings.STATIC_ROOT, path)
        path = default_storage.save(_file, ContentFile(file_obj.read()))
        return True
    except Exception as e:
        print("ERROR: ",e)
        custom_logger.log_error("upload", str(e), request, "File_Upload")
        return False
