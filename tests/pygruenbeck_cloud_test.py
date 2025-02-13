"""Test for pygruenbeck_cloud."""

from __future__ import annotations

import datetime
import json
from unittest.mock import patch

import aiohttp
from aiohttp import ClientSession, CookieJar, web
import pytest

from pygruenbeck_cloud import PyGruenbeckCloud
from pygruenbeck_cloud.const import (
    PARAM_NAME_DEVICE_ID,
    PARAM_NAME_ENDPOINT,
    PARAM_NAME_PASSWORD,
    PARAM_NAME_TENANT,
    PARAM_NAME_USERNAME,
    WEB_REQUESTS,
)
from pygruenbeck_cloud.models import GruenbeckAuthToken

from tests.conftest import FakeApi


@patch("pygruenbeck_cloud.const.WEB_REQUESTS")
@pytest.mark.asyncio
async def test_login(
    mock_request,
    aiohttp_server: any,
    fake_api: FakeApi,
):
    """Test login with patch"""
    # From request 1
    tenant = {
        PARAM_NAME_TENANT: "/a50d35c1-202f-4da7-aa87-76e51a3098c6/B2C_1A_SignInUp"
    }
    username = "fake@mail.com"
    password = "fakepassword"

    async def handler_step_1(request: web.Request) -> web.Response:
        req1 = WEB_REQUESTS["login_step_1"]["path"]
        if request.path == req1:
            return web.Response(
                body=fake_api.login_step_1_response(),
                headers=fake_api.login_step_1_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    async def handler_step_2(request: web.Request) -> web.Response:
        data = await request.post()
        data_values = {
            PARAM_NAME_USERNAME: username,
            PARAM_NAME_PASSWORD: password,
        }
        for key, value in WEB_REQUESTS["login_step_2"]["data"].items():
            if key not in data.keys() or data[key] != value.format(**data_values):
                assert False, f"Incorrect value for {key} parameter: {value}"

        # Check if cookies are set
        # print("Headers: ")
        # print(request.headers)
        # print("Cookies: ")
        # print(request.cookies)

        req2 = WEB_REQUESTS["login_step_2"]["path"].format(**tenant)
        if request.path == req2:
            return web.Response(
                text=fake_api.login_step_2_response(),
                headers=fake_api.login_step_2_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    async def handler_step_3(request: web.Request) -> web.Response:
        req3 = WEB_REQUESTS["login_step_3"]["path"].format(**tenant)
        if request.path == req3:
            return web.Response(
                text=fake_api.login_step_3_response(),
                headers=fake_api.login_step_3_response_headers(),
                status=aiohttp.http.HTTPStatus.FOUND,
            )

        assert False, f"Incorrect path requested {request.path}"

    async def handler_step_4(request: web.Request) -> web.Response:
        req4 = WEB_REQUESTS["login_step_4"]["path"].format(**tenant)
        if request.path == req4:
            return web.Response(
                text=fake_api.login_step_4_response(),
                headers=fake_api.login_step_4_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    app = web.Application()
    app.add_routes(
        [
            getattr(web, WEB_REQUESTS["login_step_1"]["method"].lower())(
                WEB_REQUESTS["login_step_1"]["path"], handler_step_1
            ),
            getattr(web, WEB_REQUESTS["login_step_2"]["method"].lower())(
                WEB_REQUESTS["login_step_2"]["path"].format(**tenant), handler_step_2
            ),
            getattr(web, WEB_REQUESTS["login_step_3"]["method"].lower())(
                WEB_REQUESTS["login_step_3"]["path"].format(**tenant), handler_step_3
            ),
            getattr(web, WEB_REQUESTS["login_step_4"]["method"].lower())(
                WEB_REQUESTS["login_step_4"]["path"].format(**tenant), handler_step_4
            ),
        ]
    )

    server = await aiohttp_server(app)

    # Overwrite server values
    return_value = WEB_REQUESTS
    return_value["login_step_1"]["scheme"] = "http"
    return_value["login_step_1"]["host"] = f"{server.host}"
    return_value["login_step_1"]["port"] = int(f"{server.port}")
    return_value["login_step_2"]["scheme"] = "http"
    return_value["login_step_2"]["host"] = f"{server.host}"
    return_value["login_step_2"]["port"] = int(f"{server.port}")
    return_value["login_step_3"]["scheme"] = "http"
    return_value["login_step_3"]["host"] = f"{server.host}"
    return_value["login_step_3"]["port"] = int(f"{server.port}")
    return_value["login_step_4"]["scheme"] = "http"
    return_value["login_step_4"]["host"] = f"{server.host}"
    return_value["login_step_4"]["port"] = int(f"{server.port}")
    mock_request.return_value = return_value

    fake_api.domain = f"{server.host}:{server.port}"

    gruenbeck = PyGruenbeckCloud(
        username=username,
        password=password,
    )
    gruenbeck.session = ClientSession(
        cookie_jar=CookieJar(
            unsafe=True, treat_as_secure_origin=f"http://{fake_api.domain}"
        )
    )

    result = await gruenbeck.login()
    assert result is True, "Error login into GruenbeckCloud"

    await server.close()


# get_diagnostics
@patch("pygruenbeck_cloud.const.WEB_REQUESTS")
@pytest.mark.asyncio
async def test_get_devices(
    mock_request,
    aiohttp_server: any,
    fake_api: FakeApi,
):
    """Test get_devices Method"""
    username = "fake@mail.com"
    password = "fakepassword"

    fake_response = fake_api.get_devices_response()

    async def handler_get_devices(request: web.Request) -> web.Response:
        req1 = WEB_REQUESTS["get_devices"]["path"]
        if request.path == req1:
            return web.Response(
                body=fake_response,
                headers=fake_api.get_devices_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    app = web.Application()
    app.add_routes(
        [
            getattr(web, WEB_REQUESTS["get_devices"]["method"].lower())(
                WEB_REQUESTS["get_devices"]["path"], handler_get_devices
            ),
        ]
    )

    server = await aiohttp_server(app)

    # Overwrite server values
    return_value = WEB_REQUESTS
    return_value["get_devices"]["scheme"] = "http"
    return_value["get_devices"]["host"] = f"{server.host}"
    return_value["get_devices"]["port"] = int(f"{server.port}")
    mock_request.return_value = return_value

    fake_api.domain = f"{server.host}:{server.port}"

    gruenbeck = PyGruenbeckCloud(
        username=username,
        password=password,
    )
    gruenbeck._auth_token = GruenbeckAuthToken(
        access_token="access_token",
        refresh_token="refresh_token",
        not_before=datetime.datetime.now(),
        expires_on=(datetime.datetime.now() + datetime.timedelta(hours=5)),
        expires_in=(5 * 60 * 60),
        tenant="tenant",
    )

    devices = await gruenbeck.get_devices()
    fake_response_json = json.loads(fake_response)
    assert len(devices) == len(fake_response_json), "Incorrect number of devices"
    for i, expected in enumerate(fake_response_json):
        assert devices[i].type == expected["type"], "Incorrect device type"
        assert devices[i].has_error == expected["hasError"], "Incorrect device hasError"
        assert devices[i].id == expected["id"], "Incorrect device id"
        assert devices[i].series == expected["series"], "Incorrect device series"
        assert (
            devices[i].serial_number == expected["serialNumber"]
        ), "Incorrect device serialNumber"
        assert devices[i].name == expected["name"], "Incorrect device name"
        assert devices[i].register == expected["register"], "Incorrect device register"


@patch("pygruenbeck_cloud.const.WEB_REQUESTS")
@pytest.mark.asyncio
async def test_set_device(
    mock_request,
    aiohttp_server: any,
    fake_api: FakeApi,
):
    """Test set_device Method"""
    username = "fake@mail.com"
    password = "fakepassword"

    fake_response = fake_api.get_device_infos_response()
    fake_device = fake_api.fake_device()

    async def handler_get_devices(request: web.Request) -> web.Response:
        req1 = WEB_REQUESTS["get_devices"]["path"]
        if request.path == req1:
            return web.Response(
                body=fake_api.get_devices_response(),
                headers=fake_api.get_devices_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    async def handler_get_device_infos_request(request: web.Request) -> web.Response:
        req1 = PyGruenbeckCloud._placeholder_to_values_str(
            WEB_REQUESTS["get_device_infos_request"]["path"],
            {
                PARAM_NAME_DEVICE_ID: fake_device.id,
                PARAM_NAME_ENDPOINT: "",
            },
        )
        if request.path == req1:
            return web.Response(
                body=fake_response,
                headers=fake_api.get_device_infos_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    app = web.Application()
    app.add_routes(
        [
            getattr(web, WEB_REQUESTS["get_devices"]["method"].lower())(
                WEB_REQUESTS["get_devices"]["path"], handler_get_devices
            ),
            getattr(web, WEB_REQUESTS["get_device_infos_request"]["method"].lower())(
                PyGruenbeckCloud._placeholder_to_values_str(
                    WEB_REQUESTS["get_device_infos_request"]["path"],
                    {
                        PARAM_NAME_DEVICE_ID: fake_device.id,
                        PARAM_NAME_ENDPOINT: "",
                    },
                ),
                handler_get_device_infos_request,
            ),
        ]
    )

    server = await aiohttp_server(app)

    # Overwrite server values
    return_value = WEB_REQUESTS
    return_value["get_devices"]["scheme"] = "http"
    return_value["get_devices"]["host"] = f"{server.host}"
    return_value["get_devices"]["port"] = int(f"{server.port}")
    return_value["get_device_infos_request"]["scheme"] = "http"
    return_value["get_device_infos_request"]["host"] = f"{server.host}"
    return_value["get_device_infos_request"]["port"] = int(f"{server.port}")
    mock_request.return_value = return_value

    fake_api.domain = f"{server.host}:{server.port}"

    gruenbeck = PyGruenbeckCloud(
        username=username,
        password=password,
    )
    gruenbeck._auth_token = GruenbeckAuthToken(
        access_token="access_token",
        refresh_token="refresh_token",
        not_before=datetime.datetime.now(),
        expires_on=(datetime.datetime.now() + datetime.timedelta(hours=5)),
        expires_in=(5 * 60 * 60),
        tenant="tenant",
    )

    result = await gruenbeck.set_device_from_id(fake_device.id)
    assert result is True, "Unable to set device by ID"


@patch("pygruenbeck_cloud.const.WEB_REQUESTS")
@pytest.mark.asyncio
async def test_get_device_se(
    mock_request,
    aiohttp_server: any,
    fake_api: FakeApi,
):
    """Test set_device Method"""
    username = "fake@mail.com"
    password = "fakepassword"

    fake_response = fake_api.get_device_infos_se_response()
    fake_device = fake_api.fake_device("SE")

    async def handler_get_devices(request: web.Request) -> web.Response:
        req1 = WEB_REQUESTS["get_devices"]["path"]
        if request.path == req1:
            return web.Response(
                body=fake_api.get_devices_response(),
                headers=fake_api.get_devices_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    async def handler_get_device_infos_se_request(request: web.Request) -> web.Response:
        req1 = PyGruenbeckCloud._placeholder_to_values_str(
            WEB_REQUESTS["get_device_infos_request"]["path"],
            {
                PARAM_NAME_DEVICE_ID: fake_device.id,
                PARAM_NAME_ENDPOINT: "",
            },
        )
        if request.path == req1:
            return web.Response(
                body=fake_response,
                headers=fake_api.get_device_infos_se_response_headers(),
                status=200,
            )

        assert False, f"Incorrect path requested {request.path}"

    app = web.Application()
    app.add_routes(
        [
            getattr(web, WEB_REQUESTS["get_devices"]["method"].lower())(
                WEB_REQUESTS["get_devices"]["path"], handler_get_devices
            ),
            getattr(web, WEB_REQUESTS["get_device_infos_request"]["method"].lower())(
                PyGruenbeckCloud._placeholder_to_values_str(
                    WEB_REQUESTS["get_device_infos_request"]["path"],
                    {
                        PARAM_NAME_DEVICE_ID: fake_device.id,
                        PARAM_NAME_ENDPOINT: "",
                    },
                ),
                handler_get_device_infos_se_request,
            ),
        ]
    )

    server = await aiohttp_server(app)

    # Overwrite server values
    return_value = WEB_REQUESTS
    return_value["get_devices"]["scheme"] = "http"
    return_value["get_devices"]["host"] = f"{server.host}"
    return_value["get_devices"]["port"] = int(f"{server.port}")
    return_value["get_device_infos_request"]["scheme"] = "http"
    return_value["get_device_infos_request"]["host"] = f"{server.host}"
    return_value["get_device_infos_request"]["port"] = int(f"{server.port}")
    mock_request.return_value = return_value

    fake_api.domain = f"{server.host}:{server.port}"

    gruenbeck = PyGruenbeckCloud(
        username=username,
        password=password,
    )
    gruenbeck._auth_token = GruenbeckAuthToken(
        access_token="access_token",
        refresh_token="refresh_token",
        not_before=datetime.datetime.now(),
        expires_on=(datetime.datetime.now() + datetime.timedelta(hours=5)),
        expires_in=(5 * 60 * 60),
        tenant="tenant",
    )

    await gruenbeck.get_devices()
    result = await gruenbeck.set_device_from_id(fake_device.id)
    assert result is True, "Unable to set device by ID"
