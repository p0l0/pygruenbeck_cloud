"""Module for pygruenbeck_cloud Exceptions."""

from __future__ import annotations


class PyGruenbeckCloudError(Exception):
    """Generic PyGruenbeck exception."""


class PyGruenbeckCloudResponseError(Exception):
    """PyGruenbeck API Response Error exception."""


class PyGruenbeckCloudResponseStatusError(Exception):
    """PyGruenbeck API Response status Error exception."""


class PyGruenbeckCloudUpdateParameterError(Exception):
    """PyGruenbeck API Response Error on Parameter Update exception."""


class PyGruenbeckCloudConnectionError(Exception):
    """PyGruenbeck API Connection Error exception."""


class PyGruenbeckCloudConnectionClosedError(Exception):
    """PyGruenbeck API Connection Closed exception."""


class PyGruenbeckCloudMissingAuthTokenError(Exception):
    """PyGruenbeck Missing Auth Token exception."""
