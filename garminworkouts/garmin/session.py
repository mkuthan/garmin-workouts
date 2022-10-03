import os
import re
from http import cookiejar

import cloudscraper


def connect(connect_url, sso_url, username, password, cookie_jar):
    session = cloudscraper.CloudScraper()
    _load_cookie_jar(session, cookie_jar)

    url = connect_url + "/modern/settings"
    response = session.get(url, allow_redirects=False)
    if response.status_code != 200:
        _authenticate(session, connect_url, sso_url, username, password)

    return session


def disconnect(session):
    _save_cookie_jar(session)
    session.close()


def _load_cookie_jar(session, cookie_jar):
    if cookie_jar:
        session.cookies = cookiejar.LWPCookieJar(cookie_jar)
        if os.path.isfile(cookie_jar):
            session.cookies.load(ignore_discard=True, ignore_expires=True)


def _save_cookie_jar(session):
    if isinstance(session.cookies, cookiejar.LWPCookieJar):
        session.cookies.save(ignore_discard=True, ignore_expires=True)


def _authenticate(session, connect_url, sso_url, username, password):
    url = sso_url + "/sso/signin"
    headers = {'origin': 'https://sso.garmin.com'}
    params = {
        "service": "https://connect.garmin.com/modern"
    }
    data = {
        "username": username,
        "password": password,
        "embed": "false"
    }

    auth_response = session.post(url, headers=headers, params=params, data=data)
    auth_response.raise_for_status()

    auth_ticket = _extract_auth_ticket(auth_response.text)

    response = session.get(connect_url + "/modern", params={"ticket": auth_ticket})
    response.raise_for_status()


def _extract_auth_ticket(auth_response):
    match = re.search(r'response_url\s*=\s*".*\?ticket=(.+)"', auth_response)
    if not match:
        raise Exception("Unable to extract auth ticket URL from:\n%s" % auth_response)
    return match.group(1)
