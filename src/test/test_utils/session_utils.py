from unittest.mock import Mock

from sqlalchemy.orm import Session, SessionTransaction


class SessionTestHelper:
    def __init__(self):
        super().__init__()
        self.session_mock = Mock(spec=Session)
        self.session_transaction_mock = Mock(spec=SessionTransaction)
        self.session_mock.begin_nested.return_value = \
            self.session_transaction_mock

    def assert_session_commit(self):
        self.session_mock.begin_nested.assert_called_once()
        self.session_transaction_mock.commit.assert_called_once()
        self.session_transaction_mock.rollback.assert_not_called()
