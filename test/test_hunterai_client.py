import pytest
from hunterai_client import HunterAIClient

# Mock responses for testing
class MockResponse:
    @staticmethod
    def json():
        return {"status": "success", "data": "mocked_data"}

    def raise_for_status(self):
        pass

# Mocking requests for testing
def mock_get(*args, **kwargs):
    return MockResponse()

def mock_post(*args, **kwargs):
    return MockResponse()

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr("requests.get", mock_get)
    monkeypatch.setattr("requests.post", mock_post)
    return HunterAIClient(api_key="test_key", token="test_token")

def test_get_crypto_data(client):
    result = client.get_crypto_data("BTC")
    assert result["data"] == "mocked_data"

def test_get_trade_recommendation(client):
    result = client.get_trade_recommendation("ETH")
    assert result["data"] == "mocked_data"

def test_execute_trade(client):
    result = client.execute_trade("BUY", "ETH", amount=1.0)
    assert result["data"] == "mocked_data"

def test_get_balance(client):
    result = client.get_balance()
    assert result["data"] == "mocked_data"
