"""Custom exception hierarchy for the API testing framework.

All exceptions raised by adapters inherit from ``APIClientError``, allowing
callers to catch the entire hierarchy with a single ``except`` clause while
still being able to catch specific subtypes when needed.
"""


class APIClientError(Exception):
    """Base exception for all API client errors.

    Raised by ``BaseAPIClient`` and its subclasses when an API call fails.
    Catch this class to handle any framework-raised error in a broad clause.
    """


class APIAuthError(APIClientError):
    """Raised when the server returns 401 Unauthorized or 403 Forbidden.

    Indicates a missing, expired, or insufficiently privileged credential.
    """


class APINotFoundError(APIClientError):
    """Raised when the server returns 404 Not Found.

    Indicates the requested resource does not exist at the given path.
    """


class APIValidationError(APIClientError):
    """Raised when a 4xx response indicates a request validation failure.

    Typically maps to 400 Bad Request or 422 Unprocessable Entity when the
    response body describes a schema or constraint violation.
    """


class APITransportError(APIClientError):
    """Raised on connection errors, timeouts, or other transport-level failures.

    Wraps exceptions that occur before any response is received from the
    server — e.g. ``httpx.ConnectError`` or ``httpx.TimeoutException``.
    """
