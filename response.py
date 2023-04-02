import xml.etree.ElementTree as ET


def query_response(id, open, canceled, executed):
    # Create the root element
    status = ET.Element("status", {"id": id})
    if open is not None:
        shares = str(open.amount)
        # Create the "open" element
        open_elem = ET.SubElement(status, "open", {"shares": shares})

    if canceled is not None:
        shares = str(canceled.amount)
        time = str(int(canceled.time.timestamp()))
        # Create the "canceled" element
        canceled_elem = ET.SubElement(
            status, "canceled", {"shares": shares, "time": time})

    if executed is not None:
        for each in executed:
            shares = str(each.amount)
            price = str(each.limit)
            time = str(int(each.time.timestamp()))
            # Create the "executed" element
            executed_elem = ET.SubElement(
                status, "executed", {"shares": shares, "price": price, "time": time})
    # Create the XML tree
    tree = ET.ElementTree(status)
    # Convert the XML tree to a string and print it
    xml_string = ET.tostring(status, encoding="unicode")
    print(xml_string)

    return tree

# sym is true if create symbol


def create_response(root, id, success, sym=None, msg=None):
    if not success:
        if sym:
            errorElement = ET.SubElement(root, 'error', {'sym': sym, 'id': id})
        else:
            errorElement = ET.SubElement(root, 'error', {'id': id})
        if sym is None:
            if msg is None:
                errorElement.text = "Account Already Exists"
            else:
                errorElement.text = msg
        else:
            if msg is None:
                errorElement.text = "Cannot find account"
            else:
                errorElement.text = msg

    else:
        if sym is None:
            createElement = ET.SubElement(root, 'created', {'id': id})
        else:
            createElement = ET.SubElement(
                root, 'created', {'sym': sym, 'id': id})

    return ET


def order_response(root, success, sym, amount, limit, msg, id=-1):
    if not success:
        errorElement = ET.SubElement(
            root, 'error', {'sym': sym, 'amount': str(amount), 'limit': limit})

        errorElement.text = msg
    else:
        createElement = ET.SubElement(
            root, 'opened', {'sym': sym, 'amount': str(amount), 'limit': str(limit), 'id': str(id)})
    return ET


def cancel_response_success(root,id, openTime, openShare, executedTime, executedShare, price, hasExecuted=False):
    canceledElement = ET.SubElement(root, 'canceled', {'id': str(id)})
    cancalled = ET.SubElement(canceledElement, 'canceled', {
                              'shares': str(openShare), 'time': str(openTime)})
    if hasExecuted:
        executed = ET.SubElement(canceledElement, 'executed', {'shares': str(
            executedShare), 'price': str(price), 'time': str(executedTime)})
    return ET


def cancel_response_error(root, sym, amount, limit, msg):
    errorElement = ET.SubElement(
        root, 'error', {'sym': sym, 'amount': str(amount), 'limit': limit})

    errorElement.text = msg
    return ET
