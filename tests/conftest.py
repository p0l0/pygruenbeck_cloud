"""Conftest for pygruenbeck_cloud."""

from __future__ import annotations

from dataclasses import dataclass
import os.path

from multidict import CIMultiDict
import pytest

from pygruenbeck_cloud.models import Device

DIR_NAME = os.path.dirname(__file__)


@dataclass
class FakeApi:
    """Class for Fake Grünbeck API."""

    domain: str = ""

    def login_step_1_response(self) -> str:
        """Fixture for login step 1 response."""
        with open(f"{DIR_NAME}/responses/login_step_1.txt", encoding="utf-8") as file:
            data = file.read()

        return data

    def login_step_1_response_headers(self) -> CIMultiDict:
        """Fixture for login step 1 response headers."""
        domain = self.domain
        return CIMultiDict(
            [
                ("Cache-Control", "no-store, must-revalidate, no-cache"),
                ("Content-Type", "text/html; charset=utf-8"),
                # "Content-Encoding": "gzip",
                ("Expires", "-1"),
                ("Vary", "Accept-Encoding"),
                ("x-ms-gateway-requestid", "ff412852-c391-4fdf-b156-c910c3156a06"),
                ("X-UA-Compatible", "IE=edge"),
                ("X-Request-ID", "a3e25dda-0371-43d8-8fd9-5ab94c244d53"),
                ("X-Build", "1.1.22.0"),
                (
                    "Content-Security-Policy-Report-Only",
                    "script-src 'strict-dynamic' 'self' 'nonce-e437IoG78dDjCvfVt9mfsA==' 'report-sample'; report-uri /gruenbeckb2c.onmicrosoft.com/B2C_1A_SignInUp/client/cspreport?p=B2C_1A_SignInUp",
                ),
                ("X-Frame-Options", "DENY"),
                ("Public", "OPTIONS,TRACE,GET,HEAD,POST"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                ("X-Content-Type-Options", "nosniff"),
                ("X-XSS-Protection", "1; mode=block"),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-csrf=SWtMbFV3SS9QQUEvY2lBTGVpcytseWYxVVhqZTVxV2VvcWxFR2twQ0lWTWFhNVFYM1NvQmxISFRJbFNhRFNud1RvTWhYaG1mdDhqL0g1YlVsNUNCVkE9PTsyMDI0LTAxLTExVDIwOjMxOjI0LjA4NDM4MzFaO3kxd0pacitoUXpock5wTk5EMGNER0E9PTt7Ik9yY2hlc3RyYXRpb25TdGVwIjoxfQ==; domain={domain}; path=/; SameSite=None; HttpOnly",
                ),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-cache|2l3io3ed2eop2vq5tcrnuw_0=m1.m65ktdhVad9ELsbt.c30jho7MMmYIcNJICtGcvw==.0.+1qT2yw5nAnSsVs15klddvJUVJXYJyKQ72LWB+89Roag2UjsykCuzebhjaN485vNrjNdWhgo0qBOQVKWA0LWzDSNFNnPkgmCGVc0D9c/FgIXoOR8tSaP3LfVLgLErfAM4Pwu6eP3a7iIvyBtPlQk0OZSJKmMFFZnjuhYen8QFrHl2YuBfD+UBCy132zK/ygXiJ11kzrMTCPEP6J0TggRMwy8jSBqnnppAIC379DY+guvB7tVOtvfJMkdiJzFCryW86lkILpL65vCkZNp7FVOTqIhvBuSamLqFN4cqvnPAKdVnK7Fl7QuUeM9Bw0iqWieOJDu5xcHffd6qK/7F9ChhsCJSdJ25BY05clxJH1t1a2MbmkQKLzq5GE5gPzTHww59L+K5SkJ9QdZpPiCzSHcNUN7vtmMqAp1E3HPzlUgDv/ZRqe7iBTdfsJfJ4cTW/aAbgt73OE0uDCDezTMNKgjSWYnPyYXZak/vd3lyUPuzTLyxgjQsFsn1xBRLt7CTKvu3d8DTyJv7+Ist1awOKCPsRh/xvrLL5z6bgDxILtFXskFyMjy37wX9mpunG6nJU4LeNLq5Aw07CVAiaPWd8wmKzed8OkQwvnH0GHj2ZM7LomovC5OIqb3NEphzehMeozQ+IYfqhYV+V34HLt6oTf/9aNxoAZaGXA1ivFniNJT1X9XFhqfYWQcL8lmbj7e8hQX75tqkrmBSX4sFIuz/EKjQywjgMxuHL9ive+heTvibLndFqcDZoyontSLENgTev6HcdPSK/fd6xpOw0Eyokh24+N0OqVeeCe/fI8e6Vq7kPmnQx0W9V6tBeXPFVDsYYy8vpwCtCHQtOLeh3zY77IEX6VfqZ3FSGJg1na4MYzm/tI/3ZKFl7Xd+xhNgo3UJwy5a/O/C0eymmTDQ1/qN5uCy9aO2b6NuWPFq0kLn7gRPcdi4KTeFZYV3o2NhmF8JqmsX3k1zJRgWeL/GMx4fs8ZjK6WyfMz8Rj86exf54D8+7aTeXktlTd28fFnVdCn40BijgtRU9Wv6boKTMgIJucA7UlQWqgIs0i/+Mg=; domain={domain}; path=/; SameSite=None; HttpOnly",
                ),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-trans=eyJUX0RJQyI6W3siSSI6ImEzZTI1ZGRhLTAzNzEtNDNkOC04ZmQ5LTVhYjk0YzI0NGQ1MyIsIlQiOiJncnVlbmJlY2tiMmMub25taWNyb3NvZnQuY29tIiwiUCI6ImIyY18xYV9zaWduaW51cCIsIkMiOiI1YTgzY2MxNi1mZmIxLTQyZTktOTg1OS05ZmJmMDdmMzZkZjgiLCJTIjoxLCJNIjp7fSwiRCI6MCwiRSI6IiJ9XSwiQ19JRCI6ImEzZTI1ZGRhLTAzNzEtNDNkOC04ZmQ5LTVhYjk0YzI0NGQ1MyJ9; domain={domain}; path=/; SameSite=None; HttpOnly",
                ),
                ("Allow", "OPTIONS"),
                ("Allow", "TRACE"),
                ("Allow", "GET"),
                ("Allow", "HEAD"),
                ("Allow", "POST"),
            ]
        )

    def login_step_2_response(self):
        """Fixture for login step 2 response."""
        with open(f"{DIR_NAME}/responses/login_step_2.txt", encoding="utf-8") as file:
            data = file.read()

        return data

    def login_step_2_response_headers(self) -> CIMultiDict:
        """Fixture for login step 2 response headers."""
        domain = self.domain
        return CIMultiDict(
            [
                ("Cache-Control", "no-store, must-revalidate, no-cache"),
                ("Content-Type", "text/json; charset=utf-8"),
                # "Content-Encoding", "gzip",
                ("Vary", "Accept-Encoding"),
                ("x-ms-gateway-requestid", "fcf6945e-86ed-4a29-9adb-06f787189052"),
                ("X-Frame-Options", "DENY"),
                ("Public", "OPTIONS,TRACE,GET,HEAD,POST"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                ("X-Content-Type-Options", "nosniff"),
                ("X-XSS-Protection", "1; mode=block"),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-cache|2l3io3ed2eop2vq5tcrnuw_0=m1.ZzK81CE8VLsm/HTj.8rtNSyItDwtMAFLAUzSknQ==.0.SUiC698JBt+pFaaeoUIv01i6loE09LTodugdl6pAMVc6lr9uzot46ywByUlLIaWDQb7vJKhOFaLoimF6Z3JBQrRn2/NQCHRBYK63hBpHsdqWqQFeOybFPQGVpp6VcwdFxtdnW9AGjMINlTYa8PMzX6WRJVzXYcRuddrweUhz/RQCWqdhWJjWknKX23MnMGekzDpCfCigAT5ztn7/4I0mkkUXzCj7J4rSwmxZHn3G5fW8auH5iB5oIjnKLe05hU6tkx69+oT6BVhVJUyB1UvolFAaVzug0w12ZjfVYyM5fWxp5Q/wDov/zYHbGqbk2F9+0aE2ERGThFc60RVRm6chrmSn8Act0BP353H+Pzj0NY/BbOn1N6MwouuIgYrX4m1xo9vDuaoaRNg5pJDYX2qvLwjDWZ4O+UtLmjHCPIyGqa7RcBoo+Q35EOQ8f+ERY7lE+nSJ4QTZaKEDYKQIsyGB5KNKFPESX4HS7AtVp2sh0C6f1ziQDxxCMhTO75ymGMKfXFfmeveUPFINANUKfgtyjQO6WXi/DldB9KBksdPM6UUh2nbS6Q3n/9pDn/4GYilvmWfqVnmgi9KHFQMZa/zrgv+23o9QHlnZfNkuUrKgR+KQ5KxkIhiOksKpv5teYeCJWNp3N7FESuxC6HlX7qjU+ZjU5p0eTiNlbYtrR718o1tQQJCWBRVgfaQ+rbZCrvJpXrssAF0e73I0/0ofmzw5PjlBoAgUU4DdtSpAy8tWMjjlIclhaHLr0UGionRallheGsBBii9Ns1kkrC70ZLvsc+75v+L8NXnDbqmPAnRQCs0MeO+cx2w8OOdbM/X4Ot4NxlbLdsqcRRjvj1Yv0Cx4Pmta5j2jUMZiaHzxhdHdOvcmwufhFHp5O5/IqsMAwCjiPcZ7NSdbIP+KR/FHH0aXPw4u9E/puXLsvs6nnn3dk2kYfxpQ2CjaXxhRKTk4LLnuAyplSY+OB5Q8gGUhIy0JESbeiLJ21YrxsKw06XXoOn+CVMy0mZ4kTnzf4x1Mf/LEunfPjs3yMI5RnFsk2aE77XRk1TLdtVxyANRtRquTdGiTR3KGOP6IRusL/P+VD1Ybv6IeJF9tZntb7SqshNOJFzvvn2pq+kABW35EpP7IL9fEBF6Brqevtht0SbwfYRGy1ldqO8H2MNNooM7YXOp+rF2AqLC3TftxgaxJ6I/nYCeqKdL3OV8Qrv1F79fYTOYizsMSS4VQOAGNft64Syc=; domain={domain}; path=/; SameSite=None; HttpOnly",
                ),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-trans=eyJUX0RJQyI6W3siSSI6ImEzZTI1ZGRhLTAzNzEtNDNkOC04ZmQ5LTVhYjk0YzI0NGQ1MyIsIlQiOiJncnVlbmJlY2tiMmMub25taWNyb3NvZnQuY29tIiwiUCI6ImIyY18xYV9zaWduaW51cCIsIkMiOiI1YTgzY2MxNi1mZmIxLTQyZTktOTg1OS05ZmJmMDdmMzZkZjgiLCJTIjoyLCJNIjp7fSwiRCI6MCwiRSI6IiJ9XSwiQ19JRCI6ImEzZTI1ZGRhLTAzNzEtNDNkOC04ZmQ5LTVhYjk0YzI0NGQ1MyJ9; domain={domain}; path=/; SameSite=None; HttpOnly",
                ),
                ("Allow", "OPTIONS"),
                ("Allow", "TRACE"),
                ("Allow", "GET"),
                ("Allow", "HEAD"),
                ("Allow", "POST"),
            ]
        )

    def login_step_3_response(self):
        """Fixture for login step 3 response."""
        with open(f"{DIR_NAME}/responses/login_step_3.txt", encoding="utf-8") as file:
            data = file.read()

        return data

    def login_step_3_response_headers(self) -> CIMultiDict:
        """Fixture for login step 3 response headers."""
        domain = self.domain
        return CIMultiDict(
            [
                ("Cache-Control", "no-store, must-revalidate, no-cache"),
                ("Content-Type", "text/html; charset=utf-8"),
                (
                    "Location",
                    "msal5a83cc16-ffb1-42e9-9859-9fbf07f36df8://auth/?state=NjkyQjZBQTgtQkM1My00ODBDLTn3MkYtOTZCQ0QyQkQ2NEE5&trustFrameworkPolicy=B2C_1A_SignInUp&client_info=eyJ1aWQiOiIzODc2Yjk3Zi01NThhLTQ1YzUtOTRjNC1jNzAwOGI1YTdmYjYtYjJjXzFhX3NpZ25pbnVwIiwidXRpZCI6ImE1MGQzNWMxLTIwMmYtNGRhNy1hYTg3LTc2ZTUxYTMwOThjNiJ9&code=eyJraWQiOiJrdnp2djVnb2NQT0lEZF9HMkpEdmNLRXFaZ1lQTDV0U2lyejVNb1k3bm9FIiwidmVyIjoiMS4wIiwiemlwIjoiRGVmbGF0ZSIsInNlciI6IjEuMCJ9.M5WYAuLcfQZpS--fIWzGVl_NyzSNcPO-DQHhKXihvbj69KPAmAn1lV-YphSjCqmOt3ZVOYsnR38hAuo4xJnkfCYp_0id7o_W7PcCaHRuOlhYtNNrmLJ41hk7CmY3S5bCcfQ_TfDYG69IhRadsWwVg4PTRAhl0l7UAXD-aPFJR8P2ZcP1EygXUrN7F-kQ8IvkGb3GjhckLY0qeMG8V3UT4dKHs3YodvWt8eOO_pXNE1Fj3sYIJQYAeT8dsCnIVJuGlCwXUTS-vK-Ks7F-_kw4CrWd1RfwzWmUTrsOxLwtz2AeYZZSCf38C4xbA5N_mp_1Ppo_pBv4TbZGtlwdWpGs8A.0vI1GY94JfckUTS-.QY12LGxUY0JEEHeesRk-1Gv5efmhUCVijLBGhAhnC37C0PrwPmXZ_NkJCHFFiC_ekNXSTbt74t_fOcBa7QpY6hGFm18ssKa5IM1neWR1ZuS4PlR3Ln6L86I7H1vDd5GpHIQTQVGy_r4N9cwCgp2LM74VsxaHttkBt6OcHMqmPbi7ZwTlzxVjK6SWz-OU-C23zbgNR5vekZRAn2dBb1RN4En6zpdsY-AydMR31PSEJsDO_0pYlJJmUl8A3AhCQBSDnap5q-LF1wnbJsudeSWYZ7W4gRVl_UYIGyEMaV8iuz4fqU8FC5SmNxuNv_ZRpbdeiMfblFk4Nz3bIna3o06DW7hn2Zsti6Hl5hGseZQWrxELIKfW3cxEl1QaNaQm32PJQluZULQVPyOSdN80A4IABoNZ6RMsv6aM1N_ospfFdEbXnW0TIzvzJFgzB_tE-R1n_LPXEbmHZDS9EMoXAcFItxDF_-26XgnDQnI1YdO1gHST8m19fJGh_srg5S_9tMbBZ9WASUZxXSKqTLebPhiBaaYwH7SmON01lr0dBqWc33J03U4fYpl9E5lUV0CdiTEmqIWRy5-ne3Mw-1u3L-oeRCL2ifjdhIhIagOkdpzFYW2GqSwOf602_nk1rjCqLt6qzydx1ZwqAEfrapgAP_ASZJPEmAVL05jTfNctV17j1u12Knjwk5FeWKj53VPxhJ06KuLUQ2Zw2I6fVtSn0ucgZeywtxlcvoFQUyIQMuJNuTdfQTHlYHv0ClQ--ZJOVzxOFyPl0y9GyT47NaRP08x0_16Cdsw.Vf0ytsIdraOnIXZWNQyzEA",
                ),
                ("x-ms-gateway-requestid", "5960b578-3a98-4dd0-8984-71884a9c9ed2"),
                ("X-Frame-Options", "DENY"),
                ("Public", "OPTIONS,TRACE,GET,HEAD,POST"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                ("X-Content-Type-Options", "nosniff"),
                ("X-XSS-Protection", "1; mode=block"),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-sso:gruenbeckb2c.onmicrosoft.com_0=m1.Xv8OXEZ05e3qLcbX.4W6C0e4+p3bY3AaT1Fwf6A==.0.farsJsYESgSEEqbTam2Zd/1ncsT0+3whsLPJsO3WRK0Avw03DSmhDuK18Q5DzhuOllzeJGxtNJoQRPt06woT9lq7snhZZCLS2mPB8L4NhLrM/NvD1lQnOVUBmwQ18C9BIH5P+5K9fnl8sFg0DH1X+Vys/31YxSHsg7lpCXBpIIXvxAGnnxYgefwR75sVbQ7D0df6tStHsiXj7zmZrzLW4ax2gYE09zp5liz446I7A3gzgZZEn9nJtU90YaN5JfFOPEr4iauv8S5AyXN7umXtSJm/K5OIvmocYA3p7oPa4avPkLZDWdPZeaba9A8Xp5RSpc+4+cVKBe7OWw5g4iYzV7rVphwlmiUb4AAd0d9WmKPKPUA9YUZtblvPq+b1vdg6GM4Qcec+MB7sVFqsvplMlz+zVIpDvSf6RkssifMJhrcP2g47Enuna+Yj3+UbEjXakUexMxNomXhHEFVAueY/uzk602cw1zq+6qm7VL8ZDuS1GORAmxjDFu79BpluLojQ+ihLH6+naSHpLbjXZQgEzc7MT+ghfTfFkUWl; domain={domain}; path=/; SameSite=None; HttpOnly",
                ),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-cache|2l3io3ed2eop2vq5tcrnuw_0=; domain={domain}; expires=Sat, 11-Jan-2014 20:31:24 GMT; path=/; SameSite=None; HttpOnly",
                ),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-trans=; domain={domain}; expires=Sat, 11-Jan-2014 20:31:24 GMT; path=/; SameSite=None; HttpOnly",
                ),
                ("Allow", "OPTIONS"),
                ("Allow", "TRACE"),
                ("Allow", "GET"),
                ("Allow", "HEAD"),
                ("Allow", "POST"),
            ]
        )

    def login_step_4_response(self):
        """Fixture for login step 4 response."""
        with open(f"{DIR_NAME}/responses/login_step_4.txt", encoding="utf-8") as file:
            data = file.read()

        return data

    def login_step_4_response_headers(self) -> CIMultiDict:
        """Fixture for login step 4 response headers."""
        domain = self.domain
        return CIMultiDict(
            [
                ("Cache-Control", "no-store, must-revalidate, no-cache"),
                ("Content-Type", "application/json; charset=utf-8"),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-trans=; domain={domain}; expires=Sat, 11-Jan-2014 20:31:24 GMT; path=/; SameSite=None; HttpOnly",
                ),
                ("x-ms-gateway-requestid", "3e839510-5c8e-4a4c-b431-a57f9a95fc5c"),
                ("X-Frame-Options", "DENY"),
                ("Public", "OPTIONS,TRACE,GET,HEAD,POST"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                ("X-Content-Type-Options", "nosniff"),
                ("X-XSS-Protection", "1; mode=block"),
                ("Allow", "OPTIONS"),
                ("Allow", "TRACE"),
                ("Allow", "GET"),
                ("Allow", "HEAD"),
                ("Allow", "POST"),
            ]
        )

    def refresh_token_response_headers(self) -> CIMultiDict:
        """Fixture for refresh token response headers."""
        domain = self.domain
        return CIMultiDict(
            [
                ("Cache-Control", "no-store, must-revalidate, no-cache"),
                ("Content-Type", "application/json; charset=utf-8"),
                (
                    "Set-Cookie",
                    f"x-ms-cpim-trans=; domain={domain}; expires=Sat, 11-Jan-2014 20:31:24 GMT; path=/; SameSite=None; HttpOnly",
                ),
                ("x-ms-gateway-requestid", "15c796c0-f338-4529-a16d-255dd72e24ee"),
                ("X-Frame-Options", "DENY"),
                ("Public", "OPTIONS,TRACE,GET,HEAD,POST"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                ("X-Content-Type-Options", "nosniff"),
                ("X-XSS-Protection", "1; mode=block"),
                ("Allow", "OPTIONS"),
                ("Allow", "TRACE"),
                ("Allow", "GET"),
                ("Allow", "HEAD"),
                ("Allow", "POST"),
            ]
        )

    def get_devices_response(self) -> str:
        """Fixture for get_devices response."""
        with open(f"{DIR_NAME}/responses/get_devices.txt", encoding="utf-8") as file:
            data = file.read()

        return data

    def get_devices_response_headers(self) -> CIMultiDict:
        """Fixture for get devices response headers."""
        return CIMultiDict(
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                (
                    "Request-Context",
                    "appId=cid-v1:9bf1e130-ec63-42ac-b6a7-7ce1131e9176",
                ),
            ]
        )

    def get_device_infos_response(self) -> str:
        """Fixture for get_device_infos response."""
        with open(
            f"{DIR_NAME}/responses/get_device_infos.txt", encoding="utf-8"
        ) as file:
            data = file.read()

        return data

    def get_device_infos_response_headers(self) -> CIMultiDict:
        """Fixture for get devices infos response headers."""
        return CIMultiDict(
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                (
                    "Request-Context",
                    "appId=cid-v1:9bf1e130-ec63-42ac-b6a7-7ce1131e9176",
                ),
            ]
        )

    def get_device_infos_se_response(self) -> str:
        """Fixture for get_device_infos response."""
        with open(
            f"{DIR_NAME}/responses/get_device_infos_SE.txt", encoding="utf-8"
        ) as file:
            data = file.read()

        return data

    def get_device_infos_se_response_headers(self) -> CIMultiDict:
        """Fixture for get devices infos response headers."""
        return CIMultiDict(
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
                (
                    "Request-Context",
                    "appId=cid-v1:9bf1e130-ec63-42ac-b6a7-7ce1131e9176",
                ),
            ]
        )

    def fake_device(self, series: str = "SD") -> Device:
        """Fixture returning fake Device object."""
        devices = {
            "SD": {
                "type": 18,
                "hasError": True,
                "id": "softliQ.D/6ZF9Z5KAA2",
                "series": "softliQ.D",
                "serialNumber": "6ZF9Z5KAA2",
                "name": "softIQ:SD18",
                "register": True,
            },
            "SE": {
                "type": 118,
                "hasError": False,
                "id": "softliQ.SE/BS110",
                "series": "softliQ.SE",
                "serialNumber": "BS110",
                "name": "softIQ:SE18",
                "register": True,
            },
        }
        return Device.from_dict(devices[series])  # pylint: disable=no-member


