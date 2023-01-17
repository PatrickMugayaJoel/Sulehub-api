# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from .models import Subject


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
        instance.school = validated_data['school']
        instance.save()
        return instance

    class Meta:
        model = Subject
        fields = ('name', 'level', 'description', 'teacher', 'school')
