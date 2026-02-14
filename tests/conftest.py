import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import gift_view.db.models

from gift_view.db.base import Base
from gift_view.db.models import Marketplace, Asset, Gift, Backdrop, Symbol, Sale


@pytest.fixture
def session():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


# @pytest.fixture
# def marketplace(session):
#     obj = Marketplace(name="test_marketplace")
#     session.add(obj)
#     session.commit()
#     return obj
#
#
# @pytest.fixture
# def asset(session):
#     obj = Asset(symbol="TON")
#     session.add(obj)
#     session.commit()
#     return obj
#
#
# @pytest.fixture
# def gift(session):
#     obj = Gift(name="test_gift")
#     session.add(obj)
#     session.commit()
#     return obj
#
#
# @pytest.fixture
# def backdrop(session):
#     obj = Backdrop(name="test_backdrop", rarity_percent=10)
#     session.add(obj)
#     session.commit()
#     return obj
#
#
# @pytest.fixture
# def symbol(session):
#     obj = Symbol(name="test_symbol", rarity_percent=8)
#     session.add(obj)
#     session.commit()
#     return obj
#
#
# @pytest.fixture
# def sale(
#     session,
#     marketplace,
#     gift,
#     model,
#     backdrop,
#     symbol,
#     asset,
# ):
#     sale = Sale(
#         marketplace_id=marketplace.id,
#         gift_id=gift.id,
#         gift_number=1,
#         model_id=model.id,
#         backdrop_id=backdrop.id,
#         symbol_id=symbol.id,
#         asset_id=asset.id,
#         price_native=10.0,
#         price_usd=12.5,
#     )
#
#     session.add(sale)
#     session.commit()
#
#     return sale