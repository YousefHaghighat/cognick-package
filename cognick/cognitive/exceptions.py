
class CognitiveException(Exception):
    """Base exception for cognitive package."""


class CognitiveNotFoundException(CognitiveException):
    """Raised when a cognitive parameter cannot be found."""


class CognitiveConnectionException(CognitiveException):
    """Raised when the cognitive service cannot be reached."""


class CognitiveResponseException(CognitiveException):
    """Raised when the cognitive service returns an invalid response."""
