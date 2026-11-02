"""A client whose requests are answered by the test, and whose waits are only recorded."""

import json

import httpx
import pytest

from tarifftrust import AsyncTariffTrust, TariffTrust


class Api:
    """What the API answers, in order, and what it received."""

    def __init__(self):
        self.answers = []
        self.requests = []
        self.waits = []

    def answer(self, status=200, body=None, headers=None, text=None):
        self.answers.append(
            httpx.Response(status, headers=headers, text=text)
            if text is not None
            else httpx.Response(status, json=body if body is not None else {}, headers=headers)
        )

    def fail(self, failure):
        self.answers.append(failure)

    def __call__(self, request):
        self.requests.append(request)
        answer = self.answers.pop(0)
        if isinstance(answer, Exception):
            raise answer
        return answer

    @property
    def sent(self):
        return json.loads(self.requests[-1].content)


@pytest.fixture
def api(monkeypatch):
    found = Api()
    monkeypatch.setattr("tarifftrust._client.time.sleep", found.waits.append)

    async def wait(seconds):
        found.waits.append(seconds)

    monkeypatch.setattr("tarifftrust._client.asyncio.sleep", wait)
    return found


@pytest.fixture
def client(api):
    return TariffTrust(
        "tarifftrust_test", http_client=httpx.Client(transport=httpx.MockTransport(api))
    )


@pytest.fixture
def async_client(api):
    return AsyncTariffTrust(
        "tarifftrust_test", http_client=httpx.AsyncClient(transport=httpx.MockTransport(api))
    )
