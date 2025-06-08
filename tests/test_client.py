from currency.client import CurrencyClient

def test_currency_client_calculate(monkeypatch):
    dummy_response = {
        "rates": {"USD": 1.0, "EUR": 0.9}
    }

    def mock_get(url, timeout):
        class Dummy:
            def __init__(self):
                self.status_code = 200
            def json(self):
                return dummy_response
        return Dummy()

    monkeypatch.setattr("requests.get", mock_get)

    client = CurrencyClient("fake_app_id")
    client.set_base_currency("USD")
    client.set_target_currency("EUR")
    client.set_base_value(100)
    result = client.calculate()
    assert result == 90.0
