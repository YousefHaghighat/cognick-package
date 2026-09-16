from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.db import models

from .client import CognitiveClient
from .objects import CognitiveParameter


class CognitiveField(models.CharField):
    """
    Stores a cognitive parameter ID in the database.

    The field accepts either a cognitive parameter ID or a
    CognitiveParameter instance when saving.
    """

    def __init__(
        self,
        *args,
        cache_timeout: int | None = None,
        timeout: int | None = None,
        **kwargs,
    ):
        kwargs.setdefault("max_length", 36)

        self.cache_timeout = cache_timeout
        self.timeout = timeout

        super().__init__(*args, **kwargs)

    def get_prep_value(
        self,
        value: CognitiveParameter | str | int | None,
    ) -> str | None:
        if value is None:
            return None

        if isinstance(value, CognitiveParameter):
            return str(value.id)

        if isinstance(value, (str, int)):
            return str(value)

        raise ValueError(
            "CognitiveField only accepts a cognitive parameter ID "
            "or a CognitiveParameter instance."
        )

    def from_db_value(
        self,
        value: Any,
        expression,
        connection,
    ) -> str | None:
        if value is None:
            return None

        return str(value)

    def get_full_data(
        self,
        value: str | int | CognitiveParameter | None,
    ) -> CognitiveParameter | None:
        """
        Resolve a cognitive parameter ID to a CognitiveParameter object.
        """

        if value is None:
            return None

        if isinstance(value, CognitiveParameter):
            return value

        value = str(value)

        cache_timeout = (
            self.cache_timeout
            if self.cache_timeout is not None
            else getattr(
                settings,
                "COGNICK_COGNITIVE_CACHE_TIMEOUT",
                3600,
            )
        )

        cache_key = f"cognick:cognitive:{value}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return CognitiveParameter(cached_data)

        client = CognitiveClient(
            timeout=self.timeout,
        )

        cognitive = client.get_parameter(value)

        cache.set(
            cache_key,
            cognitive.payload,
            timeout=cache_timeout,
        )

        return cognitive
