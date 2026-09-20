from typing import Any
from django.conf import settings

from caching import RedisCache
from .client import CognitiveClient



def get_all_data(
        cache_timeout,
        timeout
) -> dict[str, dict[str, Any]]:
    """
    Get all cognitive parameters indexed by their ID.

    The complete list is cached so individual cognitive parameter
    lookups do not require separate API requests.
    """
    all_cache_key = "cognick:cognitive:all"

    cache = RedisCache()
    cached_data = cache.get_data(all_cache_key)

    if cached_data is not None:
        return cached_data

    client = CognitiveClient(
        timeout=timeout,
    )

    response = client.get_parameter()

    data = response.payload

    if isinstance(data, dict):
        parameters = data.get("results", data.get("data", []))
    else:
        parameters = data

    if not isinstance(parameters, list):
        raise ValueError(
            "Cognitive API returned an invalid response format."
        )

    cognitive_data = {
        str(item["id"]): item
        for item in parameters
        if isinstance(item, dict) and item.get("id") is not None
    }

    cache_timeout = (
        cache_timeout
        if cache_timeout is not None
        else getattr(
            settings,
            "COGNICK_COGNITIVE_CACHE_TIMEOUT",
            3600,
        )
    )

    cache.set_data(
        all_cache_key,
        cognitive_data,
        timeout=cache_timeout,
    )

    return cognitive_data
