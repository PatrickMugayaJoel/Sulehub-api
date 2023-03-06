from rest_framework import serializers
from .models import StudyGroup, GroupRegistration


class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ('id', 'name', 'tags', 'description', 'level', 'is_active', 'created_on', 'created_by')
        extra_kwargs = {'created_on':{'read_only':True},}

class StudyGroupUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(StudyGroupUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.tags = validated_data['tags']
        instance.is_active = validated_data['is_active']
        instance.description = validated_data['description']
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance

    class Meta:
        model = StudyGroup
        fields = ('name', 'description', 'tags', 'is_active',)

## Group Registrations
#############################################
class GroupRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRegistration
        fields = ('member_id', 'student', 'study_group', 'is_active', 'created')
        extra_kwargs = {'created':{'read_only':True},}

class GroupRegistrationUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(GroupRegistrationUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance

    class Meta:
        model = GroupRegistration
        fields = ('is_active',)
