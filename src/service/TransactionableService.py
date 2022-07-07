from sqlalchemy.orm import Session


class TransactionRequiredService(object):

    def __init__(self, session: Session):
        super().__init__()
        self.session = session
