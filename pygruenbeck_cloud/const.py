"""Constants for the Gruenbeck Cloud library."""

from datetime import timedelta
import re
from typing import Any, Final

import aiohttp
from yarl._url import DEFAULT_PORTS

# User Agent configuration
USER_AGENT_APP: Final = "Gruenbeck/354 CFNetwork/1209 Darwin/20.2.0"
USER_AGENT_WS: Final = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X)"
    " AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
)

# API Parameters mapping
PARAM_NAME_CODE_CHALLENGE: Final = "code_challenge"
PARAM_NAME_CSRF_TOKEN: Final = "csrf_token"
PARAM_NAME_TENANT: Final = "tenant"
PARAM_NAME_TRANS_ID: Final = "transId"
PARAM_NAME_POLICY: Final = "policy"
PARAM_NAME_USERNAME: Final = "signInName"
PARAM_NAME_PASSWORD: Final = "password"
PARAM_NAME_CODE: Final = "code"
PARAM_NAME_CODE_VERIFIER: Final = "code_verifier"
PARAM_NAME_ACCESS_TOKEN: Final = "access_token"
PARAM_NAME_REFRESH_TOKEN: Final = "refresh_token"
PARAM_NAME_CONNECTION_ID: Final = "connection_id"
PARAM_NAME_DEVICE_ID: Final = "device_id"
PARAM_NAME_ENDPOINT: Final = "endpoint"


# Details needed for login
LOGIN_SCHEME: Final = "https"
LOGIN_HOST: Final = "gruenbeckb2c.b2clogin.com"
LOGIN_CODE_CHALLENGE_CHARS: Final = (
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
)
LOGIN_REFRESH_TIME_BEFORE_EXPIRE = timedelta(minutes=10)

# HTTP API Details
API_SCHEME: Final = "https"
API_HOST: Final = "prod-eu-gruenbeck-api.azurewebsites.net"
API_VERSION: Final = "2024-05-02"
API_GET_MG_INFOS_ENDPOINT: Final = ""  # Endpoint is empty for normal MG Infos
API_GET_MG_INFOS_ENDPOINT_PARAMETERS: Final = "parameters"
API_GET_MG_INFOS_ENDPOINT_SALT_MEASUREMENTS: Final = "measurements/salt"
API_GET_MG_INFOS_ENDPOINT_WATER_MEASUREMENTS: Final = "measurements/water"

# WS API Details
API_WS_SCHEME_HTTP: Final = "https"
API_WS_SCHEME_WS: Final = "wss"
API_WS_HOST: Final = "prod-eu-gruenbeck-signalr.service.signalr.net"
API_WS_REQUEST_TIMEOUT: Final = 2 * 60  # 2 minutes
API_WS_CLIENT_URL: Final = "/client/"
API_WS_CLIENT_QUERY: dict[str, str] = {
    "hub": "gruenbeck",
    "id": f"{{{PARAM_NAME_CONNECTION_ID}}}",
    "access_token": f"{{{PARAM_NAME_ACCESS_TOKEN}}}",
}
API_WS_CLIENT_HEADER: dict[str, str] = {
    "Upgrade": "websocket",
    "Host": "prod-eu-gruenbeck-signalr.service.signalr.net",
    "Origin": "null",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "User-Agent": USER_AGENT_WS,
}
# There is a "%1E = Record Separator" char at the end of the string!
API_WS_INITIAL_MESSAGE: Final = '{"protocol":"json","version":1}'
API_WS_RESPONSE_TYPE_PING: Final = 6
API_WS_RESPONSE_TYPE_DATA: Final = 1
API_WS_RESPONSE_TYPE_DATA_TARGETS: list[str] = [
    "SendOneTimeMessageToDevice",
    "SendMessageToDevice",
]

