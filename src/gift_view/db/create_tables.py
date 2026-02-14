from gift_view.db.base import Base
from gift_view.db.engine import engine

import gift_view.db.models


def create_tables():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()