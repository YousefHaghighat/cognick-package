from typing import Any


class CognitiveParameter:
    """
    Represents a cognitive parameter retrieved from the cognitive service.
    """

    def __init__(self, payload: dict[str, Any]):
        self._payload = payload

    def __getattr__(self, name: str) -> Any:
        try:
            return self._payload[name]
        except KeyError as exc:
            raise AttributeError(
                f"{self.__class__.__name__!s} object has no attribute {name!r}"
            ) from exc

    def __getitem__(self, key: str) -> Any:
        return self._payload[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._payload.get(key, default)

    @property
    def payload(self) -> dict[str, Any]:
        return self._payload

    @property
    def id(self) -> str | int | None:
        return self._payload.get("id")

    def __bool__(self) -> bool:
        return bool(self._payload)

    def __repr__(self) -> str:
        return f"<CognitiveParameter(id={self.id})>"
