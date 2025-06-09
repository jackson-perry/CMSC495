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

