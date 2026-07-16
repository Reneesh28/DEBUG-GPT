"""
FastAPI client for DebugGPT.
"""

from __future__ import annotations

import requests

BASE_URL = "http://127.0.0.1:8000"

TIMEOUT = 300


class APIClientError(Exception):
    """Raised when the backend cannot be reached."""


def _request(method: str, endpoint: str, payload: dict | None = None, is_form: bool = False):
    """
    Generic request helper.
    """

    url = f"{BASE_URL}{endpoint}"

    try:
        kwargs = {"timeout": TIMEOUT}
        if is_form:
            kwargs["data"] = payload
        else:
            kwargs["json"] = payload

        response = requests.request(
            method=method,
            url=url,
            **kwargs
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        raise APIClientError(
            "The backend request timed out."
        )

    except requests.exceptions.ConnectionError:

        raise APIClientError(
            "Unable to connect to the FastAPI backend."
        )

    except requests.exceptions.HTTPError as exc:

        try:
            detail = response.json()
        except Exception:
            detail = response.text

        raise APIClientError(
            f"Backend returned an error:\n{detail}"
        ) from exc

    except requests.RequestException as exc:

        raise APIClientError(str(exc)) from exc


def health():
    return _request("GET", "/health")


def analyze(language: str, code: str):
    mapped_lang = "cpp" if language.lower() == "c++" else language.lower()
    return _request(
        "POST",
        "/analyze",
        {
            "language": mapped_lang,
            "code": code,
        },
        is_form=True,
    )


def debug(language: str, code: str):
    mapped_lang = "cpp" if language.lower() == "c++" else language.lower()
    return _request(
        "POST",
        "/debug",
        {
            "language": mapped_lang,
            "code": code,
        },
        is_form=True,
    )


def explain(error: str):
    return _request(
        "POST",
        "/explain",
        {
            "error": error,
        },
    )


def optimize(language: str, code: str):
    mapped_lang = "cpp" if language.lower() == "c++" else language.lower()
    return _request(
        "POST",
        "/optimize",
        {
            "language": mapped_lang,
            "code": code,
        },
        is_form=True,
    )