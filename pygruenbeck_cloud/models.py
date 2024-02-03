"""Models for Gruenbeck Cloud library."""
from dataclasses import dataclass, field
import datetime
import logging
from typing import Any

from dataclasses_json import LetterCase, config as json_config, dataclass_json
from marshmallow import fields as mm_fields

from pygruenbeck_cloud.const import (
    API_WS_RESPONSE_TYPE_DATA,
    API_WS_RESPONSE_TYPE_DATA_TARGETS,
    API_WS_RESPONSE_TYPE_PING,
    LOGIN_REFRESH_TIME_BEFORE_EXPIRE,
)
from pygruenbeck_cloud.exceptions import PyGruenbeckCloudError


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


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DeviceError:
    """Object holding Device Error Information."""

    is_resolved: bool
    message: str
    type: str
    date: datetime.datetime = field(
        metadata=json_config(
            encoder=lambda value: value.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            # Object seems to be UTC, so we need to set correct timezone
            decoder=lambda value: datetime.datetime.strptime(
                value, "%Y-%m-%dT%H:%M:%S.%f"
            ).replace(tzinfo=datetime.UTC),
        ),
    )


@dataclass_json
@dataclass
class DailyUsageEntry:
    """Object holding daily usage data."""

    value: int
    date: datetime.date = field(
        metadata=json_config(
            encoder=lambda value: value.strftime("%Y-%m-%d"),
            decoder=lambda value: datetime.datetime.strptime(value, "%Y-%m-%d").date(),
            mm_field=mm_fields.Date(format="%Y-%m-%d"),
        ),
    )


@dataclass_json
@dataclass
class DeviceParameters:
    """Object holding Device Parameters."""

    # Daylight saving time
    dlst: bool | None = field(
        default=None,
        metadata=json_config(field_name="pdlstauto"),
    )

    # Signal on error
    buzzer: bool | None = field(
        default=None,
        metadata=json_config(field_name="pbuzzer"),
    )
    buzzer_from: datetime.time | None = field(
        default=None,
        metadata=json_config(field_name="pbuzzfrom"),
    )
    buzzer_to: datetime.time | None = field(
        default=None,
        metadata=json_config(field_name="pbuzzto"),
    )

    # Notifications
    push_notification: bool | None = field(
        default=None,
        metadata=json_config(field_name="pallowpushnotification"),
    )
    email_notification: bool | None = field(
        default=None,
        metadata=json_config(field_name="pallowemail"),
    )

    # Water
    water_hardness_unit: int | None = field(
        default=None,
        metadata=json_config(field_name="phunit"),
    )
    raw_water_hardness: int | None = field(
        default=None,
        metadata=json_config(field_name="prawhard"),
    )
    soft_water_hardness: int | None = field(
        default=None,
        metadata=json_config(field_name="psetsoft"),
    )

    # Mode
    mode: int | None = field(
        default=None,
        metadata=json_config(field_name="pmode"),
    )
    mode_individual_monday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodemo"),
    )
    mode_individual_tuesday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodetu"),
    )
    mode_individual_wednesday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodewe"),
    )
    mode_individual_thursday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodeth"),
    )
    mode_individual_friday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodefr"),
    )
    mode_individual_saturday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodesa"),
    )
    mode_individual_sunday: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodesu"),
    )

    # Regeneration
    regeneration_mode: int | None = field(
        default=None,
        metadata=json_config(field_name="pregmode"),
    )
    regeneration_time_monday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregmo1"),
    )  # datetime.time | None = None
    regeneration_time_monday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregmo2"),
    )  # datetime.time | None = None
    regeneration_time_monday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregmo3"),
    )  # datetime.time | None = None
    regeneration_time_tuesday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregtu1"),
    )  # datetime.time | None = None
    regeneration_time_tuesday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregtu2"),
    )  # datetime.time | None = None
    regeneration_time_tuesday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregtu3"),
    )  # datetime.time | None = None
    regeneration_time_wednesday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregwe1"),
    )  # datetime.time | None = None
    regeneration_time_wednesday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregwe2"),
    )  # datetime.time | None = None
    regeneration_time_wednesday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregwe3"),
    )  # datetime.time | None = None
    regeneration_time_thursday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregth1"),
    )  # datetime.time | None = None
    regeneration_time_thursday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregth2"),
    )  # datetime.time | None = None
    regeneration_time_thursday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregth3"),
    )  # datetime.time | None = None
    regeneration_time_friday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregfr1"),
    )  # datetime.time | None = None
    regeneration_time_friday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregfr2"),
    )  # datetime.time | None = None
    regeneration_time_friday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregfr3"),
    )  # datetime.time | None = None
    regeneration_time_saturday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregsa1"),
    )  # datetime.time | None = None
    regeneration_time_saturday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregsa2"),
    )  # datetime.time | None = None
    regeneration_time_saturday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregsa3"),
    )  # datetime.time | None = None
    regeneration_time_sunday_1: str | None = field(
        default=None,
        metadata=json_config(field_name="pregsu1"),
    )  # datetime.time | None = None
    regeneration_time_sunday_2: str | None = field(
        default=None,
        metadata=json_config(field_name="pregsu2"),
    )  # datetime.time | None = None
    regeneration_time_sunday_3: str | None = field(
        default=None,
        metadata=json_config(field_name="pregsu3"),
    )  # datetime.time | None = None

    # Maintenance Information
    maintenance_interval: int | None = field(
        default=None,
        metadata=json_config(field_name="pmaintint"),
    )
    installer_name: str | None = field(
        default=None,
        metadata=json_config(field_name="pname"),
    )
    installer_phone: str | None = field(
        default=None,
        metadata=json_config(field_name="ptelnr"),
    )
    installer_email: str | None = field(
        default=None,
        metadata=json_config(field_name="pmailadress"),
    )

    # Additional unknown parameter
    pntpsync: bool | None = None
    pcfcontact: bool | None = None
    pknx: bool | None = None
    pmonflow: bool | None = None
    pmondisinf: bool | None = None
    pledatsaltpre: bool | None = None
    prescaplimit: int | None = None
    pcurrent: int | None = None
    pload: int | None = None
    pforcedregdist: int | None = None
    pfreqregvalve: int | None = None
    pfreqblendvalve: int | None = None
    pledbright: int | None = None
    pvolume: int | None = None
    ppratesoftwater: float | None = None
    pprateblending: float | None = None
    pprateregwater: float | None = None
    psetcapmo: int | None = None
    psetcaptu: int | None = None
    psetcapwe: int | None = None
    psetcapth: int | None = None
    psetcapfr: int | None = None
    psetcapsa: int | None = None
    psetcapsu: int | None = None
    pnomflow: float | None = None
    ppressurereg: int | None = None
    pmonregmeter: int | None = None
    pmonsalting: int | None = None
    prinsing: float | None = None
    pbackwash: int | None = None
    pwashingout: int | None = None
    pminvolmincap: float | None = None
    pmaxvolmincap: float | None = None
    pminvolmaxcap: float | None = None
    pmaxvolmaxcap: float | None = None
    pmaxdurdisinfect: int | None = None
    pmaxresdurreg: int | None = None
    planguage: int | None = None
    pprogout: int | None = None
    pprogin: int | None = None
    ppowerfail: int | None = None
    pmodedesinf: int | None = None
    pled: int | None = None
    pmonblend: int | None = None
    poverload: int | None = None
    pfreqregvalve2: int | None = None


