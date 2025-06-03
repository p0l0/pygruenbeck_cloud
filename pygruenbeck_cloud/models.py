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
    PARAMETER_LANGUAGES,
    PARAMETER_LED_MODES,
    PARAMETER_OPERATION_MODES,
    PARAMETER_REGENERATION_MODES,
    PARAMETER_WATER_UNITS,
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
    error_code: int
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

    # Audio signal on error
    buzzer: bool | None = field(
        default=None,
        metadata=json_config(field_name="pbuzzer"),
    )
    # Audio signal release from [hh:mm]
    buzzer_from: datetime.time | None = field(
        default=None,
        metadata=json_config(field_name="pbuzzfrom"),
    )
    # Audio signal release until [hh:mm]
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

    # Water settings
    water_hardness_unit: int | None = field(
        default=None,
        metadata=json_config(
            field_name="phunit",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_WATER_UNITS))
            ),
        ),
    )
    raw_water_hardness: int | None = field(
        default=None,
        metadata=json_config(field_name="prawhard"),
    )
    soft_water_hardness: int | None = field(
        default=None,
        metadata=json_config(field_name="psetsoft"),
    )

    # Working mode
    mode: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmode",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_monday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodemo",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_tuesday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodetu",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_wednesday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodewe",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_thursday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodeth",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_friday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodefr",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_saturday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodesa",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )
    mode_individual_sunday: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pmodesu",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_OPERATION_MODES))
            ),
        ),
    )

    # Regeneration mode
    regeneration_mode: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pregmode",
            decoder=lambda value: (
                value
                if value is not False
                else next(iter(PARAMETER_REGENERATION_MODES))
            ),
        ),
    )

    regeneration_time_monday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregmo1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_monday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregmo2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_monday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregmo3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_tuesday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregtu1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_tuesday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregtu2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_tuesday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregtu3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_wednesday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregwe1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_wednesday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregwe2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_wednesday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregwe3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_thursday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregth1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_thursday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregth2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_thursday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregth3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_friday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregfr1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_friday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregfr2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_friday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregfr3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )
    # regeneration_time_saturday_1: str | None = field(
    #     default=None,
    #     metadata=json_config(field_name="pregsa1"),
    # )  # datetime.time | None = None
    regeneration_time_saturday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregsa1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_saturday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregsa2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_saturday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregsa3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_sunday_1: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregsu1",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_sunday_2: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregsu2",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    regeneration_time_sunday_3: datetime.time | None = field(
        default=None,
        metadata=json_config(
            field_name="pregsu3",
            encoder=lambda value: (
                value.strftime("%H:%M")
                if value is not None and value != "--:--"
                else None
            ),
            decoder=lambda value: (
                datetime.datetime.strptime(value, "%H:%M").time()
                if value is not None and value != "--:--"
                else None
            ),
            mm_field=mm_fields.Date(format="%H:%M"),
        ),
    )

    # Maintenance information [days]
    maintenance_interval: int | None = field(
        default=None,
        metadata=json_config(field_name="pmaintint"),
    )
    # Installer information
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

    # Get date/time automatically (NTP)
    ntp_sync: bool | None = field(
        default=None,
        metadata=json_config(field_name="pntpsync"),
    )

    # Function fault signal contact
    fault_signal_contact: bool | None = field(
        default=None,
        metadata=json_config(field_name="pcfcontact"),
    )

    # KNX connection
    knx: bool | None = field(
        default=None,
        metadata=json_config(field_name="pknx"),
    )

    # Monitoring of nominal flow
    nominal_flow_monitoring: bool | None = field(
        default=None,
        metadata=json_config(field_name="pmonflow"),
    )

    # Disinfection monitoring
    disinfection_monitoring: bool | None = field(
        default=None,
        metadata=json_config(field_name="pmondisinf"),
    )

    # Illuminated LED ring mode
    led_ring_mode: int | None = field(
        default=None,
        metadata=json_config(
            field_name="pled",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_LED_MODES))
            ),
        ),
    )
    # Illuminated LED ring flashes for pre-alarm salt supply
    led_ring_flash_on_signal: bool | None = field(
        default=None,
        metadata=json_config(field_name="pledatsaltpre"),
    )
    # LED ring Brightness [%]
    led_ring_brightness: int | None = field(
        default=None,
        metadata=json_config(field_name="pledbright"),
    )

    # Residual capacity limit value [%]
    residual_capacity_limit: int | None = field(
        default=None,
        metadata=json_config(field_name="prescaplimit"),
    )

    # Current setpoint [mA]
    current_setpoint: int | None = field(
        default=None,
        metadata=json_config(field_name="pcurrent"),
    )

    # Charge [mAmin]
    charge: int | None = field(
        default=None,
        metadata=json_config(field_name="pload"),
    )

    # Interval of forced regeneration [days]
    interval_forced_regeneration: int | None = field(
        default=None,
        metadata=json_config(field_name="pforcedregdist"),
    )

    # End frequency regeneration valve [Hz]
    end_frequency_regeneration_valve: int | None = field(
        default=None,
        metadata=json_config(field_name="pfreqregvalve"),
    )
    # End frequency regeneration valve 2 [Hz]
    end_frequency_regeneration_valve_2: int | None = field(
        default=None,
        metadata=json_config(field_name="pfreqregvalve2"),
    )

    # End frequency blending valve [Hz]
    end_frequency_blending_valve: int | None = field(
        default=None,
        metadata=json_config(field_name="pfreqblendvalve"),
    )

    # Treatment volume [m³]
    treatment_volume: int | None = field(
        default=None,
        metadata=json_config(field_name="pvolume"),
    )

    # Soft water meter pulse rate [l/Imp]
    soft_water_meter_pulse_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="ppratesoftwater"),
    )

    # Blending water meter pulse rate [l/Imp]
    blending_water_meter_pulse_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="pprateblending"),
    )

    # Regeneration water meter pulse rate [l/Imp]
    regeneration_water_meter_pulse_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="pprateregwater"),
    )

    # Capacity figure Monday [m³x°dH]
    capacity_figure_monday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcapmo"),
    )
    # Capacity figure Tuesday [m³x°dH]
    capacity_figure_tuesday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcaptu"),
    )
    # Capacity figure Wednesday [m³x°dH]
    capacity_figure_wednesday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcapwe"),
    )
    # Capacity figure Thursday [m³x°dH]
    capacity_figure_thursday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcapth"),
    )
    # Capacity figure Friday [m³x°dH]
    capacity_figure_friday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcapfr"),
    )
    # Capacity figure Saturday [m³x°dH]
    capacity_figure_saturday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcapsa"),
    )
    # Capacity figure Sunday [m³x°dH]
    capacity_figure_sunday: int | None = field(
        default=None,
        metadata=json_config(field_name="psetcapsu"),
    )

    # Nominal flow rate [m³/h]
    nominal_flow_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="pnomflow"),
    )

    # Regeneration monitoring time [min]
    regeneration_monitoring_time: int | None = field(
        default=None,
        metadata=json_config(field_name="pmonregmeter"),
    )
    # Salting monitoring time [min]
    salting_monitoring_time: int | None = field(
        default=None,
        metadata=json_config(field_name="pmonsalting"),
    )

    # Slow rinse [min]
    slow_rinse: float | None = field(
        default=None,
        metadata=json_config(field_name="prinsing"),
    )

    # Backwash [l]
    backwash: int | None = field(
        default=None,
        metadata=json_config(field_name="pbackwash"),
    )

    # Washing out [l]
    washing_out: int | None = field(
        default=None,
        metadata=json_config(field_name="pwashingout"),
    )

    # Minimum filling volume smallest cap [l]
    minimum_filling_volume_smallest_cap: float | None = field(
        default=None,
        metadata=json_config(field_name="pminvolmincap"),
    )
    # Maximum filling volume smallest cap [l]
    maximum_filling_volume_smallest_cap: float | None = field(
        default=None,
        metadata=json_config(field_name="pmaxvolmincap"),
    )
    # Minimum filling volume largest cap [l]
    minimum_filling_volume_largest_cap: float | None = field(
        default=None,
        metadata=json_config(field_name="pminvolmaxcap"),
    )
    # Maximum filling volume largest cap [l]
    maximum_filling_volume_largest_cap: float | None = field(
        default=None,
        metadata=json_config(field_name="pmaxvolmaxcap"),
    )

    # Longest switch-on time chlorine cell [min]
    longest_switch_on_time_chlorine_cell: int | None = field(
        default=None,
        metadata=json_config(field_name="pmaxdurdisinfect"),
    )

    # Maximum remaining time regeneration [min]
    maximum_remaining_time_regeneration: int | None = field(
        default=None,
        metadata=json_config(field_name="pmaxresdurreg"),
    )

    # Current language
    language: int | None = field(
        default=None,
        metadata=json_config(
            field_name="planguage",
            decoder=lambda value: (
                value if value is not False else next(iter(PARAMETER_LANGUAGES))
            ),
        ),
    )

    # Programmable output function
    programmable_output_function: int | None = field(
        default=None,
        metadata=json_config(field_name="pprogout"),
    )
    # Programmable input function
    programmable_input_function: int | None = field(
        default=None,
        metadata=json_config(field_name="pprogin"),
    )

    # Reaction to power failure > 5 min
    reaction_to_power_failure: int | None = field(
        default=None,
        metadata=json_config(field_name="ppowerfail"),
    )

    # Activate/deactivate chlorine cell
    chlorine_cell_mode: int | None = field(
        default=None,
        metadata=json_config(field_name="pmodedesinf"),
    )

    # Blending monitoring
    blending_monitoring: int | None = field(
        default=None,
        metadata=json_config(field_name="pmonblend"),
    )

    # System overloaded
    system_overloaded: int | None = field(
        default=None,
        metadata=json_config(field_name="poverload"),
    )
    # Unknown Parameter
    ppressurereg: int | None = field(
        default=None,
        metadata=json_config(field_name="ppressurereg"),
    )
    # pdate: "[yyyy.mm.dd] Current date",
    # pclearerrmem: "Delete error memory",
    # pclearcntwater: "Reset water meter",
    # pclearcntreg: "Reset regeneration counter",


