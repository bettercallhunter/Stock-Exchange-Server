import xml.etree.ElementTree as ET
from database import *
from handler import *
from bs4 import BeautifulSoup
import multiprocessing
# def reply(success,):
#     results = ET.Element('results')
#     if success:
#         node = ET.SubElement(results, 'created')
#         node.set('account_id', account_id)
#         if symbol is not None:
#             node.set('sym', symbol)
#     else:
#         print("Failure")


def readRequest(xml):
    with open(xml, 'r') as f:
        input_string = f.read()
        xml_string = input_string.split('\n', 1)[1].strip()
        root = ET.fromstring(xml_string)
        
if __name__ == "__main__":
    flag = int(input(
        "Enter 0 for init_db, 1 for create, 2 for transaction, 3 for query: "))
    if flag == 0:
        init_db()
    elif flag == 1:
        xml = "create.xml"
    elif flag == 2:
        xml = "transactions.xml"
    elif flag == 3:
        xml = "query.xml"

# with open('query.xml', 'r') as f:
# with open('create.xml', 'r') as f:
    with open(xml, 'r') as f:
        input_string = f.read()
        xml_string = input_string.split('\n', 1)[1].strip()
        root = ET.fromstring(xml_string)
        handle(root)


