from flask import current_app
from sqlalchemy.orm import Session, SessionTransaction


def transactional(func):
    def wrapper(*args, **kw):
        db_session: Session = current_app.db.session
        transaction: SessionTransaction = db_session.begin_nested()
        try:
            res = func(*args, **kw)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        return res
    return wrapper