@dataclass_json
@dataclass
class DeviceRealtimeInfo:
    """Object holding WebSocket realtime Information."""

    # Soft water exchanger 1 [l]
    soft_water_quantity: int | None = field(
        default=None,
        metadata=json_config(field_name="mcountwater1"),
    )
    # Soft water exchanger 2 [l]
    soft_water_quantity_2: int | None = field(
        default=None,
        metadata=json_config(field_name="mcountwater2"),
    )
    # Regeneration counter
    regeneration_counter: int | None = field(
        default=None,
        metadata=json_config(field_name="mcountreg"),
    )
    # Flow rate exchanger 1 [m³/h]
    current_flow_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="mflow1"),
    )
    # Flow rate exchanger 2 [m³/h]
    current_flow_rate_2: float | None = field(
        default=None,
        metadata=json_config(field_name="mflow2"),
    )
    # Soft water Exchanger 1 [m³]
    remaining_capacity_volume: float | None = field(
        default=None,
        metadata=json_config(field_name="mrescapa1"),
    )
    # Soft water Exchanger 2 [m³]
    remaining_capacity_volume_2: float | None = field(
        default=None,
        metadata=json_config(field_name="mrescapa2"),
    )
    # Residual capacity Exchanger 1 [%]
    remaining_capacity_percentage: int | None = field(
        default=None,
        metadata=json_config(field_name="mresidcap1"),
    )
    # Residual capacity Exchanger 2 [%]
    remaining_capacity_percentage_2: int | None = field(
        default=None,
        metadata=json_config(field_name="mresidcap2"),
    )
    # Salt-reach [days]
    salt_range: int | None = field(
        default=None,
        metadata=json_config(field_name="msaltrange"),
    )
    # Salt consumption [kg]
    salt_consumption: float | None = field(
        default=None,
        metadata=json_config(field_name="msaltusage"),
    )
    # Perform maintenance in [days]
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
    # Remaining amount / time of current regeneration step
    regeneration_remaining_time: float | None = field(
        default=None, metadata=json_config(field_name="mremregstep")
    )
    # Regeneration step
    regeneration_step: int | None = field(
        default=None,
        metadata=json_config(field_name="mregstatus"),
    )
    # Make-up water volume [l]
    make_up_water_volume: int | None = field(
        default=None,
        metadata=json_config(field_name="mcountwatertank"),
    )
    # During [min] int?
    # during_min: int | None = field(
    #     default=None,
    #     metadata=json_config(field_name="mflowexc"),
    # )
    # # : "[Min]", int?
    # make_up_water_volume: int | None = field(
    #     default=None,
    #     metadata=json_config(field_name="mflowexc2reg1"),
    # )
    # # : "[Min]", int?
    # make_up_water_volume: int | None = field(
    #     default=None,
    #     metadata=json_config(field_name="mflowexc1reg2"),
    # )

    # Adsorber exhausted percentage [%]
    exhausted_percentage: int | None = field(
        default=None,
        metadata=json_config(field_name="mlifeadsorb"),
    )
    # Actual value soft water hardness [°dh] - int?
    actual_value_soft_water_hardness: int | None = field(
        default=None,
        metadata=json_config(field_name="mhardsoftw"),
    )
    # Capacity figure [m³x°dH]
    capacity_figure: float | None = field(
        default=None,
        metadata=json_config(field_name="mcapacity"),
    )
    # Flow rate peak value [m³/h]
    flow_rate_peak_value: float | None = field(
        default=None,
        metadata=json_config(field_name="mflowmax"),
    )
    # Exchanger 1 peak value [m³/h] - float?
    exchanger_peak_value: float | None = field(
        default=None,
        metadata=json_config(field_name="mflowmax1reg2"),
    )
    # Exchanger 2 peak value [m³/h] - float?
    exchanger_peak_value_2: float | None = field(
        default=None,
        metadata=json_config(field_name="mflowmax2reg1"),
    )
    # Last regeneration Exchanger 1 [hh:mm]
    last_regeneration_exchanger: datetime.time | None = field(
        default=None,
        metadata=json_config(field_name="mendreg1"),
    )
    # Last regeneration Exchanger 2 [hh:mm]
    last_regeneration_exchanger_2: datetime.time | None = field(
        default=None,
        metadata=json_config(field_name="mendreg2"),
    )
    # # [%]?
    # percentage: int | None = field(
    #     default=None,
    #     metadata=json_config(field_name="mregpercent1"),
    # )
    # # 2 [%]?
    # percentage_2: int | None = field(
    #     default=None,
    #     metadata=json_config(field_name="mregpercent2"),
    # )
    # Regeneration flow rate Exchanger 1 [l/h] - int?
    regeneration_flow_rate_exchanger: int | None = field(
        default=None,
        metadata=json_config(field_name="mflowreg1"),
    )
    # Regeneration flow rate Exchanger 2 [l/h] - int?
    regeneration_flow_rate_exchanger_2: int | None = field(
        default=None,
        metadata=json_config(field_name="mflowreg2"),
    )
    # Blending flow rate [m³/h] - float?
    blending_flow_rate: float | None = field(
        default=None,
        metadata=json_config(field_name="mflowblend"),
    )
    # Step indication regeneration valve 1
    step_indication_regeneration_valve: int | None = field(
        default=None,
        metadata=json_config(field_name="mstep1"),
    )
    # Step indication regeneration valve 2
    step_indication_regeneration_valve_2: int | None = field(
        default=None,
        metadata=json_config(field_name="mstep2"),
    )
    # Current chlorine [mA]
    current_chlorine: int | None = field(
        default=None,
        metadata=json_config(field_name="mcurrent"),
    )
    # Adsorber remaining amount of water [m³] - float?
    remaining_amount_of_water: float | None = field(
        default=None,
        metadata=json_config(field_name="mreswatadmod"),
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
    # Start-up date
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
