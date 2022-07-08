from exception.transaction.transactional_exception import \
    TransactionalException
from service.transaction_required_service import TransactionRequiredService


def transactional(func):
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, TransactionRequiredService):
            raise TransactionalException("Call transactional method "
                                         "outside transactional service!")
        transactional_service: TransactionRequiredService = self
        transaction = transactional_service.session.begin_nested()
        try:
            res = func(self, *args, **kwargs)
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            raise e
        return res

    return wrapper
