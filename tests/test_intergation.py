from unittest.mock import patch
from currency.client import CurrencyClient

def test_full_currency_conversion_flow(client, app):
    # Patch the API response inside the app context
    dummy_rates = {"USD": 1.0, "EUR": 0.9}
    
    def mock_get(url, timeout):
        class Dummy:
            def __init__(self):
                self.status_code = 200
            def json(self):
                return {"rates": dummy_rates}
        return Dummy()

    with patch("currency.client.requests.get", mock_get):
        response = client.post("/", data={
            "amount": "100",
            "base_currency": "USD",
            "target_currency": "EUR"
        }, follow_redirects=True)

    # Assert it succeeded and showed the converted result
    assert response.status_code == 200
    html = response.data.decode("utf-8")
    assert "Converted Amount" in html
    assert "90.0" in html or "90" in html  # depending on your rounding
