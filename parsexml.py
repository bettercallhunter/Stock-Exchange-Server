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
        



