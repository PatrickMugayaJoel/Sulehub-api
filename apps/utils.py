from django.core.serializers.json import DjangoJSONEncoder
from apps.users.models import User
from apps.schools.models import School
from apps.school_extras.models import Level

class JsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, User) or isinstance(obj, School) or isinstance(obj, Level):
            return obj.natural_key()
        return super().default(obj)

