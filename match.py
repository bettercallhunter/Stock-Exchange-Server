from database import *
from sqlalchemy import desc
from sqlalchemy.orm.attributes import flag_modified



def update_account(session, buyer, seller, sym, amount, price, buyerPrice):
    buyerAccount = session.query(Account).filter(
        Account.id == buyer.account_id).with_for_update().first()
    sellerAccount = session.query(Account).filter(
        Account.id == seller.account_id).with_for_update().first()

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
    


def execute_order(session,sym):
    with session.begin_nested():
        buyer = session.query(Open).filter(Open.amount > 0, Open.sym == sym).with_for_update().order_by(
            desc(Open.limit), Open.time).first()
        seller = session.query(Open).filter(
            Open.amount < 0, Open.sym == sym).with_for_update().order_by(Open.limit, Open.time).first()
        if buyer is None or seller is None or buyer.limit < seller.limit:
            session.commit()
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
        
        session.add(executed_buy)
        session.add(executed_sell)
        buyer.amount -= amount
        seller.amount += amount
        if buyer.amount == 0:
            session.delete(buyer)
        if seller.amount == 0:
            session.delete(seller)
        update_account(session, buyer, seller, buyer.sym, amount, price, buyer.limit)
        session.commit()
    return True


def match_order(session, sym):
    while execute_order(session,sym):
        pass
