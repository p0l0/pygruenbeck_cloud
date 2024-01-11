"""pygruenbeck_cloud is a Python library to communicate with the Grünbeck Cloud based Water softeners."""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import logging
import random
import socket
from datetime import datetime, timedelta
from types import TracebackType
from typing import Any

import aiohttp
from aiohttp import ClientSession, ClientTimeout, CookieJar, ClientWebSocketResponse, \
    ContentTypeError, ClientConnectorError, ServerDisconnectedError, \
    WSServerHandshakeError, ClientConnectionError, WSMsgType
from yarl import URL

from collections.abc import Callable

from .const import API_WS_HOST, API_WS_CLIENT_URL, API_WS_CLIENT_QUERY, \
    LOGIN_CODE_CHALLENGE_CHARS, LOGIN_HOST, \
    LOGIN_SCHEME, PARAM_NAME_CODE_CHALLENGE, HTTP_REQUEST_TIMEOUT, \
    PARAM_NAME_CSRF_TOKEN, PARAM_NAME_TENANT, PARAM_NAME_TRANS_ID, PARAM_NAME_POLICY, \
    PARAM_NAME_USERNAME, PARAM_NAME_PASSWORD, PARAM_NAME_CODE, \
    PARAM_NAME_CODE_VERIFIER, UPDATE_INTERVAL, WEB_REQUESTS, PARAM_NAME_REFRESH_TOKEN, \
    PARAM_NAME_ACCESS_TOKEN, API_WS_SCHEME_WS, PARAM_NAME_CONNECTION_ID, \
    API_WS_CLIENT_HEADER, API_WS_INITIAL_MESSAGE, WS_REQUEST_TIMEOUT, \
    PARAM_NAME_DEVICE_ID, PARAM_NAME_ENDPOINT, API_GET_MG_INFOS_ENDPOINT, \
    API_GET_MG_INFOS_ENDPOINT_PARAMETERS, API_GET_MG_INFOS_ENDPOINT_SALT_MEASUREMENTS, \
    API_GET_MG_INFOS_ENDPOINT_WATER_MEASUREMENTS
from .exceptions import PyGruenbeckCloudInvalidResponseStatus, \
    PyGruenbeckCloudClientConnectionError
from .models import GruenbeckAuthToken, Device

# logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s", datefmt="%d/%b/%Y %H:%M:%S")
_LOGGER = logging.getLogger(__name__)

