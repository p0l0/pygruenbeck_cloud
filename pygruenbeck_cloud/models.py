"""Models for Gruenbeck Cloud library."""
from __future__ import annotations

from dataclasses import dataclass, field
import datetime
import keyword
import logging
import re
from typing import Any

from pygruenbeck_cloud.const import (
    API_WS_RESPONSE_TYPE_DATA,
    API_WS_RESPONSE_TYPE_DATA_TARGETS,
    API_WS_RESPONSE_TYPE_PING,
    LOGIN_REFRESH_TIME_BEFORE_EXPIRE,
)
from pygruenbeck_cloud.exceptions import PyGruenbeckCloudError


def camel_to_snake(data: dict) -> dict:
    """Return dict with keys converted from camelCase to snake_case."""
    new_data = {}
    pattern = re.compile(r"(?<!^)(?=[A-Z])")  # camelCase to snake_case
    for key, value in data.items():
        var_name = pattern.sub("_", key).lower()
        if keyword.iskeyword(var_name):
            var_name = f"{var_name}_"
        new_data[var_name] = value

    return new_data


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
        return datetime.datetime.now() >= (
            self.expires_on - LOGIN_REFRESH_TIME_BEFORE_EXPIRE
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
    def from_json(data: dict) -> DeviceError:
        """Prepare values from json dict."""
        new_data = camel_to_snake(data)

        return DeviceError(**new_data)

    @property  # type: ignore[no-redef]
    def date(self) -> datetime.datetime | None:
        """Return date value."""
        return self._date

    @date.setter
    def date(self, value: str) -> None:
        """Parse and set date as datetime from string value."""
        datetime_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
        # Object seems to be UTC, so we need to set correct timezone
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
class DeviceParameters:
    """Object holding Device Parameters."""

    # Common
    dlst: bool  # pdlstauto -> Daylight saving time

    # Signals
    buzzer: bool  # pbuzzer -> signal on error
    buzzer_from: datetime.time  # pbuzzfrom
    buzzer_to: datetime.time  # pbuzzto
    push_notification: bool  # pallowpushnotification
    email_notification: bool  # pallowemail

    # Water
    water_hardness_unit: int  # ? phunit?
    raw_water_hardness: int  # prawhard
    soft_water_hardness: int  # psetsoft

    # Mode
    mode: int  # pmode
    # {% if value == '1' %}
    #               {% set modus = 'Eco' %}
    #           {% endif %}
    #           {% if value == '2' %}
    #               {% set modus = 'Comfort' %}
    #           {% endif %}
    #           {% if value == '3' %}
    #               {% set modus = 'Power' %}
    #           {% endif %}
    # Individual is 4?
    mode_monday: int  # pmodemo
    mode_tuesday: int  # pmodetu
    mode_wednesday: int  # pmodewe
    mode_thursday: int  # pmodeth
    mode_friday: int  # pmodefr
    mode_saturday: int  # pmodesa
    mode_sunday: int  # pmodesu

    # Regeneration
    regeneration_mode: int  # pregmode ?
    regeneration_time: datetime.time  # pregmo1 ?

    # Infos
    maintenance_interval: int  # pmaintint
    installer_name: str  # pname
    installer_phone: str  # ptelnr
    installer_email: str  # pmailadress

    # Additional unknown parameter
    pntpsync: bool
    pcfcontact: bool
    pknx: bool
    pmonflow: bool
    pmondisinf: bool
    pledatsaltpre: bool
    prescaplimit: int
    pcurrent: int
    pload: int
    pforcedregdist: int
    pfreqregvalve: int
    pfreqblendvalve: int
    pledbright: int
    pvolume: int
    ppratesoftwater: float
    pprateblending: float
    pprateregwater: float
    psetcapmo: int
    psetcaptu: int
    psetcapwe: int
    psetcapth: int
    psetcapfr: int
    psetcapsa: int
    psetcapsu: int
    pnomflow: float
    ppressurereg: int
    pmonregmeter: int
    pmonsalting: int
    prinsing: float
    pbackwash: int
    pwashingout: int
    pminvolmincap: float
    pmaxvolmincap: float
    pminvolmaxcap: float
    pmaxvolmaxcap: float
    pmaxdurdisinfect: int
    pmaxresdurreg: int
    planguage: int
    pprogout: int
    pprogin: int
    ppowerfail: int
    pmodedesinf: int
    pled: int
    pregmo1: datetime.time
    pregmo2: datetime.time
    pregmo3: datetime.time
    pregtu1: datetime.time
    pregtu2: datetime.time
    pregtu3: datetime.time
    pregwe1: datetime.time
    pregwe2: datetime.time
    pregwe3: datetime.time
    pregth1: datetime.time
    pregth2: datetime.time
    pregth3: datetime.time
    pregfr1: datetime.time
    pregfr2: datetime.time
    pregfr3: datetime.time
    pregsa1: datetime.time
    pregsa2: datetime.time
    pregsa3: datetime.time
    pregsu1: datetime.time
    pregsu2: datetime.time
    pregsu3: datetime.time
    pmonblend: int
    poverload: int
    pfreqregvalve2: int


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
    last_service: datetime.date
    errors: list[DeviceError]
    salt: list[DailyUsageEntry]
    water: list[DailyUsageEntry]
    hardware_version: str | None = None
    _last_service: datetime.date | None = field(init=False, repr=False, default=None)
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

    # Values from WebSocket
    soft_water_quantity: int | None = None
    regeneration_counter: int | None = None
    current_flow_rate: float | None = None
    remaining_capacity_volume: float | None = None
    remaining_capacity_percentage: int | None = None
    salt_range: int | None = None
    salt_consumption: float | None = None
    next_service: int | None = None

    # WebSocket PING counter
    ping_counter: int = 0

    # Logger instance
    logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def from_json(data: dict) -> Device:
        """Prepare values from json dict."""
        new_data = camel_to_snake(data)

        return Device(**new_data)

    def update_from_json(self, data: dict) -> Device:
        """Update current object from json dict."""
        new_data = camel_to_snake(data)

        for key, value in new_data.items():
            setattr(self, key, value)

        return self

    def update_from_response(self, data: dict[str, Any]) -> Device:
        """Update object with data from API response."""
        # Count how many PINGs we got in succession
        if data.get("type") == API_WS_RESPONSE_TYPE_PING:
            self.ping_counter += 1
        # Parse Message Data
        elif data.get("type") == API_WS_RESPONSE_TYPE_DATA:
            if not data.get("target") in API_WS_RESPONSE_TYPE_DATA_TARGETS:
                self.logger.debug(
                    "Got unknown target '%s' in response: %s", data.get("target"), data
                )
                return self

            message_arguments = data.get("arguments")
            if not message_arguments:
                self.logger.error("No arguments found in response: %s", data)
                return self

            # Reset ping counter if we got a valid response
            self.ping_counter = 0

            for message in message_arguments:
                if message.get("id") != self.serial_number:
                    msg = (
                        f"Expected id value {self.serial_number}"
                        f" but got {message.get('id')}"
                    )
                    raise PyGruenbeckCloudError(msg)

                if message.get("mcountwater1") is not None:
                    self.soft_water_quantity = message.get("mcountwater1")

                if message.get("mcountreg") is not None:
                    self.regeneration_counter = message.get("mcountreg")

                if message.get("mflow1") is not None:
                    self.current_flow_rate = float(message.get("mflow1"))

                if message.get("mrescapa1") is not None:
                    self.remaining_capacity_volume = message.get("mrescapa1")

                if message.get("mresidcap1") is not None:
                    self.remaining_capacity_percentage = message.get("mresidcap1")

                if message.get("msaltrange") is not None:
                    self.salt_range = message.get("msaltrange")

                if message.get("msaltusage") is not None:
                    self.salt_consumption = message.get("msaltusage")

                if message.get("mmaint") is not None:
                    self.next_service = message.get("mmaint")
        # Got an unknown response type
        else:
            self.logger.debug(
                "Got response type '%s' which we don't can process: %s",
                data.get("type"),
                data,
            )

        return self

    @property  # type: ignore[no-redef]
    def next_regeneration(self) -> datetime.datetime | None:
        """Return next regeneration value."""
        return self._next_regeneration

    @next_regeneration.setter
    def next_regeneration(self, value: str | property) -> None:
        """Parse and set next regeneration as datetime from string value."""
        if isinstance(value, property):
            return
        datetime_obj = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        # Timezone for next regeneration comes from {time_zone} parameter
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
            return
        self._startup = datetime.datetime.strptime(value, "%Y-%m-%d")

    @property  # type: ignore[no-redef]
    def last_service(self) -> datetime.date | None:
        """Return last service value."""
        return self._last_service

    @last_service.setter
    def last_service(self, value: str | property) -> None:
        """Parse and set last service as date from string value."""
        if isinstance(value, property):
            return
        self._last_service = datetime.datetime.strptime(value, "%Y-%m-%d")

    @property  # type: ignore[no-redef]
    def time_zone(self) -> datetime.tzinfo | None:
        """Return time zone value."""
        return self._time_zone

    @time_zone.setter
    def time_zone(self, value: str | property) -> None:
        """Parse and set time zone as tzinfo from string value."""
        if isinstance(value, property):
            return
        tzinfo = datetime.datetime.strptime(value, "%z").tzinfo
        # Provided data for {next_regneration} has no timezone, this is provided here
        if self._next_regeneration:
            self._next_regeneration = self._next_regeneration.replace(tzinfo=tzinfo)

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
            result.append(DeviceError.from_json(entry))

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
