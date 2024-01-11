"""Module for pygruenbeck_cloud Exceptions."""
from __future__ import annotations

from typing import Any


class BasePyGruenbeckCloudException(Exception):
    """pygruenbeck_cloud Base exception."""

    def __init__(self, name: str, *args: Any) -> None:
        """Init the BasePyGruenbeckCloudException."""
        super().__init__(*args)
        self.name = name


class PyGruenbeckCloudClientConnectionError(BasePyGruenbeckCloudException):
    """pygruenbeck_cloud PyGruenbeckCloudClientConnectionError exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyGruenbeckCloudClientConnectionError."""
        super().__init__("PyGruenbeckCloudClientConnectionError", *args)


class PyGruenbeckCloudInvalidResponseStatus(BasePyGruenbeckCloudException):
    """pygruenbeck_cloud PyGruenbeckCloudInvalidResponseStatus exception."""

    def __init__(self, *args: Any) -> None:
        """Init the PyGruenbeckCloudInvalidResponseStatus."""
        super().__init__("PyGruenbeckCloudInvalidResponseStatus", *args)
