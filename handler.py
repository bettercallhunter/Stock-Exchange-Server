
from database import *
from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.orm.attributes import flag_modified
from response import *
from match import *


def handle(root):
    if root.tag == "create":
        handleCreate(root)

    elif root.tag == "transactions":
        handleTransactions(root)


def handleCancel(Responseroot, child, account_id):
    id = child.attrib['id']
    stmt = select(Open).where(Open.id == id)
    order = session.scalar(stmt)
    if order is None:
        msg = "order does not exist"
        cancel_response_error(Responseroot,id,msg)
        return

    if str(order.account_id )!= account_id:
        msg = "You are not authrized to cancel this order"
        cancel_response_error(Responseroot,id,msg)
        return


    amount = order.amount
    limit = order.limit
    # modify account balance and position
    stmt = select(Account).where(Account.id == account_id)
    account = session.scalar(stmt)

    # if it is a buy order
    if int(amount) > 0:
        account.balance += amount * limit
    # if it is a sell order
    else:
        account.position[order.sym] -= amount
        flag_modified(account, "position")
    # delete from open
    stmt = delete(Open).where(Open.id == id)
    session.execute(stmt)
    # add to cancel
    ######### WHAT IS THE TIME OF CANCEL?##########
    cancel = Cancel(id=id, sym=order.sym, amount=order.amount,
                    limit=order.limit, account_id=account_id, time=datetime.now())

    # find order in executed

    stmt = select(Executed).where(Executed.transId == id)
    executed_order = session.scalar(stmt)
    if executed_order is None:
        cancel_response_success(
            Responseroot, id, order.time, order.amount, order.time, order.amount, order.limit, False)

    else:

        cancel_response_success(
            Responseroot, id, order.time, order.amount, executed_order.time, executed_order.amount, executed_order.limit, True)
    session.add(cancel)
    session.commit()


def handleQuery(root):
    id = root.attrib['id']
    # open
    open = session.query(Open).filter_by(id=id).first()
    # canceled
    canceled = session.query(Cancel).filter_by(id=id).first()
    # executed
    executed = session.query(Executed).filter_by(transId=id).all()
    
    query_response(id,open,canceled,executed)
    
        
def handleTransactions(root):
    Responseroot = ET.Element('results')
    for child in root:
        if child.tag == 'order':
            handleOrder(Responseroot, child, root.attrib['id'])
        elif child.tag == 'cancel':
            handleCancel(Responseroot, child, root.attrib['id'])
        elif child.tag == 'query':
            handleQuery(child)

    xml_string = ET.tostring(
        Responseroot, encoding='utf8', method='xml').decode()
    print(xml_string)


def handleOrder(Responseroot, child, account_id) -> None:
    sym = child.attrib['sym']
    amount = child.attrib['amount']
    limit = child.attrib['limit']
    # first, check if there is a match
    stmt = select(Account).where(Account.id == account_id)
    account = session.execute(stmt).fetchone()
    if account is None:
        msg = "account does not exist"
        order_response(Responseroot, False, sym, amount, limit, msg)
        return
    # if it is a buy order
    if int(amount) > 0:
        newBalance = account[0].balance - int(amount) * int(limit)
        if newBalance < 0:
            msg = "insufficient funds"
            order_response(Responseroot, False, sym, amount, limit, msg)
            return

        account[0].balance = newBalance

    # if it is a sell order
    elif int(amount) < 0:
        # check if have enough shares
        if account[0].position is None or sym not in account[0].position or int(account[0].position[sym]) < abs(int(amount)):
            msg = "insufficient shares"
            order_response(Responseroot, False, sym, amount, limit, msg)
            return
        newAmount = int(account[0].position[sym]) - abs(int(amount))
        # update position
        account[0].position[sym] = newAmount
        flag_modified(account[0], "position")
    # add order to database
    Transaction_id = getMaxId()+1

    new_order = Open(account_id=account_id, id=Transaction_id,
                     sym=sym, amount=amount, limit=limit, time=datetime.now())
    order_response(Responseroot, True, sym, amount,
                   limit, "ok", Transaction_id)

    session.add(new_order)
    session.commit()
    print("order placed")
    match_order(sym)


def handleCreate(root):
    Responseroot = ET.Element('results')
    for child in root:
        if child.tag == 'account':
            id = child.attrib['id']
            balance = child.attrib['balance']
            position = child.attrib.get('position')
            hasAccount = session.query(Account).filter_by(id=id).first()
            if hasAccount is not None:
                print("account already exists")
                create_response(Responseroot, id, False)
                continue
            new_account = Account(id=id, balance=balance,
                                  position=position)

            session.add(new_account)
            session.commit()
            create_response(Responseroot, id, True)
        elif child.tag == 'symbol':
            account = child.find('account').attrib['id']
            sym = child.attrib['sym']
            amount = child.find('account').text
            selected = session.query(Account).filter_by(id=account).first()
            if selected is None:
                create_response(Responseroot, id, False, sym)
                print("account does not exist")
                continue
            if selected.position is None:
                create_response(Responseroot, id, True, sym)
                selected.position = {sym: amount}
                flag_modified(selected, "position")
            elif sym not in selected.position:
                create_response(Responseroot, id, True, sym)
                selected.position[sym] = amount
                flag_modified(selected, "position")
            else:
                selected.position[sym] = int(
                    selected.position[sym]) + int(amount)
                flag_modified(selected, "position")
                create_response(Responseroot, id, True, sym)

    session.flush()
    session.commit()
    xml_string = ET.tostring(
        Responseroot, encoding='utf8', method='xml').decode()
    print(xml_string)
    return
