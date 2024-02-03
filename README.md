# pygruenbeck_cloud

<p align="center">
    <a href="https://www.gruenbeck.com/" target="_blank"><img src="https://www.gruenbeck.com/typo3conf/ext/sitepackage_gruenbeck/Resources/Public/Images/gruenbeck-logo.svg" alt="Gruenbeck" /></a>
</p>

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pygruenbeck_cloud?logo=python)
[![PyPI release](https://img.shields.io/pypi/v/pygruenbeck_cloud)](https://pypi.org/project/pygruenbeck_cloud/)
![Release status](https://img.shields.io/pypi/status/pygruenbeck_cloud)
![Build Pipeline](https://img.shields.io/github/actions/workflow/status/p0l0/pygruenbeck_cloud/ci.yml)
[![codecov](https://codecov.io/gh/p0l0/pygruenbeck_cloud/branch/main/graph/badge.svg?token=V5C2O6SK2O)](https://codecov.io/gh/p0l0/pygruenbeck_cloud)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=f8b424)](https://github.com/pre-commit/pre-commit)
![License](https://img.shields.io/github/license/p0l0/pygruenbeck_cloud)

`pygruenbeck_cloud` is a Python 3 (>= 3.11) library to communicate with the Grünbeck Cloud based Water softeners.

It is intended to be used in custom_component [hagruenbeck_cloud](https://github.com/p0l0/hagruenbeck_cloud) for [Home Assistant](https://www.home-assistant.io/).

Implementation is based on the [ioBroker gruenbeck adapter](https://github.com/TA2k/ioBroker.gruenbeck) implementation.

### Available configuration parameter

| Parameter                     | Type         | Description                                                                      |
|-------------------------------|--------------|----------------------------------------------------------------------------------|
| dslt                          | boolean      | Activation of daylight saving time                                               |
| buzzer                        | boolean      | Activation of signal on error                                                    |
| buzzer_from                   | time (HH:MM) | Signal from time                                                                 |
| buzzer_to                     | time (HH:MM) | Signal from time                                                                 |
| push_notification             | boolean      | Activation of push notifications                                                 |
| email_notification            | boolean      | Activation of email notifications                                                |
| water_hardness_unit           | integer      | Water hardness Unit (1 = "°dH", 2 = "°fH", 3 = "°e", 4 = "mol/m³", 5 = "ppm")    |
| raw_water_hardness            | integer      | Water hardness value                                                             |
| soft_water_hardness           | integer      | Softwater hardness value                                                         |
| mode                          | integer      | Current operation mode (1 = "Eco", 2 = "Comfort", 3 = "Power", 4 = "Individual") |
| mode_individual_monday        | integer      | Individual mode for Monday                                                       |
| mode_individual_tuesday       | integer      | Individual mode for Tuesday                                                      |
| mode_individual_wednesday     | integer      | Individual mode for Wednesday                                                    |
| mode_individual_thursday      | integer      | Individual mode for Thursday                                                     |
| mode_individual_friday        | integer      | Individual mode for Friday                                                       |
| mode_individual_saturday      | integer      | Individual mode for Saturday                                                     |
| mode_individual_sunday        | integer      | Individual mode for Sunday                                                       |
| regeneration_mode             | integer      | Regeneration mode (0 = "Auto", 1 = "Fixed")                                      |
| regeneration_time_monday_1    | string       | Custom regeneration time for Monday 1 (Format: HH:MM)                            |                                                                                  |
| regeneration_time_monday_2    | string       | Custom regeneration time for Monday 2 (Format: HH:MM)                            |
| regeneration_time_monday_3    | string       | Custom regeneration time for Monday 3 (Format: HH:MM)                            |
| regeneration_time_tuesday_1   | string       | Custom regeneration time for Tuesday 1 (Format: HH:MM)                           |                                                                                  |
| regeneration_time_tuesday_2   | string       | Custom regeneration time for Tuesday 2 (Format: HH:MM)                           |
| regeneration_time_tuesday_3   | string       | Custom regeneration time for Tuesday 3 (Format: HH:MM)                           |
| regeneration_time_wednesday_1 | string       | Custom regeneration time for Wednesday 1 (Format: HH:MM)                         |                                                                                  |
| regeneration_time_wednesday_2 | string       | Custom regeneration time for Wednesday 2 (Format: HH:MM)                         |
| regeneration_time_wednesday_3 | string       | Custom regeneration time for Wednesday 3 (Format: HH:MM)                         |
| regeneration_time_thursday_1  | string       | Custom regeneration time for Thursday 1 (Format: HH:MM)                          |                                                                                  |
| regeneration_time_thursday_2  | string       | Custom regeneration time for Thursday 2 (Format: HH:MM)                          |
| regeneration_time_thursday_3  | string       | Custom regeneration time for Thursday 3 (Format: HH:MM)                          |
| regeneration_time_friday_1    | string       | Custom regeneration time for Friday 1 (Format: HH:MM)                            |                                                                                  |
| regeneration_time_friday_2    | string       | Custom regeneration time for Friday 2 (Format: HH:MM)                            |
| regeneration_time_friday_3    | string       | Custom regeneration time for Friday 3 (Format: HH:MM)                            |
| regeneration_time_saturday_1  | string       | Custom regeneration time for Saturday 1 (Format: HH:MM)                          |                                                                                  |
| regeneration_time_saturday_2  | string       | Custom regeneration time for Saturday 2 (Format: HH:MM)                          |
| regeneration_time_saturday_3  | string       | Custom regeneration time for Saturday 3 (Format: HH:MM)                          |
| regeneration_time_sunday_1    | string       | Custom regeneration time for Sunday 1 (Format: HH:MM)                            |                                                                                  |
| regeneration_time_sunday_2    | string       | Custom regeneration time for Sunday 2 (Format: HH:MM)                            |
| regeneration_time_sunday_3    | string       | Custom regeneration time for Sunday 3 (Format: HH:MM)                            |
| maintenance_interval          | integer      | Maintenance interval in days                                                     |
| installer_name                | string       | Installer name                                                                   |
| installer_phone               | string       | Installer phone                                                                  |
| installer_email               | string       | Installer email                                                                  |

And these are additional parameter which are provided by the API, but their meaning and/or value is not known:

| Parameter        | Type  |
|------------------|-------|
| pntpsync         | bool  |
| pcfcontact       | bool  |
| pknx             | bool  |
| pmonflow         | bool  |
| pmondisinf       | bool  |
| pledatsaltpre    | bool  |
| prescaplimit     | int   |
| pcurrent         | int   |
| pload            | int   |
| pforcedregdist   | int   |
| pfreqregvalve    | int   |
| pfreqblendvalve  | int   |
| pledbright       | int   |
| pvolume          | int   |
| ppratesoftwater  | float |
| pprateblending   | float |
| pprateregwater   | float |
| psetcapmo        | int   |
| psetcaptu        | int   |
| psetcapwe        | int   |
| psetcapth        | int   |
| psetcapfr        | int   |
| psetcapsa        | int   |
| psetcapsu        | int   |
| pnomflow         | float |
| ppressurereg     | int   |
| pmonregmeter     | int   |
| pmonsalting      | int   |
| prinsing         | float |
| pbackwash        | int   |
| pwashingout      | int   |
| pminvolmincap    | float |
| pmaxvolmincap    | float |
| pminvolmaxcap    | float |
| pmaxvolmaxcap    | float |
| pmaxdurdisinfect | int   |
| pmaxresdurreg    | int   |
| planguage        | int   |
| pprogout         | int   |
| pprogin          | int   |
| ppowerfail       | int   |
| pmodedesinf      | int   |
| pled             | int   |
| pmonblend        | int   |
| poverload        | int   |
| pfreqregvalve2   | int   |

Feel free to open an [issue](https://github.com/p0l0/pygruenbeck_cloud/issues) if you know the meaning of them and their possible values.
