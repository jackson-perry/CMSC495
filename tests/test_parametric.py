import pytest
from currency.client import CurrencyClient

# Mocked exchange rates for consistency in tests
mock_rates = {
    "USD": 1.0,
    "EUR": 0.9,
    "JPY": 140.0,
    "GBP": 0.8,
    "CAD": 1.3
}

@pytest.mark.parametrize("amount", [0, -1, 1000000])
def test_conversion_edge_amounts(monkeypatch, amount):
    def mock_get(url, timeout):
        class Dummy:
            def __init__(self):
                self.status_code = 200
            def json(self):
                return {"rates": mock_rates}
        return Dummy()

    monkeypatch.setattr("currency.client.requests.get", mock_get)

    client = CurrencyClient("fake_app_id")
    client.set_base_currency("USD")
    client.set_target_currency("EUR")
    client.set_base_value(amount)
    result = client.calculate()

    assert isinstance(result, float)
    assert result >= 0 or amount < 0  # check logic doesn't crash for negatives

@pytest.mark.parametrize("target_currency", ["EUR", "JPY", "GBP", "CAD"])
def test_all_supported_currencies(monkeypatch, target_currency):
    def mock_get(url, timeout):
        class Dummy:
            def __init__(self):
                self.status_code = 200
            def json(self):
                return {"rates": mock_rates}
        return Dummy()

    monkeypatch.setattr("currency.client.requests.get", mock_get)

    client = CurrencyClient("fake_app_id")
    client.set_base_currency("USD")
    client.set_target_currency(target_currency)
    client.set_base_value(100)
    result = client.calculate()

    assert result > 0
