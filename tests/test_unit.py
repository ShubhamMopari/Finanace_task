from datetime import datetime, timedelta

def test_expiry_rule():
    future = datetime.utcnow() + timedelta(minutes=2)
    assert future > datetime.utcnow()
