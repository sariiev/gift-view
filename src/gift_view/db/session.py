from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from gift_view.db.engine import engine

Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
