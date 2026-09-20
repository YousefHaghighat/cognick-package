from typing import Any

from rest_framework import serializers
from .objects import CognitiveParameter


class CognitiveParameterSerializer(serializers.Serializer):
    """
    Dynamically serializes a CognitiveParameter payload.
    """

    id = serializers.IntegerField(read_only=True)
    child_details = serializers.ListField(
        child=serializers.DictField(),
        read_only=True,
    )
    name_en = serializers.CharField(read_only=True)
    name_fa = serializers.CharField(read_only=True)
    name_ar = serializers.CharField(read_only=True)
    icon = serializers.CharField(
        allow_null=True,
        read_only=True,
    )
    description_en = serializers.CharField(read_only=True)
    description_fa = serializers.CharField(read_only=True)
    description_ar = serializers.CharField(read_only=True)
    parent = serializers.IntegerField(
        allow_null=True,
        read_only=True
    )

    def to_representation(
        self,
        instance: CognitiveParameter,
    ) -> dict[str, Any]:
        if isinstance(instance, CognitiveParameter):
            return instance.payload.copy()

        if isinstance(instance, dict):
            return instance.copy()

        return super().to_representation(instance)