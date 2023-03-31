import xml.etree.ElementTree as ET
from database import *
# define the input string
input_string = '''  173
  <?xml version="1.0" encoding="UTF-8"?>
  <create>
    <account id="123456" balance="1000"/>
    <symbol sym="SPY">
      <account id="123456">100000</account>
    </symbol>
    <symbol sym="SPY">
      <account id="123456">100000</account>
    </symbol>
    <symbol sym="SPY">
      <account id="123456">100000</account>
    </symbol>
  </create>'''


def handleCreate(root):
    # for child in root:
    #     if child.tag == "account":
    #         id = child.attrib['id']
    #         balance = child.attrib['balance']
    #         new_account = Account(id=id, balance=balance)
    #         session.add(new_account)
    #     elif child.tag == "symbol":
    #         print(child.tag)
    #         print(child.attrib)

    #         sym = child.attrib['sym']
    # session.commit()
    root = ET.fromstring(xml_string)
    for child in root:
        if child.tag == 'account':
            id = child.attrib['id']
            balance = child.attrib['balance']
            position = child.attrib.get('position')
            print(id, balance, position)
            new_account = Account(id=id, balance=balance, position=position)
            session.add(new_account)
        elif child.tag == 'symbol':
            account = child.find('account').attrib['id']
            sym = child.attrib['sym']
            number = child.find('account').text
            try:
                last_symbol_id = session.query(
                    Symbol.id).order_by(desc(Symbol.id)).first()[0]
            except:
                last_symbol_id = 0

            new_symbol = Symbol(
                id=last_symbol_id+1, sym=sym, number=number, account_id=account)
            session.add(new_symbol)
    session.commit()


xml_string = input_string.split('\n', 1)[1].strip()

# parse the XML string using ElementTree
root = ET.fromstring(xml_string)


if root.tag == "create":
    handleCreate(root)


# print the child elements and their attributes
