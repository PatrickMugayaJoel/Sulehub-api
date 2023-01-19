from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'school', 'tags', 'description', 'expires_on', 'created_on', 'created_by')

class EventUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(EventUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.school = validated_data['school']
        instance.tags = validated_data['tags']
        instance.description = validated_data['description']
        instance.expires_on = validated_data['expires_on']
        instance.save()
        return instance

    class Meta:
        model = Event
        fields = ('name', 'school', 'description', 'tags', 'expires_on')
