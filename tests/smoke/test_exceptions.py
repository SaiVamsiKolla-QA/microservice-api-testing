"""Smoke tests for the adapters.exceptions exception hierarchy.

Verifies that all exception classes exist, inherit correctly, and behave
as expected when raised and caught. No I/O, no mocks — pure type checks.
"""

import pytest

from adapters.exceptions import (
    APIAuthError,
    APIClientError,
    APINotFoundError,
    APITransportError,
    APIValidationError,
)

# -- Base class ----------------------------------------------------------------


@pytest.mark.smoke
def test_api_client_error_subclasses_exception() -> None:
    """APIClientError is a subclass of Python's built-in Exception."""
    # Assert — issubclass is a structural fact; no arrange or act needed
    assert issubclass(APIClientError, Exception)


@pytest.mark.smoke
def test_api_client_error_str_includes_message() -> None:
    """str() of an APIClientError instance includes the message passed to the constructor."""
    # Arrange
    message = "something went wrong"
    # Act
    error = APIClientError(message)
    # Assert
    assert message in str(error)


# -- Subclass identity ---------------------------------------------------------


@pytest.mark.smoke
@pytest.mark.parametrize(
    "exc_class",
    [APIAuthError, APINotFoundError, APIValidationError, APITransportError],
    ids=["APIAuthError", "APINotFoundError", "APIValidationError", "APITransportError"],
)
def test_all_subclasses_are_api_client_error(exc_class: type[APIClientError]) -> None:
    """Each of the four leaf exception classes is a subclass of APIClientError."""
    # Assert — structural fact; no arrange or act needed
    assert issubclass(exc_class, APIClientError)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "exc_class",
    [APIClientError, APIAuthError, APINotFoundError, APIValidationError, APITransportError],
    ids=[
        "APIClientError",
        "APIAuthError",
        "APINotFoundError",
        "APIValidationError",
        "APITransportError",
    ],
)
def test_all_exceptions_subclass_exception(exc_class: type[APIClientError]) -> None:
    """All five exception classes inherit from Python's built-in Exception."""
    # Assert — structural fact; no arrange or act needed
    assert issubclass(exc_class, Exception)


@pytest.mark.smoke
@pytest.mark.parametrize(
    "exc_class",
    [APIClientError, APIAuthError, APINotFoundError, APIValidationError, APITransportError],
    ids=[
        "APIClientError",
        "APIAuthError",
        "APINotFoundError",
        "APIValidationError",
        "APITransportError",
    ],
)
def test_all_exceptions_instantiate_and_str_includes_message(
    exc_class: type[APIClientError],
) -> None:
    """Each exception class instantiates cleanly and str() includes the passed message."""
    # Arrange
    message = "test message"
    # Act
    error = exc_class(message)
    # Assert
    assert message in str(error)


# -- Polymorphism and independence ---------------------------------------------


@pytest.mark.smoke
def test_subclass_caught_as_base_class() -> None:
    """A leaf exception raised can be caught as APIClientError (polymorphic catch)."""
    # Arrange / Act / Assert
    with pytest.raises(APIClientError):
        raise APINotFoundError("resource not found")


@pytest.mark.smoke
def test_distinct_subclasses_not_interchangeable() -> None:
    """Catching APINotFoundError does not catch APIAuthError — leaf classes are independent."""
    # Arrange
    not_found_caught = False
    auth_caught = False
    # Act
    try:
        raise APIAuthError("unauthorized")
    except APINotFoundError:
        not_found_caught = True
    except APIAuthError:
        auth_caught = True
    # Assert
    assert not not_found_caught, "APINotFoundError incorrectly caught APIAuthError"
    assert auth_caught, "APIAuthError was not caught by its own handler"
