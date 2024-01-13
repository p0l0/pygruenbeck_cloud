"""Models for pygruenbeck_cloud."""
from __future__ import annotations

from dataclasses import dataclass, field
import datetime

# from datetime import datetime, timedelta, timezone
import keyword
import re

from pygruenbeck_cloud.const import UPDATE_INTERVAL


@dataclass
class GruenbeckAuthToken:
    """Object holding auth tokens for gruenbeck cloud."""

    access_token: str
    refresh_token: str
    not_before: datetime.datetime
    expires_on: datetime.datetime
    expires_in: int
    tenant: str

    def is_expired(self) -> bool:
        """Return if token is expired or not."""
        return not (
            (datetime.datetime.now() - datetime.timedelta(seconds=UPDATE_INTERVAL))
            <= self.expires_on
        )


@dataclass
class DeviceError:
    """Object holding Device Error Information."""

    is_resolved: bool
    message: str
    type: str
    date: datetime.datetime
    _date: datetime.datetime | None = field(init=False, repr=False, default=None)

    @staticmethod
    def from_dict(data: dict) -> DeviceError:
        """Prepare values from dict."""
        new_data = {}
        pattern = re.compile(r"(?<!^)(?=[A-Z])")  # camelCase to snake_case
        for key, value in data.items():
            var_name = pattern.sub("_", key).lower()
            if keyword.iskeyword(var_name):
                var_name = f"{var_name}_"
            new_data[var_name] = value

        return DeviceError(**new_data)

    @property  # type: ignore[no-redef]
    def date(self) -> datetime.datetime | None:
        """Return date value."""
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        """Parse and set date as datetime from string value."""
        datetime_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        # Object seems to be UTC, so we need to set correct timezeon
        self._date = datetime_obj.replace(tzinfo=datetime.UTC)


@dataclass
class DailyUsageEntry:
    """Object holding daily usage data."""

    value: int
    date: datetime.date
    _date: datetime.date | None = field(init=False, repr=False, default=None)

    @property  # type: ignore[no-redef]
    def date(self) -> datetime.date | None:
        """Return date value."""
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        """Parse and set date as date from string value."""
        self._date = datetime.datetime.strptime(value, "%Y-%m-%d")


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
    next_regeneration: datetime.datetime
    time_zone: datetime.tzinfo
    startup: datetime.date
    errors: list[DeviceError]
    salt: list[DailyUsageEntry]
    water: list[DailyUsageEntry]
    hardware_version: str | None = None
    last_service: str | None = None
    mode: int | None = None
    _next_regeneration: datetime.datetime | None = field(
        init=False, repr=False, default=None
    )
    nominal_flow: float | None = None
    raw_water: float | None = None
    soft_water: float | None = None
    software_version: str | None = None
    _errors: list[DeviceError] | None = field(init=False, repr=False, default=None)
    _salt: list[DailyUsageEntry] | None = field(init=False, repr=False, default=None)
    _time_zone: datetime.tzinfo | None = field(init=False, repr=False, default=None)
    _water: list[DailyUsageEntry] | None = field(init=False, repr=False, default=None)
    unit: int | None = None
    _startup: datetime.date | None = field(init=False, repr=False, default=None)

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

        print(new_data)
        return Device(**new_data)

    @property  # type: ignore[no-redef]
    def next_regeneration(self) -> datetime.datetime | None:
        """Return next regeneration value."""
        return self._next_regeneration

    @next_regeneration.setter
    def next_regeneration(self, value: str | property) -> None:
        """Parse and set next regeneration as datetime from string value."""
        if isinstance(value, property):
            print("next_regeneration: Initial value not specified")
            return
        # Provided date is UTC, but format has no timezone information
        datetime_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        if self.time_zone:
            datetime_obj = datetime_obj.replace(tzinfo=self.time_zone)
        self._next_regeneration = datetime_obj

    @property  # type: ignore[no-redef]
    def startup(self) -> datetime.date | None:
        """Return startup value."""
        return self._startup

    @startup.setter
    def startup(self, value: str | property) -> None:
        """Parse and set startup as date from string value."""
        if isinstance(value, property):
            print("startup: Initial value not specified")
            return
        self._startup = datetime.datetime.strptime(value, "%Y-%m-%d")

    @property  # type: ignore[no-redef]
    def time_zone(self) -> datetime.tzinfo | None:
        """Return time zone value."""
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value: str | property) -> None:
        """Parse and set time zone as tzinfo from string value."""
        if isinstance(value, property):
            print("timezone: Initial value not specified")
            return
        tzinfo = datetime.datetime.strptime(value, "%z").tzinfo
        if self._next_regeneration:
            self._next_regeneration.replace(tzinfo=tzinfo)

        self._time_zone = tzinfo

    @property  # type: ignore[no-redef]
    def errors(self) -> list[DeviceError] | None:
        """Return list of errors."""
        return self._errors

    @errors.setter
    def errors(self, value: list[dict] | property) -> None:
        """Set list of errors as DeviceError object."""
        if isinstance(value, property):
            return

        result: list[DeviceError] = []
        for entry in value:
            result.append(DeviceError.from_dict(entry))

        self._errors = result

    @property  # type: ignore[no-redef]
    def salt(self) -> list[DailyUsageEntry] | None:
        """Return list of salt usage."""
        return self._salt

    @salt.setter
    def salt(self, value: list[dict] | property) -> None:
        """Set list of salt usage as DailyUsageEntry object."""
        if isinstance(value, property):
            return

        result: list[DailyUsageEntry] = []
        for entry in value:
            result.append(DailyUsageEntry(**entry))

        self._salt = result

    @property  # type: ignore[no-redef]
    def water(self) -> list[DailyUsageEntry] | None:
        """Return list of water usage."""
        return self._water

    @water.setter
    def water(self, value: list[dict] | property) -> None:
        """Set list of water usage as DailyUsageEntry object."""
        if isinstance(value, property):
            return

        result: list[DailyUsageEntry] = []
        for entry in value:
            result.append(DailyUsageEntry(**entry))

        self._water = result