@pytest.fixture
def fake_api():
    """Fixture for our Fake API."""
    return FakeApi()


@pytest.fixture()
def enter_sd_response_headers() -> CIMultiDict:
    """Fixture for enter sd response headers."""
    return CIMultiDict(
        [
            ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
            ("Request-Context", "appId=cid-v1:9bf1e130-ec63-42ac-b6a7-7ce1131e9176"),
        ]
    )


@pytest.fixture()
def refresh_sd_response_headers() -> CIMultiDict:
    """Fixture for refresh sd response headers."""
    return CIMultiDict(
        [
            ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
            ("Request-Context", "appId=cid-v1:9bf1e130-ec63-42ac-b6a7-7ce1131e9176"),
        ]
    )


@pytest.fixture()
def start_ws_negotiation_response_headers() -> CIMultiDict:
    """Fixture for start ws negotiation response headers."""
    return CIMultiDict(
        [
            ("Content-Type", "application/json; charset=utf-8"),
            # "Content-Encoding": "gzip",
            ("Transfer-Encoding", "chunked"),
            ("Vary", "Accept-Encoding"),
            ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
            ("Request-Context", "appId=cid-v1:9bf1e130-ec63-42ac-b6a7-7ce1131e9176"),
        ]
    )


@pytest.fixture()
def get_ws_connection_id_response_headers() -> CIMultiDict:
    """Fixture for get ws connection id response headers."""
    return CIMultiDict(
        [
            ("Content-Type", "application/json"),
            ("Connection", "keep-alive"),
            ("Access-Control-Allow-Credentials", "true"),
            ("Access-Control-Allow-Origin", "file://"),
            ("Vary", "Origin"),
            ("Strict-Transport-Security", "max-age=15724800; includeSubDomains"),
        ]
    )
