from utils.currency_logging import log_event

def test_log_event_gets_added(app, client):
    with app.test_request_context("/", headers={"User-Agent": "test"}, environ_base={"REMOTE_ADDR": "127.0.0.1"}):
        log_event(event_type="test", base="USD", target="EUR", amount=100, result=90)
        from models.models import VisitorLog
        log = VisitorLog.query.first()
        assert log is not None
        assert log.event_type == "test"
        assert log.base_currency == "USD"
