from flask_sqlalchemy import SQLAlchemy


class TransactionRequiredService(object):
    database: SQLAlchemy

    def __init__(self, database) -> None:
        super().__init__()
        self.database = database
