from rest_framework import serializers
from .models import RefBook, Version, Element


class RefbookSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Refbook.
    """
    class Meta:
        model = RefBook
        fields = ['id', 'code', 'name']


class VersionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Version.
    """
    class Meta:
        model = Version
        fields = ['id', 'version', 'start_date']


class ElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Element.
    """
    class Meta:
        model = Element
        fields = ['code', 'value']
