import xml.etree.ElementTree as ET


def account_generator(id, balance, symbols):
    root = ET.Element("create")

    ET.SubElement(root, "account", {"id": str(id), "balance": str(balance)})

    for sym, amount in symbols:
        symb = ET.SubElement(root, "symbol", {"sym": str(sym)})
        ET.SubElement(symb, "account", {"id": str(id)}).text = str(amount)

    accXML = ET.tostring(root)

    return str(len(accXML)) + '\n' + accXML.decode('UTF-8')


def trans_generator(id, dic):
    root = ET.Element("transactions", {"id": str(id)})

    for d in dic:
        if d[0] == "order":
            ET.SubElement(root, "order", {"sym": str(
                d[1]), "amount": str(d[2]), "limit": str(d[3])})

        elif d[0] == "query":
            ET.SubElement(root, "query", {"id": str(d[1])})

        elif d[0] == "cancel":
            ET.SubElement(root, "cancel", {"id": str(d[1])})

    transXML = ET.tostring(root)

    return str(len(transXML)) + '\n' + transXML.decode('UTF-8')


def get_xml():
    buy_orders = []
    sell_orders = []
    querys = []
    for i in range(20):
        buy_orders.append(["order", chr(ord('A')+i), 10, 100])
        sell_orders.append(["order", chr(ord('A')+i), -5, 90+i])
        querys.append(["query", 1000+i])
    return trans_generator(1, buy_orders)


if __name__ == '__main__':
    init_orders = []
    for i in range(20):
        init_orders.append([chr(ord('A')+i), 10])
    # print(account_generator(1, 100000, init_orders))
    # print(account_generator(2, 100000, init_orders))
    # print(account_generator(3, 100000, init_orders))

    # print(trans_generator(1, buy_orders))

    # print(trans_generator(2, buy_orders))
    # print(trans_generator(2, sell_orders))
    # print(trans_generator(1, querys))
    # print(trans_generator(2, querys))
