from rest_framework import serializers
from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('id', 'price', 'resource', 'reference_text', 'created_on', 'created_by')
        extra_kwargs = {'created_on':{'read_only':True},} # TODO: created_by: should be auto added and a read_only

class SaleUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(SaleUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.reference_text = validated_data['reference_text']
        instance.save()
        return instance

    class Meta:
        model = Sale
        fields = ('reference_text',)
