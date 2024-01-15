"""Module for pygruenbeck_cloud Exceptions."""
from __future__ import annotations


class PyGruenbeckCloudError(Exception):
    """Generic PyGruenbeck exception."""


class PyGruenbeckCloudResponseError(Exception):
    """PyGruenbeck API Response exception."""


class PyGruenbeckCloudResponseStatusError(Exception):
    """PyGruenbeck API Response status exception."""


class PyGruenbeckCloudConnectionError(Exception):
    """PyGruenbeck API Connection Error exception."""


class PyGruenbeckCloudInvalidResponseStatus(Exception):
    """PyGruenbeck API Incorrect response status code exception."""


class PyGruenbeckCloudConnectionClosedError(Exception):
    """PyGruenbeck API Connection Closed exception."""


class PyGruenbeckCloudMissingAuthTokenError(Exception):
    """PyGruenbeck Missing Auth Token exception."""