# Web Request details
WEB_REQUESTS: dict[str, dict[str, Any]] = {
    "login_step_1": {
        "scheme": LOGIN_SCHEME,
        "host": LOGIN_HOST,
        "port": DEFAULT_PORTS.get(LOGIN_SCHEME),
        "path": (
            "/a50d35c1-202f-4da7-aa87-76e51a3098c6/b2c_1a_signinup/oauth2/v2.0/authorize"  # noqa: E501
        ),
        "method": aiohttp.hdrs.METH_GET,
        "use_cookies": True,
        "data": {},
        "json_data": False,
        "query_params": {
            "x-client-Ver": "0.8.0",
            "state": "NjkyQjZBQTgtQkM1My00ODBDLTn3MkYtOTZCQ0QyQkQ2NEE5",
            "client_info": "1",
            "response_type": "code",
            "code_challenge_method": "S256",
            "x-app-name": "Grünbeck",
            "x-client-OS": "14.3",
            "x-app-ver": "1.2.1",
            "scope": (
                "https://gruenbeckb2c.onmicrosoft.com/iot/user_impersonation openid profile offline_access"  # noqa: E501
            ),
            "x-client-SKU": "MSAL.iOS",
            "code_challenge": f"{{{PARAM_NAME_CODE_CHALLENGE}}}",
            "x-client-CPU": "64",
            "client-request-id": "F2929DED-2C9D-49F5-A0F4-31215427667C",
            "redirect_uri": "msal5a83cc16-ffb1-42e9-9859-9fbf07f36df8://auth",
            "client_id": "5a83cc16-ffb1-42e9-9859-9fbf07f36df8",
            "haschrome": "1",
            "return-client-request-id": "true",
            "x-client-DM": "iPhone",
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive",
            "Accept-Language": "de-de",
            "User-Agent": USER_AGENT_APP,
        },
    },
    "login_step_2": {
        "scheme": LOGIN_SCHEME,
        "host": LOGIN_HOST,
        "port": DEFAULT_PORTS.get(LOGIN_SCHEME),
        "path": f"{{{PARAM_NAME_TENANT}}}/SelfAsserted",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": True,
        "data": {
            "request_type": "RESPONSE",
            "signInName": f"{{{PARAM_NAME_USERNAME}}}",
            "password": f"{{{PARAM_NAME_PASSWORD}}}",
        },
        "json_data": False,
        "query_params": {
            "tx": f"{{{PARAM_NAME_TRANS_ID}}}",
            "p": f"{{{PARAM_NAME_POLICY}}}",
        },
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-CSRF-TOKEN": f"{{{PARAM_NAME_CSRF_TOKEN}}}",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://gruenbeckb2c.b2clogin.com",
            "User-Agent": USER_AGENT_APP,
        },
    },
    "login_step_3": {
        "scheme": LOGIN_SCHEME,
        "host": LOGIN_HOST,
        "port": DEFAULT_PORTS.get(LOGIN_SCHEME),
        "path": f"{{{PARAM_NAME_TENANT}}}/api/CombinedSigninAndSignup/confirmed",
        "method": aiohttp.hdrs.METH_GET,
        "use_cookies": True,
        "data": {},
        "json_data": False,
        "query_params": {
            "csrf_token": f"{{{PARAM_NAME_CSRF_TOKEN}}}",
            "tx": f"{{{PARAM_NAME_TRANS_ID}}}",
            "p": f"{{{PARAM_NAME_POLICY}}}",
        },
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "br, gzip, deflate",
            "Connection": "keep-alive",
            "Accept-Language": "de-de",
            "User-Agent": USER_AGENT_APP,
        },
    },
    "login_step_4": {
        "scheme": LOGIN_SCHEME,
        "host": LOGIN_HOST,
        "port": DEFAULT_PORTS.get(LOGIN_SCHEME),
        "path": f"{{{PARAM_NAME_TENANT}}}/oauth2/v2.0/token",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": True,
        "data": {
            "client_info": "1",
            "scope": (
                "https://gruenbeckb2c.onmicrosoft.com/iot/user_impersonation openid profile offline_access"  # noqa: E501
            ),
            "code": f"{{{PARAM_NAME_CODE}}}",
            "grant_type": "authorization_code",
            "code_verifier": f"{{{PARAM_NAME_CODE_VERIFIER}}}",
            "redirect_uri": "msal5a83cc16-ffb1-42e9-9859-9fbf07f36df8://auth",
            "client_id": "5a83cc16-ffb1-42e9-9859-9fbf07f36df8",
        },
        "json_data": False,
        "query_params": {},
        "headers": {
            "Host": "gruenbeckb2c.b2clogin.com",
            "x-client-SKU": "MSAL.iOS",
            "Accept": "application/json",
            "x-client-OS": "14.3",
            "x-app-name": "Grünbeck",
            "x-client-CPU": "64",
            "x-app-ver": "1.2.0",
            "Accept-Language": "de-de",
            "client-request-id": "F2929DED-2C9D-49F5-A0F4-31215427667C",
            "x-ms-PkeyAuth": "1.0",
            "x-client-Ver": "0.8.0",
            "x-client-DM": "iPhone",
            "User-Agent": USER_AGENT_APP,
            "return-client-request-id": "true",
        },
    },
    "web_token_refresh": {
        "scheme": LOGIN_SCHEME,
        "host": LOGIN_HOST,
        "port": DEFAULT_PORTS.get(LOGIN_SCHEME),
        "path": f"{{{PARAM_NAME_TENANT}}}/oauth2/v2.0/token",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": False,
        "data": {
            "client_info": "1",
            "scope": (
                "https://gruenbeckb2c.onmicrosoft.com/iot/user_impersonation openid profile offline_access"  # noqa: E501
            ),
            "grant_type": "refresh_token",
            "refresh_token": f"{{{PARAM_NAME_REFRESH_TOKEN}}}",
            "client_id": "5a83cc16-ffb1-42e9-9859-9fbf07f36df8",
        },
        "json_data": False,
        "query_params": {},
        "headers": {
            "Host": "gruenbeckb2c.b2clogin.com",
            "x-client-SKU": "MSAL.iOS",
            "Accept": "application/json",
            "x-client-OS": "14.3",
            "x-app-name": "Grünbeck",
            "x-client-CPU": "64",
            "x-app-ver": "1.2.0",
            "Accept-Language": "de-de",
            "client-request-id": "F2929DED-2C9D-49F5-A0F4-31215427667C",
            "User-Agent": USER_AGENT_APP,
            "x-client-Ver": "0.8.0",
            "x-client-DM": "iPhone",
            "return-client-request-id": "true",
            "cache-control": "no-cache",
        },
    },
    "start_ws_negotiation": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": "/api/realtime/negotiate",
        "method": aiohttp.hdrs.METH_GET,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {},
        "headers": {
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "file://",
            "Accept": "*/*",
            "User-Agent": USER_AGENT_APP,
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
            "Accept-Language": "de-de",
            "cache-control": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
        },
    },
    "get_ws_connection_id": {
        "scheme": API_WS_SCHEME_HTTP,
        "host": API_WS_HOST,
        "port": DEFAULT_PORTS.get(API_WS_SCHEME_HTTP),
        "path": "/client/negotiate",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {"hub": "gruenbeck"},
        "headers": {
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "file://",
            "Accept": "*/*",
            "User-Agent": USER_AGENT_APP,
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
            "Accept-Language": "de-de",
            "X-Requested-With": "XMLHttpRequest",
        },
    },
    "get_devices": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": "/api/devices",
        "method": aiohttp.hdrs.METH_GET,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
            "cache-control": "no-cache",
        },
    },
    "get_device_infos_request": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": f"/api/devices/{{{PARAM_NAME_DEVICE_ID}}}/{{{PARAM_NAME_ENDPOINT}}}",
        "method": aiohttp.hdrs.METH_GET,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
            "cache-control": "no-cache",
        },
    },
    "enter_sd": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": f"/api/devices/{{{PARAM_NAME_DEVICE_ID}}}/realtime/enter",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
        },
    },
    "refresh_sd": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": f"/api/devices/{{{PARAM_NAME_DEVICE_ID}}}/realtime/refresh",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
        },
    },
    "leave_sd": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": f"/api/devices/{{{PARAM_NAME_DEVICE_ID}}}/realtime/leave",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
        },
    },
    "update_device_parameter": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": f"/api/devices/{{{PARAM_NAME_DEVICE_ID}}}/parameters",
        "method": aiohttp.hdrs.METH_PATCH,
        "use_cookies": False,
        "data": {},
        "json_data": True,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
        },
    },
    "regenerate": {
        "scheme": API_SCHEME,
        "host": API_HOST,
        "port": DEFAULT_PORTS.get(API_SCHEME),
        "path": f"/api/devices/{{{PARAM_NAME_DEVICE_ID}}}/regenerate",
        "method": aiohttp.hdrs.METH_POST,
        "use_cookies": False,
        "data": {},
        "json_data": True,
        "query_params": {
            "api-version": API_VERSION,
        },
        "headers": {
            "Host": "prod-eu-gruenbeck-api.azurewebsites.net",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": USER_AGENT_APP,
            "Accept-Language": "de-de",
            "Authorization": f"Bearer {{{PARAM_NAME_ACCESS_TOKEN}}}",
        },
    },
    "placeholder": {
        "scheme": LOGIN_SCHEME,
        "host": LOGIN_HOST,
        "port": DEFAULT_PORTS.get(LOGIN_SCHEME),
        "path": "/path",
        "method": aiohttp.hdrs.METH_GET,
        "use_cookies": False,
        "data": {},
        "json_data": False,
        "query_params": {},
        "headers": {},
    },
}

