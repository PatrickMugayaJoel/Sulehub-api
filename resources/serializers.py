from rest_framework import serializers
from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'price', 'tags', 'is_active', 'description', 'image', '_file', 'created_on', 'created_by')
        # TODO: created_by: should be auto added and a read_only
        extra_kwargs = {'_file':{'read_only':True},'image':{'read_only':True},'created_on':{'read_only':True},}

class ResourceUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(ResourceUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.price = validated_data['price']
        instance.tags = validated_data['tags']
        instance.description = validated_data['description']
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance

    class Meta:
        model = Resource
        fields = ('name', 'price', 'is_active', 'description', 'tags')
