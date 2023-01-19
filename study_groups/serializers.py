from rest_framework import serializers
from .models import StudyGroup, GroupRegistration


class StudyGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ('id', 'name', 'school', 'tags', 'description', 'level', 'is_active', 'created_on', 'created_by')

class StudyGroupUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(StudyGroupUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.school = validated_data['school']
        instance.tags = validated_data['tags']
        instance.is_active = validated_data['is_active']
        instance.description = validated_data['description']
        instance.expires_on = validated_data['expires_on']
        instance.save()
        return instance

    class Meta:
        model = StudyGroup
        fields = ('name', 'school', 'description', 'tags', 'expires_on')

## Group Registrations
#############################################
class GroupRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupRegistration
        fields = ('member_id', 'student', 'study_group', 'is_active', 'created')

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
