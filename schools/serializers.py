# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('school_id', 'name', 'phone', 'email', 'website', 'country', 'address', 'Bio', 'school_id', 'manager')

class SchoolUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(SchoolUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.phone = validated_data['phone']
        instance.email = validated_data['email']
        instance.website = validated_data['website']
        instance.country = validated_data['country']
        instance.address = validated_data['address']
        instance.Bio = validated_data['Bio']
        instance.manager = validated_data['manager']
        instance.save()
        return instance

    class Meta:
        model = School
        fields = ('school_id', 'name', 'phone', 'email', 'website', 'country', 'address', 'Bio', 'school_id', 'manager')
