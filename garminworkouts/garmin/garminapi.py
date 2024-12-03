import logging
from requests import Response
from typing import Literal, Optional
import garth
import os

# Temp fix for API change!
garth.http.USER_AGENT = {}


class GarminApi(object):
    _GARMIN_SUBDOMAIN = "connectapi"
    _GARMIN_VERSION = "24.24.0.181"

    def __init__(self, email, password) -> None:
        self.email: str = email
        self.password: str = password

        tokenstore: Literal['./garminconnect'] | None = "./garminconnect" if os.path.isdir("./garminconnect") else None
        self.login(tokenstore)

    def login(self, /, tokenstore: Optional[str] = None) -> Literal[True]:
        is_cn = False
        self.garth = garth.Client(
            domain="garmin.cn" if is_cn else "garmin.com",
            pool_connections=20,
            pool_maxsize=20
        )
        """Log in using Garth."""
        if tokenstore:
            self.garth.load(tokenstore)
        else:
            self.garth.login(self.email, self.password, prompt_mfa=self.get_mfa)
            # Save tokens for next login
            self.garth.dump("./garminconnect")

        self.display_name: str = self.garth.profile["userName"]
        self.full_name: str = self.garth.profile["fullName"]
        logging.info("Logged in as %s (%s)", self.full_name, self.display_name)

        user_settings: dict = self.get("/userprofile-service/userprofile/user-settings").json()
        self.unit_system: dict | None = user_settings["userData"]["measurementSystem"] \
            if user_settings is not None else None

        try:
            self.version: str = self.get("/info-service/api/system/release-system").json()[0].get('version', '')
        except IndexError:
            self.version = self._GARMIN_VERSION
        try:
            assert self.version == self._GARMIN_VERSION
        except AssertionError:
            logging.error('Updated version: ' + self.version + ' from ' + self._GARMIN_VERSION)

        return True

    def get_mfa(self) -> str:
        """Get MFA."""

        return input("MFA one-time code: ")

    def get(self, *args, **kwargs) -> Response:
        return self.garth.get(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def put(self, *args, **kwargs) -> Response:
        return self.garth.put(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        return self.garth.post(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def delete(self, *args, **kwargs) -> Response:
        return self.garth.delete(self._GARMIN_SUBDOMAIN, *args, **kwargs)

    def download(self, path, **kwargs) -> bytes:
        return self.garth.download(path, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        return None
