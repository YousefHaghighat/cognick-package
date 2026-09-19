from typing import Any

import requests
from django.conf import settings

from .exceptions import (
    CognitiveConnectionException,
    CognitiveNotFoundException,
    CognitiveResponseException
)
from .objects import CognitiveParameter


class CognitiveClient:
    """
    Client for communicating with the cognitive service.
    """

    def __init__(
        self,
        timeout: int | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.url = self._get_url()
        self.timeout = timeout or getattr(
            settings,
            "COGNICK_COGNITIVE_TIMEOUT",
            10,
        )
        self.headers = headers or {}

    @staticmethod
    def _get_url() -> str:
        url = getattr(
            settings,
            "COGNICK_COGNITIVE_URL",
            None,
        )

        if not url:
            raise ValueError(
                "COGNICK_COGNITIVE_BASE_URL must be configured "
                "in Django settings."
            )

        return url.rstrip("/")

    def get_parameter(
        self
    ) -> CognitiveParameter:
        url = (
            f"{self.url}/"
        )

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise CognitiveConnectionException(
                f"Could not connect to cognitive service: {exc}"
            ) from exc

        if response.status_code == 404:
            raise CognitiveNotFoundException(
                f"Cognitive parameter was not found."
            )

        if not response.ok:
            raise CognitiveResponseException(
                f"Cognitive service returned status "
                f"{response.status_code}."
            )

        try:
            data: dict[str, Any] = response.json()
        except ValueError as exc:
            raise CognitiveResponseException(
                "Cognitive service returned invalid JSON."
            ) from exc

        return CognitiveParameter(data)
