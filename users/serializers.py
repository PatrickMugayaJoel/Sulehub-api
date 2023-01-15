#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from rest_framework import serializers
from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    DP = serializers.CharField(read_only=True)

    def validate(self, data, *args, **kwargs):
       return super(UserCreateSerializer, self).validate(data, *args, **kwargs)

    @transaction.atomic()
    def create(self, validated_data):
        # Register new users
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


    class Meta:
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name', 'last_name', 'role', 'DoB', 'contact', 'residence', 'gender', 'country', 'DP')
        extra_kwargs = {'password':{'write_only':True}}

class UserUpdateSerializer(serializers.ModelSerializer):

    def validate(self, data, *args, **kwargs):
       return super(UserUpdateSerializer, self).validate(data, *args, **kwargs)

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.role = validated_data['role']
        instance.DoB = validated_data['DoB']
        instance.contact = validated_data['contact']
        instance.residence = validated_data['residence']
        instance.gender = validated_data['gender']
        instance.country = validated_data['country']
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'DoB', 'contact', 'residence', 'gender', 'country')

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role', 'DoB', 'contact', 'residence', 'gender', 'country', 'DP')

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
