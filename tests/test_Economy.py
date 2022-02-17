import pytest
from bot.cogs.economy.EconomySystem import EconomySystem
import sqlalchemy.dialects.sqlite
from bot.database.DatabaseHandler import DatabaseHandler
from bot.cogs.economy.Account import BaseAccount


def test_create_acc():
    test_db_handler = DatabaseHandler(address='sqlite://', bases=[BaseAccount])
    ecos = EconomySystem(test_db_handler.session)
    ecos.create_account(123)
    assert ecos.info(123) == 0.0
    assert ecos.info(1) is None

def test_pay():
    test_db_handler = DatabaseHandler(address='sqlite://', bases=[BaseAccount])
    ecos = EconomySystem(test_db_handler.session)
    ecos.create_account(123)
    ecos.earn(123, 50)
    assert ecos.info(123) == 50.0

    ecos.create_account(9999)
    ecos.earn(9999, -10)
    assert ecos.info(9999) == 0.0

    ecos.pay(9999, 123, 1.0)
    assert ecos.info(123) == 50.0

    ecos.pay(123, 9999, 50.0)
    assert ecos.info(123) == 0.0
    assert ecos.info(9999) == 50.0