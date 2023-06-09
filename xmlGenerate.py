import random
import xml.etree.ElementTree as ET


def generate_xml(num_orders):
    orders = []
    for i in range(num_orders):
        sym = 'SYM' if random.randint(0, 2) == 0 else 'SYX'
        amount = random.randint(-100, 100)
        limit = random.randint(1, 100)
        order = ET.Element('order', sym=sym, amount=str(
            amount), limit=str(limit))
        orders.append(order)

    transactions = ET.Element('transactions', id='123456')

    transactions.extend(orders)

    xml_string = ET.tostring(
        transactions, encoding='UTF-8', xml_declaration=True).decode()
    xml_length = len(xml_string)
    with open('randomTransactions.xml', "w") as f:
        f.write('{}\n{}'.format(xml_length, xml_string))
    return


# generate_xml(5)
# print(generate_xml(5))