@dataclass_json
@dataclass
class DeviceRealtimeInfo:
    """Object holding WebSocket realtime Information."""

    soft_water_quantity: int | None = field(
        default=None,
        metadata=json_config(field_name="mcountwater1"),
    )
    regeneration_counter: int | None = field(
        default=None,
        metadata=json_config(field_name="mcountreg"),
    )
    current_flow_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="mflow1"),
    )
    remaining_capacity_volume: float | None = field(
        default=None,
        metadata=json_config(field_name="mrescapa1"),
    )
    remaining_capacity_percentage: int | None = field(
        default=None,
        metadata=json_config(field_name="mresidcap1"),
    )
    salt_range: int | None = field(
        default=None,
        metadata=json_config(field_name="msaltrange"),
    )
    salt_consumption: float | None = field(
        default=None,
        metadata=json_config(field_name="msaltusage"),
    )
    next_service: int | None = field(
        default=None,
        metadata=json_config(field_name="mmaint"),
    )
    # @TODO - This two parameter provide information about running regeneration
    #   if both have value 0 when no regeneration is running.
    #   Current observations:
    #   mremregstep -> on regeneration start it seems to increase from 0 it seems to
    #       increase slowly up to 1,5 and then it changes with a big step to > 4400
    #   mregstatus -> when mremregstep is between 0 and 1,5, mremregstep has the
    #       value 10 as soon as mremregstep is > 4400 then it changes to 20
    #       on mremregstep ~= 300 it changes to 30 and when < 10 it changes to 40
    mremregstep: float | None = field(
        default=None, metadata=json_config(field_name="mremregstep")
    )
    mregstatus: int | None = field(
        default=None,
        metadata=json_config(field_name="mregstatus"),
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
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
    _next_regeneration_raw: datetime.datetime | None = field(
        default=None,
        metadata=json_config(
            field_name="nextRegeneration",
            encoder=lambda value: (
                value.strftime("%Y-%m-%dT%H:%M:%S") if value is not None else None
            ),
            decoder=lambda value: datetime.datetime.strptime(
                value, "%Y-%m-%dT%H:%M:%S"
            ),
        ),
    )
    time_zone: datetime.tzinfo | None = field(
        default=None,
        metadata=json_config(
            encoder=lambda value: value,
            decoder=lambda value: datetime.datetime.strptime(value, "%z").tzinfo,
        ),
    )
    startup: datetime.date | None = field(
        default=None,
        metadata=json_config(
            encoder=lambda value: (
                value.strftime("%Y-%m-%d") if value is not None else None
            ),
            decoder=lambda value: datetime.datetime.strptime(value, "%Y-%m-%d").date(),
            # mm_field=mm_fields.DateTime(format="%Y-%m-%d"),
        ),
    )
    last_service: datetime.date | None = field(
        default=None,
        metadata=json_config(
            encoder=lambda value: (
                value.strftime("%Y-%m-%d") if value is not None else None
            ),
            decoder=lambda value: datetime.datetime.strptime(value, "%Y-%m-%d").date(),
            # mm_field=mm_fields.DateTime(format="%Y-%m-%d"),
        ),
    )
    errors: list[DeviceError] | None = field(
        default=None,
        metadata=json_config(
            encoder=lambda value: value,
            decoder=lambda value: DeviceError.schema().load(value, many=True),  # type: ignore[attr-defined]  # noqa: E501  # pylint: disable=no-member
        ),
    )

    salt: list[DailyUsageEntry] | None = field(
        default=None,
        metadata=json_config(
            encoder=lambda value: value,
            decoder=lambda value: DailyUsageEntry.schema().load(value, many=True),  # type: ignore[attr-defined]  # noqa: E501  # pylint: disable=no-member
        ),
    )
    water: list[DailyUsageEntry] | None = field(
        default=None,
        metadata=json_config(
            encoder=lambda value: value,
            decoder=lambda value: DailyUsageEntry.schema().load(value, many=True),  # type: ignore[attr-defined]  # noqa: E501  # pylint: disable=no-member
        ),
    )
    hardware_version: str | None = None
    mode: int | None = None
    nominal_flow: float | None = None
    raw_water: float | None = None
    soft_water: float | None = None
    software_version: str | None = None
    unit: int | None = None

    # Values from WebSocket
    realtime: DeviceRealtimeInfo = field(default_factory=DeviceRealtimeInfo)

    # Device Parameter Values
    parameters: DeviceParameters = field(default_factory=DeviceParameters)

    # Logger instance
    logger: logging.Logger = logging.getLogger(__name__)

    def update_from_dict(self, data: dict) -> "Device":
        """Update current object from json dict."""
        return self.from_dict(self.to_dict() | data)  # type: ignore[attr-defined,no-any-return]  # noqa: E501  # pylint: disable=no-member

    def update_from_response(self, data: dict[str, Any]) -> "Device":
        """Update object with data from API response."""
        # If we got PING, do nothing
        if data.get("type") == API_WS_RESPONSE_TYPE_PING:
            return self

        # Parse Message Data
        if data.get("type") == API_WS_RESPONSE_TYPE_DATA:
            if not data.get("target") in API_WS_RESPONSE_TYPE_DATA_TARGETS:
                self.logger.debug(
                    "Got unknown target '%s' in response: %s", data.get("target"), data
                )
                return self

            message_arguments = data.get("arguments")
            if not message_arguments:
                self.logger.error("No arguments found in response: %s", data)
                return self

            for message in message_arguments:
                if message.get("id") != self.serial_number:
                    msg = (
                        f"Expected id value {self.serial_number}"
                        f" but got {message.get('id')}"
                    )
                    raise PyGruenbeckCloudError(msg)

                self.realtime = DeviceRealtimeInfo.from_dict(  # type: ignore[attr-defined]  # noqa: E501  # pylint: disable=no-member
                    self.realtime.to_dict() | message  # type: ignore[attr-defined]  # noqa: E501  # pylint: disable=no-member
                )
        # Got an unknown response type
        else:
            self.logger.debug(
                "Got response type '%s' which we don't can process: %s",
                data.get("type"),
                data,
            )

        return self

    @property
    def next_regeneration(self) -> datetime.datetime | None:
        """Return next regeneration value."""
        if self._next_regeneration_raw is None:
            return None

        return self._next_regeneration_raw.replace(tzinfo=self.time_zone)
