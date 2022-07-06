from sqlalchemy.orm import Session

from exception.TransactionalException import TransactionalException
from service.TransactionableService import TransactionRequiredService


def transactional(func):
    def wrapper(self, *args, **kw):
        if not isinstance(self, TransactionRequiredService):
            raise TransactionalException("Call transactional method outside transactional service!")
        db_session: Session = self.database.session
        try:
            res = func(self, *args, **kw)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e
        return res
    return wrapper