# Diagnostic
DIAGNOSTIC_REDACTED: Final = "**REDACTED**"
DIAGNOSTIC_REGEX: list[dict[str, Any]] = [
    {
        "regex": re.compile(r"%3d([A-Za-z0-9_\-\.]+)(%26|\")"),
        "index": 0,
    },
    {
        "regex": re.compile(
            r"(access_token|id_token|client_info|resource|refresh_token|id|serialNumber|accessToken|connectionId|pmailadress|pname|ptelnr)\":\s*\"([A-Za-z0-9_\-\.\/\s@+]+)\""  # noqa: E501
        ),
        "index": 1,
    },
    {
        "regex": re.compile(r"Bearer ([A-Za-z0-9_\-\.]+)"),
        "index": 0,
    },
]

# Mapping of some Parameter from API
PARAMETER_OPERATION_MODES: dict[int, str] = {
    1: "Eco",
    2: "Comfort",
    3: "Power",
    4: "Individual",
}

PARAMETER_OPERATION_MODES_INDIVIDUAL: Final = 4

PARAMETER_REGENERATION_MODES: dict[int, str] = {
    0: "Automatic",
    1: "Fixed",
}

PARAMETER_WATER_UNITS: dict[int, str] = {
    1: "°dH",
    2: "°fH",
    3: "°e",
    4: "mol/m³",
    5: "ppm",
}

PARAMETER_REGENERATION_STEP: dict[int, str] = {
    0: "Inactive",
    10: "Fill salt tank",
    20: "Salting",
    30: "Displacement",
    40: "Backwashing",
    50: "Backwashing",
    60: "Washing out",
}

PARAMETER_LANGUAGES: dict[int, str] = {
    1: "German",
    2: "English",
    3: "French",
    4: "Italian",
    5: "Dutch",
    6: "Spanish",
    7: "Russian",
    9: "Danish",
}

PARAMETER_LED_MODES: dict[int, str] = {
    0: "Deactivated",
    1: "Permanent lightning",
    2: "In case of failure",
    3: "In case of operation by user + failure",
    4: "In case of water treatment + operation by user + failure",
}
