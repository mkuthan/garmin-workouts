import pytest
from garminworkouts.garmin.garminclient import GarminClient
import account


@pytest.fixture
def authed_gclient() -> GarminClient:
    return GarminClient(account.EMAIL, account.PASSWORD)
