"""Models for pygruenbeck_cloud."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import keyword
import re

from pygruenbeck_cloud.const import UPDATE_INTERVAL


@dataclass
class GruenbeckAuthToken:
    """Object holding auth tokens for gruenbeck cloud."""

    access_token: str
    refresh_token: str
    not_before: datetime
    expires_on: datetime
    expires_in: int
    tenant: str

    def is_expired(self) -> bool:
        """Return if token is expired or not."""
        return not (
            (datetime.now() - timedelta(seconds=UPDATE_INTERVAL)) <= self.expires_on
        )


@dataclass
class Device:
    """Object holding Device Information."""

    type: int
    has_error: bool
    id: str
    series: str
    serial_number: str
    name: str
    register: bool

    @staticmethod
    def from_dict(data: dict) -> Device:
        """Prepare values from dict."""
        new_data = {}
        pattern = re.compile(r"(?<!^)(?=[A-Z])")  # camelCase to snake_case
        for key, value in data.items():
            var_name = pattern.sub("_", key).lower()
            if keyword.iskeyword(var_name):
                var_name = f"{var_name}_"
            new_data[var_name] = value
            # if hasattr(self, var_name):
            #     setattr(self, var_name, value)

        return Device(**new_data)
