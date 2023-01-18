# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from .models import Subject, TeacherRegistration, StudentRegistration


## Subjects
#############################################
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'level', 'description', 'teacher', 'school')

class SubjectUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(SubjectUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.level = validated_data['level']
        instance.description = validated_data['description']
        instance.teacher = validated_data['teacher']
        instance.save()
        return instance

    class Meta:
        model = Subject
        fields = ('name', 'level', 'description', 'teacher')

## Teachers
#############################################
class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherRegistration
        fields = ('reg_id', 'teacher', 'school', 'is_active', 'created', 'updated')

class TeachersUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(TeachersSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance

    class Meta:
        model = TeacherRegistration
        fields = ('is_active',)

## Students
#############################################
class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistration
        fields = ('reg_id', 'student', 'school', 'level', 'academic_year', 'is_active', 'created', 'updated')
        extra_kwargs = {'password':{'read_only':True}, 'created':{'read_only':True},
            'updated':{'read_only':True}, 'is_active':{'read_only':True}}

class StudentsUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(StudentsUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.school = validated_data['school']
        instance.level = validated_data['level']
        instance.academic_year = validated_data['academic_year']
        instance.is_active = validated_data['is_active']
        instance.save()
        return instance

    class Meta:
        model = StudentRegistration
        fields = ('school', 'level', 'academic_year', 'is_active')
