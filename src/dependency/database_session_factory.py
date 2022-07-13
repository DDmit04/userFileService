from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from exception.transaction.session_not_found_exception import \
    SessionNotFoundException
from model.database_init import Base


@dataclass
class SessionRecord:
    session_id: str
    session: Session


class DatabaseSessionFactory:

    def __init__(self, db_url: str):
        super().__init__()
        self.sessions_pool: list[SessionRecord] = []
        self.db_url = db_url

    def get_session(self, session_id: str) -> Session:
        existing_session_record: SessionRecord = self \
            .__find_session_by_id(session_id)
        if existing_session_record is None:
            session = self.__create_new_session()
            self.sessions_pool.append(SessionRecord(session_id, session))
            session.begin()
            return session
        return existing_session_record.session

    def close_session(self, session_id):
        existing_session_record: SessionRecord = self \
            .__find_session_by_id(session_id)
        if existing_session_record is None:
            raise SessionNotFoundException()
        session: Session = existing_session_record.session
        session.commit()
        session.close()
        self.sessions_pool.remove(existing_session_record)

    def __create_new_session(self) -> Session:
        db_url = self.db_url
        engine: str = create_engine(db_url, echo=True)
        Base.metadata.create_all(engine)
        session_maker: sessionmaker = sessionmaker(bind=engine)
        session: Session = session_maker()
        return session

    def __find_session_by_id(self, session_id) -> SessionRecord:
        for existing_session in self.sessions_pool:
            if existing_session.session_id == session_id:
                return existing_session
        return None