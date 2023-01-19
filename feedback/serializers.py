from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'title', 'category', 'description', 'resource', 'created_on', 'created_by')

class FeedbackSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(FeedbackSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.category = validated_data['category']
        instance.description = validated_data['description']
        instance.save()
        return instance

    class Meta:
        model = Feedback
        fields = ('title', 'category', 'description')
