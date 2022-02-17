from sqlalchemy.orm.session import Session

from .Account import Account
from sqlalchemy.orm.session import sessionmaker
from decimal import *

class EconomySystem():
    def __init__(self, db_sessionmaker:sessionmaker):
        self.sessionmaker = db_sessionmaker

    def validate(self, money):
        try:
            money = Decimal(money)
        except:
            return False
        if money.is_nan() or money.is_infinite():
            return False
        return money

    def create_account(self, id, starting_money=0.0):
        with self.sessionmaker() as session:
            session.add(Account(id=id, money=starting_money))
            session.commit()

    def earn(self, id, money):
        money = self.validate(money)
        if not money:
            return False
        with self.sessionmaker() as session:
            acc = session.query(Account).get(id)
            if acc.money + money >= 0.0:
                acc.money += money
                session.commit()
                return True
            else:
                return False

    def pay(self, from_id, to_id, money):
        money = self.validate(money)
        if not money:
            return False

        with self.sessionmaker() as session:
            from_acc = session.query(Account).get(from_id)
            to_acc = session.query(Account).get(to_id)

            if from_acc is not None and to_acc is not None:
                if money <= from_acc.money:
                    to_acc.money += money
                    from_acc.money -= money
                    session.commit()
                    return True
                else:
                    return False

    def info(self, id):
        with self.sessionmaker() as session:
            acc = session.query(Account).get(id)
            if acc is not None:
                return acc.money
            else:
                return None


