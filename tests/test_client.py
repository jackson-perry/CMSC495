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

def test_xss_injection_prevention(client):
    xss_payload = "<script>alert('xss')</script>"
    response = client.post("/", data={
        "base": "USD",
        "target": "EUR",
        "amount": xss_payload
    })

    assert response.status_code == 200
    html = response.data.decode("utf-8")

    # XSS payload should be escaped or not appear at all
    assert xss_payload not in html
    assert "alert('xss')" not in html

