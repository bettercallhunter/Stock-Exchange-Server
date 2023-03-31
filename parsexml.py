import xml.etree.ElementTree as ET
from database import *
from handler import *
from bs4 import BeautifulSoup


# def reply(success,):
#     results = ET.Element('results')
#     if success:
#         node = ET.SubElement(results, 'created')
#         node.set('account_id', account_id)
#         if symbol is not None:
#             node.set('sym', symbol)
#     else:
#         print("Failure")


# if __name__ == "main":
# init_db()

with open('transactions.xml', 'r') as f:
    # with open('create.xml', 'r') as f:
    input_string = f.read()
    xml_string = input_string.split('\n', 1)[1].strip()
    root = ET.fromstring(xml_string)
    handle(root)
