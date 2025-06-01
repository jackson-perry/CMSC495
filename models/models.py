from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class VisitorLog(db.Model):
    __tablename__ = 'visitor_logs'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    ip_address = db.Column(db.Text)
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.Text)
    method = db.Column(db.Text)
    path = db.Column(db.Text)
    event_type = db.Column(db.Text)  # 'visit' or 'conversion'
    base_currency = db.Column(db.Text)
    target_currency = db.Column(db.Text)
    amount = db.Column(db.Numeric)
    converted = db.Column(db.Numeric)

class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    iso_alpha2 = db.Column(db.String(2), nullable=False)
    currency_name = db.Column(db.String, nullable=False)
    currency_code = db.Column(db.String(3), nullable=False)
    currency_symbol = db.Column(db.String(10), nullable=False)
    flag = db.Column(db.LargeBinary, nullable=False)  # Stores binary flag image