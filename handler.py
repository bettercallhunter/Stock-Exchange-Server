
from database import *
from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.orm.attributes import flag_modified
from response import *
from match import *


class stockhandler:
    def __init__(self, session):
        self.session = session

    def handle(self, lock, root):
        rootString = ET.tostring(root, encoding='utf8', method='xml').decode()
        print(rootString)
        if root.tag == "create":
            responseRoot = self.handleCreate(lock, root)

        elif root.tag == "transactions":
            responseRoot = self.handleTransactions(lock, root)
        responseString = ET.tostring(
            responseRoot, encoding='utf8', method='xml').decode()

        return responseString

    def handleCancel(self, Responseroot, child, account_id):
        id = child.attrib['id']
        stmt = select(Open).where(Open.id == id)
        order = self.session.scalar(stmt)
        if order is None:
            msg = "order does not exist"
            cancel_response_error(Responseroot, id, msg)
            return

        if str(order.account_id) != account_id:
            msg = "You are not authrized to cancel this order"
            cancel_response_error(Responseroot, id, msg)
            return

        amount = order.amount
        limit = order.limit
        time = order.time
        

        with self.session.begin_nested():
            # modify account balance and position
            stmt = select(Account).where(Account.id == account_id).with_for_update()
            account = self.session.scalar(stmt)
            # if it is a buy order
            if int(amount) > 0:
                account.balance += amount * limit
            # if it is a sell order
            else:
                account.position[order.sym] -= amount
                flag_modified(account, "position")
            # delete from open
            stmt = delete(Open).where(Open.id == id)

            self.session.execute(stmt)
            # add to cancel
            ######### WHAT IS THE TIME OF CANCEL?##########
            cancel = Cancel(id=id, sym=order.sym, amount=order.amount,
                            limit=order.limit, account_id=account_id, time=datetime.now())

            # find order in executed
            self.session.add(cancel)
            self.session.commit()
        stmt = select(Executed).where(Executed.transId == id)
        executed_order = self.session.scalar(stmt)
        if executed_order is None:
            cancel_response_success(
                Responseroot, id, time, amount, time, amount, limit, False)

        else:

            cancel_response_success(
                Responseroot, id, time, amount, executed_order.time, executed_order.amount, executed_order.limit, True)

    def handleQuery(self, Responseroot, root):
        id = root.attrib['id']
        # open
        open = self.session.query(Open).filter_by(id=id).first()
        # canceled
        canceled = self.session.query(Cancel).filter_by(id=id).first()
        # executed
        executed = self.session.query(Executed).filter_by(transId=id).all()

        query_response(Responseroot, id, open, canceled, executed)

    def handleTransactions(self, lock, root):
        Responseroot = ET.Element('results')
        for child in root:
            if child.tag == 'order':
                self.handleOrder(lock, Responseroot, child, root.attrib['id'])
            elif child.tag == 'cancel':
                self.handleCancel(Responseroot, child, root.attrib['id'])
            elif child.tag == 'query':
                self.handleQuery(Responseroot, child)
        return Responseroot

    def handleOrder(self, lock, Responseroot, child, account_id) -> None:
        sym = child.attrib['sym']
        amount = child.attrib['amount']
        limit = child.attrib['limit']
        

        with self.session.begin_nested():
            # first, check if there is a match
            stmt = select(Account).where(
                Account.id == account_id).with_for_update()
            account = self.session.execute(stmt).fetchone()

            if account is None:
                msg = "account does not exist"
                order_response(Responseroot, False, sym, amount, limit, msg)
                return
            # if it is a buy order
            if int(amount) > 0:
                newBalance = account[0].balance - int(amount) * int(limit)
                if newBalance < 0:
                    msg = "insufficient funds"
                    order_response(Responseroot, False,
                                   sym, amount, limit, msg)
                    return

                account[0].balance = newBalance

            # if it is a sell order
            elif int(amount) < 0:
                # check if have enough shares
                if account[0].position is None or sym not in account[0].position or int(account[0].position[sym]) < abs(int(amount)):
                    msg = "insufficient shares"
                    order_response(Responseroot, False,
                                   sym, amount, limit, msg)
                    return
                newAmount = int(account[0].position[sym]) - abs(int(amount))
                # update position
                account[0].position[sym] = newAmount
                flag_modified(account[0], "position")
            # add order to database
            Transaction_id = getMaxId(self.session,lock)+1

            new_order = Open(account_id=account_id, id=Transaction_id,
                             sym=sym, amount=amount, limit=limit, time=datetime.now())
            self.session.add(new_order)
            self.session.commit()
        order_response(Responseroot, True, sym, amount,
                       limit, "ok", Transaction_id)
        print("order placed")
        match_order(self.session, sym)

    def handleCreate(self, lock, root):
        Responseroot = ET.Element('results')
        for child in root:
            child_string = ET.tostring(child, encoding='utf8', method='xml')
            print(child_string)
            if child.tag == 'account':
                id = child.attrib['id']
                balance = child.attrib['balance']
                position = child.attrib.get('position')
                with lock:
                    hasAccount = self.session.query(
                        Account).filter_by(id=id).first()
                    if hasAccount is not None:
                        msg = "account already exists"
                        create_response(Responseroot, id, False, None, msg)
                        continue
                    new_account = Account(id=id, balance=balance,
                                          position=position)

                    self.session.add(new_account)
                    self.session.commit()
                create_response(Responseroot, id, True)

            elif child.tag == 'symbol':
                account = child.find('account').attrib['id']
                sym = child.attrib['sym']
                amount = child.find('account').text
                with self.session.begin_nested():
                    selected = self.session.query(Account).filter_by(
                        id=account).with_for_update().first()
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

                    # self.session.flush()
                    self.session.commit()

        return Responseroot
