from django.db import models
from django.utils import timezone
from django.conf import settings

def resource_file_dir_path(instance, filename):
    return f'user_{instance.user.id}/resources/files/%Y/%m/%d/{instance.id}_{filename}'

def resource_pic_dir_path(instance, filename):
    return f'user_{instance.user.id}/resources/image/%Y/%m/%d/{instance.id}_{filename}'

class Resource(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    tags = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to=resource_pic_dir_path, blank=True, null=True)
    _file = models.FileField(upload_to=resource_file_dir_path, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, to_field='id', on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)

    def natural_key(self):
        return {"id": self.id, "name": self.name, "price": self.price, "tags":self.tags, "description": self.description,
            "is_active": self.is_active, "image": self.image, "_file": self._file, "created_by": self.created_by
        }
