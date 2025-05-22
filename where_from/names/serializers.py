from django.contrib.auth.models import User
from rest_framework import serializers


class NameResponseSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
    countries = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))


class PopularNameSerializer(serializers.Serializer):
    name = serializers.CharField()
    count = serializers.IntegerField()
    probability = serializers.FloatField()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
