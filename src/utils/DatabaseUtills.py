from exception.transaction.TransactionalException import TransactionalException
from service.TransactionableService import TransactionRequiredService


def transactional(func):
    def wrapper(self, *args, **kw):
        if not isinstance(self, TransactionRequiredService):
            raise TransactionalException("Call transactional method "
                                         "outside transactional service!")
        transactional_service: TransactionRequiredService = self
        transaction = transactional_service.session.begin_nested()
        try:
            res = func(self, *args, **kw)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        return res

    return wrapper
