from utils.currency_logging import log_event
from models.models import VisitorLog, db

def test_log_event_gets_added(app, client):
    with app.test_request_context("/no-visit", headers={"User-Agent": "test"}, environ_base={"REMOTE_ADDR": "127.0.0.1"}):
        assert "sqlite" in str(db.engine.url), "Refusing to run destructive tests on non-test database!"
        db.session.query(VisitorLog).delete()
        db.session.commit()

        log_event(event_type="test", base="USD", target="EUR", amount=100, result=90)

        log = VisitorLog.query.filter_by(event_type="test").first()
        assert log is not None
        assert log.event_type == "test"

def test_log_event_ip_and_route(app):
    with app.test_request_context("/ip-check", environ_base={"REMOTE_ADDR": "10.0.0.1"}):
        log_event(event_type="ip_route", base="USD", target="EUR", amount=5, result=4.5)
        entry = VisitorLog.query.filter_by(event_type="ip_route").first()
        assert entry.ip_address  == "10.0.0.1"

def test_log_event_long_user_agent(app):
    long_agent = "X" * 300
    with app.test_request_context("/long", headers={"User-Agent": long_agent}, environ_base={"REMOTE_ADDR": "127.0.0.1"}):
        log_event(event_type="long_agent", base="USD", target="EUR", amount=1, result=0.9)
        entry = VisitorLog.query.filter_by(event_type="long_agent").first()
        assert entry is not None
        assert len(entry.user_agent) <= 255 or len(entry.user_agent) == len(long_agent)
