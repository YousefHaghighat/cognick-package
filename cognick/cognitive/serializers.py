from rest_framework import serializers

from .objects import CognitiveParameter


class CognitiveParameterSerializer(serializers.Serializer):
    id = serializers.CharField()
    name_en = serializers.CharField()
    name_fa = serializers.CharField()
    name_ar = serializers.CharField()
    icon = serializers.CharField(
        allow_null=True,
        required=False,
    )
    description_en = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    description_fa = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    description_ar = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )
    parent = serializers.CharField(
        allow_null=True,
        required=False,
    )
