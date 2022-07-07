from flask_sqlalchemy import SQLAlchemy


class TransactionRequiredService(object):

    def __init__(self, database: SQLAlchemy) -> None:
        super().__init__()
        self.database = database
