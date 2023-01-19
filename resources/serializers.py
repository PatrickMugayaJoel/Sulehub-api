from rest_framework import serializers
from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'price', 'tags', 'description', 'image', 'file', 'created_on', 'created_by')

class ResourceUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(ResourceUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.tags = validated_data['tags']
        instance.description = validated_data['description']
        instance.image = validated_data['image']
        instance.save()
        return instance

    class Meta:
        model = Resource
        fields = ('name', 'price', 'description', 'tags', 'image')