class PyGruenbeckCloud:
    """Class for communicate with the Grünbeck cloud."""

    _session: ClientSession | None = None
    _ws_session: ClientSession | None = None
    _ws_client: ClientWebSocketResponse | None = None
    _auth_token: GruenbeckAuthToken | None = None

    def __init__(self, username: str, password: str) -> None:
        """Initialize PyGruenbeckCloud Class."""
        self._username = username
        self._password = password

    async def login(self):
        """Login to Grünbeck Cloud."""
        code_verifier, code_challenge = await self._get_code_challenge()

        step1_values = await self._login_step1(code_challenge)
        _LOGGER.info(step1_values)

        step2_result = await self._login_step2(step1_values)
        if step2_result == False:
            _LOGGER.error("Error trying to log in!")
            return

        code = await self._login_step3(step1_values)

        response = await self._login_step4(step1_values, code, code_verifier)

        self._auth_token = GruenbeckAuthToken(
            access_token=response["access_token"],
            refresh_token=response["refresh_token"],
            not_before=datetime.fromtimestamp(response["not_before"]),
            expires_on=datetime.fromtimestamp(response["expires_on"]),
            expires_in=response["expires_in"],
            tenant=step1_values["tenant"],
        )

        # self._access_token = response["access_token"]
        # self._refresh_token = response["refresh_token"]
        # self._not_before = datetime.fromtimestamp(response["not_before"])
        # self._expires_on = datetime.fromtimestamp(response["expires_on"])
        # self._expires_in = response["expires_in"]

    def _placeholder_to_values_dict(self, const: dict[str, str], values: dict[str, str]) -> dict[str, str]:
        """Convert placeholder from dict Constant to Value."""
        result = {}
        for key, value in const.items():
            result[key] = value.format(**values)

        return result

    def _placeholder_to_values_str(self, const: str, values: dict[str, str]) -> str:
        """Convert placeholder from str Constant to Value"""
        return const.format(**values)

    async def _login_step1(self, code_challenge: str) -> dict[str, str]:
        scheme = WEB_REQUESTS["login_step_1"]["scheme"]
        host = WEB_REQUESTS["login_step_1"]["host"]

        headers = WEB_REQUESTS["login_step_1"]["headers"]
        path = WEB_REQUESTS["login_step_1"]["path"]
        method = WEB_REQUESTS["login_step_1"]["method"]
        data = WEB_REQUESTS["login_step_1"]["data"]

        query = self._placeholder_to_values_dict(WEB_REQUESTS["login_step_1"]["query_params"], {
            PARAM_NAME_CODE_CHALLENGE: code_challenge
        })

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Login Step 1: {url}")
        response = await self._http_request(url=url, headers=headers, method=method, data=data)
        _LOGGER.debug(f"Response Login Step 1: {response}")

        return {
            "csrf_token": self._extract_from_html_response(response=response, str="csrf"),
            "transId": self._extract_from_html_response(response=response, str="transId"),
            "policy": self._extract_from_html_response(response=response, str="policy"),
            "tenant": self._extract_from_html_response(response=response, str="tenant"),
        }

    async def _login_step2(self, step1_values: dict[str, str]) -> bool:
        scheme = WEB_REQUESTS["login_step_2"]["scheme"]
        host = WEB_REQUESTS["login_step_2"]["host"]

        headers = self._placeholder_to_values_dict(WEB_REQUESTS["login_step_2"]["headers"],
                                                   {PARAM_NAME_CSRF_TOKEN: step1_values["csrf_token"]})

        path = self._placeholder_to_values_str(WEB_REQUESTS["login_step_2"]["path"],
                                                {PARAM_NAME_TENANT: step1_values["tenant"]})

        data = self._placeholder_to_values_dict(WEB_REQUESTS["login_step_2"]["data"],
                                                {
                                                    PARAM_NAME_USERNAME: self._username,
                                                    PARAM_NAME_PASSWORD: self._password,
                                                })

        method = WEB_REQUESTS["login_step_1"]["method"]

        query = self._placeholder_to_values_dict(WEB_REQUESTS["login_step_2"]["query_params"],
                                                 {
            PARAM_NAME_TRANS_ID: step1_values["transId"],
            PARAM_NAME_POLICY: step1_values["policy"],
        })

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Login Step 2: {url}")
        response = await self._http_request(url=url, headers=headers, method=method, data=data)
        _LOGGER.debug(f"Response Login Step 2: {response}")

        if "status" in response:
            if isinstance(response, str):
                response = json.loads(response)

            if response["status"] == "200":
                return True

        return False

    async def _login_step3(self, step1_values: dict[str, str]) -> str:
        scheme = WEB_REQUESTS["login_step_3"]["scheme"]
        host = WEB_REQUESTS["login_step_3"]["host"]

        headers = WEB_REQUESTS["login_step_3"]["headers"]
        path = self._placeholder_to_values_str(WEB_REQUESTS["login_step_3"]["path"], {PARAM_NAME_TENANT: step1_values["tenant"]})
        method = WEB_REQUESTS["login_step_3"]["method"]
        data = WEB_REQUESTS["login_step_3"]["data"]

        query = self._placeholder_to_values_dict(WEB_REQUESTS["login_step_3"]["query_params"],
                                                 {
            PARAM_NAME_CSRF_TOKEN: step1_values["csrf_token"],
            PARAM_NAME_TRANS_ID: step1_values["transId"],
            PARAM_NAME_POLICY: step1_values["policy"],
        })

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Login Step 3: {url}")
        # @TODO - expected_status_code and allow_redirects can also come from CONST!
        response = await self._http_request(url=url, headers=headers, method=method, data=data, expected_status_code=aiohttp.http.HTTPStatus.FOUND, allow_redirects=False)
        _LOGGER.debug(f"Response Login Step 3: {response}")

        start = response.index("code%3d") + 7
        end = response.index(">here") - 1
        return response[start:end]

    async def _login_step4(self, step1_values, code, code_verifier) -> dict[str, Any]:
        scheme = WEB_REQUESTS["login_step_4"]["scheme"]
        host = WEB_REQUESTS["login_step_4"]["host"]

        headers = WEB_REQUESTS["login_step_4"]["headers"]
        path = self._placeholder_to_values_str(WEB_REQUESTS["login_step_4"]["path"], {
            PARAM_NAME_TENANT: step1_values["tenant"]})
        method = WEB_REQUESTS["login_step_4"]["method"]
        data = self._placeholder_to_values_dict(WEB_REQUESTS["login_step_4"]["data"],
{
            PARAM_NAME_CODE: code,
            PARAM_NAME_CODE_VERIFIER: code_verifier
        })
        query = WEB_REQUESTS["login_step_4"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Login Step 4: {url}")
        response = await self._http_request(url=url, headers=headers, method=method, data=data)
        _LOGGER.debug(f"Response Login Step 4: {response}")

        return response


    def _extract_from_html_response(self, response: str, str: str, sep: str = ",") -> str:
        """Retrieve str from HTML response."""
        start = response.index(str) + len(str) + 3
        end = response.index(sep, start) - 1

        return response[start:end]

    async def _http_request(self, headers: dict, url: StrOrURL, data: Any = None, expected_status_code: int = aiohttp.http.HTTPStatus.OK, method: str = aiohttp.hdrs.METH_GET, allow_redirects: bool = False) -> str | dict[Any, Any]:  # type: ignore[no-any-return]  # noqa: E501
        """Execute HTTP request."""
        if self._session is None:
            self._session = ClientSession(timeout=ClientTimeout(total=HTTP_REQUEST_TIMEOUT),
                                cookie_jar=CookieJar())

        try:
            async with self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    allow_redirects=allow_redirects,
                    data=data,
            ) as resp:
                if resp.status != expected_status_code:
                    error = f"Incorrect status code received {resp.status}"
                    _LOGGER.error(error)
                    # await session.close()
                    raise PyGruenbeckCloudInvalidResponseStatus(error)
                _LOGGER.info(f"Response headers are: {resp.headers}")
                _LOGGER.info(f"Content-type is: {resp.headers.get('content-type')}")
                try:
                    response = await resp.json()
                except ContentTypeError:
                    response = await resp.text()

                # await session.close()
                return response
        except (ClientConnectorError, ServerDisconnectedError) as ex:
            _LOGGER.error("%s", ex)
            # await session.close()
            raise PyGruenbeckCloudClientConnectionError(ex) from ex

    @property
    def connected(self) -> bool:
        """Return if we are connected to WebSocket."""
        return self._ws_client is not None and not self._ws_client.closed

    async def connect(self) -> None:
        """Connect to the WebSocket."""
        if self.connected:
            return

        _LOGGER.debug("Start getting WS Tokens...")
        ws_access_token, ws_connection_id = await self._get_ws_tokens()
        _LOGGER.debug(f"Got WS Tokens: access_token {ws_access_token} and connection_id {ws_connection_id}")

        query = self._placeholder_to_values_dict(API_WS_CLIENT_QUERY, {
            PARAM_NAME_CONNECTION_ID: ws_connection_id,
            PARAM_NAME_ACCESS_TOKEN: ws_access_token
        })
        url = URL.build(scheme=API_WS_SCHEME_WS, host=API_WS_HOST, path=API_WS_CLIENT_URL, query=query)

        if self._ws_session is None:
            self._ws_session = ClientSession(timeout=ClientTimeout(total=WS_REQUEST_TIMEOUT))

        try:
            self._ws_client = await self._ws_session.ws_connect(url=url, headers=API_WS_CLIENT_HEADER, heartbeat=30)
            await self._ws_client.send_str(API_WS_INITIAL_MESSAGE)
        except (
            WSServerHandshakeError,
            ClientConnectionError,
            socket.gaierror,
        ) as ex:
            raise PyGruenbeckCloudClientConnectionError(ex) from ex

    async def listen(self, callback: Callable[str]) -> None:
        if not self._ws_client or not self.connected:
            raise Exception("We are not connected to WS!")

        while not self._ws_client.closed:
            msg = await self._ws_client.receive()
            _LOGGER.info(f"WS Message: {msg.data}")

            if msg.type == WSMsgType.ERROR:
                raise Exception("Websocket ERROR!")

            if msg.type == WSMsgType.TEXT:
                callback(msg.data)

            if msg.type == WSMsgType.BINARY:
                raise Exception("Got binary message!")

            if msg.type in (
                WSMsgType.CLOSE,
                WSMsgType.CLOSED,
                WSMsgType.CLOSING
            ):
                raise Exception("Websocket connection was closed!")


    async def get_devices(self) -> list[Device]:
        """Get Devices from Cloud."""
        devices: list[Device] = []

        token = await self._get_web_access_token()

        scheme = WEB_REQUESTS["get_devices"]["scheme"]
        host = WEB_REQUESTS["get_devices"]["host"]

        headers = self._placeholder_to_values_dict(WEB_REQUESTS["get_devices"]["headers"],
                                                   {
                                                       PARAM_NAME_ACCESS_TOKEN: token,
                                                   })
        path = WEB_REQUESTS["get_devices"]["path"]
        method = WEB_REQUESTS["get_devices"]["method"]
        data = WEB_REQUESTS["get_devices"]["data"]
        query = WEB_REQUESTS["get_devices"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Get Devices: {url}")
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data)
        _LOGGER.debug(f"Response Get Devices: {response}")

        for device in response:
            if "soft" in device["id"]:
                print(device)
                devices.append(Device.from_dict(device))

        return devices

    async def get_mg_infos(self, device: Device):
        data = await self._get_mg_infos_request(device, API_GET_MG_INFOS_ENDPOINT)

    async def get_mg_infos_parameters(self, device: Device):
        data = await self._get_mg_infos_request(device, API_GET_MG_INFOS_ENDPOINT_PARAMETERS)

    async def get_mg_infos_salt_measurements(self, device: Device):
        data = await self._get_mg_infos_request(device, API_GET_MG_INFOS_ENDPOINT_SALT_MEASUREMENTS)

    async def get_mg_infos_water_measurements(self, device: Device):
        data = await self._get_mg_infos_request(device, API_GET_MG_INFOS_ENDPOINT_WATER_MEASUREMENTS)

    async def _get_mg_infos_request(self, device: Device, endpoint: str = ""):
        """Get MG Infos from API."""
        token = await self._get_web_access_token()

        scheme = WEB_REQUESTS["get_mg_infos_request"]["scheme"]
        host = WEB_REQUESTS["get_mg_infos_request"]["host"]

        headers = self._placeholder_to_values_dict(
            WEB_REQUESTS["get_mg_infos_request"]["headers"],
            {
                PARAM_NAME_ACCESS_TOKEN: token,
            })
        path = self._placeholder_to_values_str(WEB_REQUESTS["get_mg_infos_request"]["path"], {
            PARAM_NAME_DEVICE_ID: device.id,
            PARAM_NAME_ENDPOINT: endpoint,
        })
        method = WEB_REQUESTS["get_mg_infos_request"]["method"]
        data = WEB_REQUESTS["get_mg_infos_request"]["data"]
        query = WEB_REQUESTS["get_mg_infos_request"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Get MG Infos: {url}")
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data)
        _LOGGER.debug(f"Response Get MG Infos: {response}")

        return response

    async def enter_sd(self, device: Device):
        """Send enter SD for WS."""
        token = await self._get_web_access_token()

        scheme = WEB_REQUESTS["enter_sd"]["scheme"]
        host = WEB_REQUESTS["enter_sd"]["host"]

        headers = self._placeholder_to_values_dict(WEB_REQUESTS["enter_sd"]["headers"], {
            PARAM_NAME_ACCESS_TOKEN: token,
        })
        path = self._placeholder_to_values_str(WEB_REQUESTS["enter_sd"]["path"], {
            PARAM_NAME_DEVICE_ID: device.id})
        method = WEB_REQUESTS["enter_sd"]["method"]
        data = WEB_REQUESTS["enter_sd"]["data"]
        query = WEB_REQUESTS["enter_sd"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Enter SD: {url}")
        # @TODO - expected_status_code and allow_redirects can also come from CONST!
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data, expected_status_code=202)
        _LOGGER.debug(f"Response Enter SD: {response}")

        return response

    async def refresh_sd(self, device: Device):
        """Send refresh SD for WS."""
        token = await self._get_web_access_token()

        scheme = WEB_REQUESTS["refresh_sd"]["scheme"]
        host = WEB_REQUESTS["refresh_sd"]["host"]

        headers = self._placeholder_to_values_dict(WEB_REQUESTS["refresh_sd"]["headers"],
                                                   {
                                                       PARAM_NAME_ACCESS_TOKEN: token,
                                                   })
        path = self._placeholder_to_values_str(WEB_REQUESTS["refresh_sd"]["path"], {
            PARAM_NAME_DEVICE_ID: device.id})
        method = WEB_REQUESTS["refresh_sd"]["method"]
        data = WEB_REQUESTS["refresh_sd"]["data"]
        query = WEB_REQUESTS["refresh_sd"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Refresh SD: {url}")
        # @TODO - expected_status_code and allow_redirects can also come from CONST!
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data, expected_status_code=202)
        _LOGGER.debug(f"Response Refresh SD: {response}")

        return response

    async def leave_sd(self, device: Device):
        """Send leave SD for WS."""
        token = await self._get_web_access_token()

        scheme = WEB_REQUESTS["leave_sd"]["scheme"]
        host = WEB_REQUESTS["leave_sd"]["host"]

        headers = self._placeholder_to_values_dict(
            WEB_REQUESTS["leave_sd"]["headers"],
            {
                PARAM_NAME_ACCESS_TOKEN: token,
            })
        path = self._placeholder_to_values_str(WEB_REQUESTS["leave_sd"]["path"], {
            PARAM_NAME_DEVICE_ID: device.id})
        method = WEB_REQUESTS["leave_sd"]["method"]
        data = WEB_REQUESTS["leave_sd"]["data"]
        query = WEB_REQUESTS["leave_sd"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request Leave SD: {url}")
        # @TODO - expected_status_code and allow_redirects can also come from CONST!
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data, expected_status_code=202)
        _LOGGER.debug(f"Response Leave SD: {response}")

        return response

    async def disconnect(self) -> None:
        """Closes open connections."""
        if not self._ws_session or not self.connected:
            return

        await self._ws_session.close()

    async def _get_ws_tokens(self) -> list[str]:
        """Get new WebSocket tokens."""
        _LOGGER.debug("Start requesting web acesss tokens")
        web_access_token = await self._get_web_access_token()
        _LOGGER.debug(f"Got following access_token: {web_access_token}")

        ws_url, ws_access_token = await self._start_ws_negotiation(access_token=web_access_token)
        ws_connection_id = await self._get_ws_connection_id(ws_access_token=ws_access_token)

        return [ws_access_token, ws_connection_id]


    async def _start_ws_negotiation(self, access_token: str) -> list[str]:
        _LOGGER.debug("Start ws Negotiation")
        scheme = WEB_REQUESTS["start_ws_negotiation"]["scheme"]
        _LOGGER.debug(f"WS Negotiation Scheme is {scheme}")
        host = WEB_REQUESTS["start_ws_negotiation"]["host"]
        _LOGGER.debug(f"WS Negotiation Host is {host}")

        headers = self._placeholder_to_values_dict(WEB_REQUESTS["start_ws_negotiation"]["headers"],
                                                   {PARAM_NAME_ACCESS_TOKEN: access_token})
        _LOGGER.debug(f"WS Negotiation Headers are {headers}")
        path = WEB_REQUESTS["start_ws_negotiation"]["path"]
        _LOGGER.debug(f"WS Negotiation Path is {path}")
        method = WEB_REQUESTS["start_ws_negotiation"]["method"]
        _LOGGER.debug(f"WS Negotiation Method is {method}")
        data = WEB_REQUESTS["start_ws_negotiation"]["data"]
        _LOGGER.debug(f"WS Negotiation Data is {data}")

        query = WEB_REQUESTS["start_ws_negotiation"]["query_params"]
        _LOGGER.debug(f"WS Negotiation Query params are {query}")

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request WS Negotiation Start: {url}")
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data)
        _LOGGER.debug(f"Response WS Negotiation Start: {response}")
        return [response["url"], response["accessToken"]]

    async def _get_ws_connection_id(self, ws_access_token: str) -> str:
        scheme = WEB_REQUESTS["get_ws_connection_id"]["scheme"]
        host = WEB_REQUESTS["get_ws_connection_id"]["host"]

        headers = self._placeholder_to_values_dict(
            WEB_REQUESTS["get_ws_connection_id"]["headers"],
            {PARAM_NAME_ACCESS_TOKEN: ws_access_token})
        path = WEB_REQUESTS["get_ws_connection_id"]["path"]
        method = WEB_REQUESTS["get_ws_connection_id"]["method"]
        data = WEB_REQUESTS["get_ws_connection_id"]["data"]

        query = WEB_REQUESTS["get_ws_connection_id"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        _LOGGER.debug(f"Request WS get connection ID: {url}")
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data)
        _LOGGER.debug(f"Response WS get connection ID: {response}")

        return response["connectionId"]

    async def _get_web_access_token(self) -> str:
        """Get current WebSocket token."""
        if not self._auth_token:
            await self.login()

        """Refreshes the token if needed"""
        if not self._auth_token.is_expired():
            return self._auth_token.access_token

        refresh = await self._refresh_web_token()
        if refresh == False:
            _LOGGER.info("Unable to refresh token, need to relogin.")
            await self.login()

        return self._auth_token.access_token

    async def _refresh_web_token(self) -> bool:
        scheme = WEB_REQUESTS["web_token_refresh"]["scheme"]
        host = WEB_REQUESTS["web_token_refresh"]["host"]

        headers = WEB_REQUESTS["web_token_refresh"]["headers"]
        path = self._placeholder_to_values_str(WEB_REQUESTS["web_token_refresh"]["path"], {
            PARAM_NAME_TENANT: self._auth_token.tenant})
        method = WEB_REQUESTS["web_token_refresh"]["method"]
        data = self._placeholder_to_values_dict(WEB_REQUESTS["web_token_refresh"]["data"],
                                                {
                                                    PARAM_NAME_REFRESH_TOKEN: self._auth_token.refresh_token,
                                                })
        query = WEB_REQUESTS["web_token_refresh"]["query_params"]

        url = URL.build(scheme=scheme, host=host, path=path, query=query)
        response = await self._http_request(url=url, headers=headers, method=method,
                                            data=data)

        # @TODO - Check response if token is expired!

        self._auth_token.access_token = response["access_token"]
        self._auth_token.refresh_token = response["refresh_token"]
        self._auth_token.not_before = datetime.fromtimestamp(response["not_before"])
        self._auth_token.expires_on = datetime.fromtimestamp(response["expires_on"])
        self._auth_token.expires_in = response["expires_in"]

        return True


    async def _get_code_challenge(self) -> list[str]:
        """Get Grünbeck Cloud Code Challenge."""
        challenge_hash = ""
        result = ""

        while (challenge_hash == "" or "+" in challenge_hash or "/" in challenge_hash or "=" in challenge_hash or "+" in result or "/" in result):
            result = "".join(random.choice(LOGIN_CODE_CHALLENGE_CHARS) for _ in range(64))
            result = base64.b64encode(result.encode()).decode().rstrip("=")
            hash_object = hashlib.sha256(result.encode())
            challenge_hash = base64.b64encode(hash_object.digest()).decode()[:-1]

        return [result, challenge_hash]

    async def close(self):
        """Close all connections."""
        await self.disconnect()

        if self._session:
            await self._session.close()


    async def __aenter__(self) -> PyGruenbeckCloud:
        """Start PyGruenbeckCloud class from context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Stop PyGruenbeckCloud class from context manager."""
        await self.close()