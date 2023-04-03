from database import *
from sqlalchemy import desc
from sqlalchemy.orm.attributes import flag_modified


def get_max_buyer(sym):
    buyer = session.query(Open).filter(Open.amount > 0, Open.sym == sym).order_by(
        desc(Open.limit), Open.time).first()
    return buyer


def get_min_seller(sym):
    seller = session.query(Open).filter(
        Open.amount < 0, Open.sym == sym).order_by(Open.limit, Open.time).first()
    return seller


def update_account(buyer, seller, sym, amount, price, buyerPrice):
    buyerAccount = session.query(Account).filter(
        Account.id == buyer.account_id).first()
    sellerAccount = session.query(Account).filter(
        Account.id == seller.account_id).first()

    if buyerAccount.position is None:
        buyerAccount.position = {sym: amount}
    elif sym not in buyerAccount.position:
        buyerAccount.position[sym] = amount
    else:
        buyerAccount.position[sym] = int(
            buyerAccount.position[sym]) + int(amount)
    flag_modified(buyerAccount, "position")

    sellerAccount.balance += amount*price
    buyerAccount.balance += amount * (buyerPrice - price)


def execute_order(buyer, seller):
    if buyer.limit < seller.limit:
        return False
    now = datetime.now()
    price = buyer.limit
    if buyer.time > seller.time:
        price = seller.limit
    amount = min(buyer.amount, abs(seller.amount))
    executed_buy = Executed(transId=buyer.id, sym=buyer.sym, amount=amount,
                            limit=price, account_id=buyer.account_id, time=now)
    executed_sell = Executed(transId=seller.id, sym=seller.sym, amount=amount,
                             limit=price, account_id=seller.account_id, time=now)
    with session.begin_nested():
        session.add(executed_buy)
        session.add(executed_sell)
        buyer.amount -= amount
        seller.amount += amount
        if buyer.amount == 0:
            session.delete(buyer)
        if seller.amount == 0:
            session.delete(seller)
        update_account(buyer, seller, buyer.sym, amount, price, buyer.limit)
        session.commit()
    return True


def match_order(sym):
    buyer = get_max_buyer(sym)
    seller = get_min_seller(sym)
    while buyer is not None and seller is not None and execute_order(buyer, seller):
        buyer = get_max_buyer(sym)
        seller = get_min_seller(sym)