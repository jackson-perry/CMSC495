from flask import request
from models import VisitorLog, db


def get_real_ip():
        # Get IP from X-Forwarded-For if present, otherwise fallback to remote_addr
        forwarded_for = request.headers.get('X-Forwarded-For', '')
        if forwarded_for:
            # X-Forwarded-For can contain multiple IPs, client IP is first
            ip = forwarded_for.split(',')[0].strip()
        else:
            ip = request.remote_addr
        return ip

def log_event(event_type, base=None, target=None, amount=None, result=None):
        try:
            log = VisitorLog(
                ip_address=get_real_ip(),
                user_agent=request.headers.get("User-Agent"),
                referrer=request.referrer,
                method=request.method,
                path=request.path,
                event_type=event_type,
                base_currency=base,
                target_currency=target,
                amount=amount,
                converted=result
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            print(f"[ERROR] Failed to log visitor event: {e}")
            db.session.rollback()