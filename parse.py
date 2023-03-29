import xml.etree.ElementTree as ET
import sys

# Get the command-line input
input_list = sys.argv[1:]

# Extract the account ID, balance, and symbol from the input list
account_id = input_list[1]
balance = input_list[2]
symbol = input_list[3]

# Create the XML document
root = ET.Element('create')
account_elem = ET.SubElement(
    root, 'account', id=str(account_id), balance=str(balance))
symbol_elem = ET.SubElement(root, 'symbol', sym=symbol)
symbol_elem_account = ET.SubElement(symbol_elem, 'account', id=str(account_id))
symbol_elem_account.text = '100000'

# Output the XML document as a string
xml_string = ET.tostring(root, encoding='UTF-8')
print(xml_string.decode('UTF-8'))
