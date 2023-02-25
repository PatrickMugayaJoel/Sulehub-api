from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('id', 'title', 'category', 'description', 'resource', 'created_on', 'created_by')
        extra_kwargs = {'created_on':{'read_only':True},} # TODO: created_by: should be auto added and a read_only

class FeedbackUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(FeedbackUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.category = validated_data['category']
        instance.description = validated_data['description']
        instance.save()
        return instance

    class Meta:
        model = Feedback
        fields = ('title', 'category', 'description')
