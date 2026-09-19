from typing import Any

from rest_framework import serializers
from .objects import CognitiveParameter


class CognitiveParameterSerializer(serializers.Serializer):
    """
    Dynamically serializes a CognitiveParameter payload.
    """

    def to_representation(self, instance: CognitiveParameter) -> dict[str, Any]:
        if isinstance(instance, CognitiveParameter):
            return instance.payload.copy()

        if isinstance(instance, dict):
            return instance.copy()

        return super().to_representation(instance)
