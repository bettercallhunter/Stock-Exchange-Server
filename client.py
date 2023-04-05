import sys
import xml.etree.ElementTree as ET
import argparse
import Pyro4
import time
from xmlGenerate import *

uri = "PYRO:stockmarket@localhost:12345"
stock_market = Pyro4.Proxy(uri)
order1 = sys.argv
with open('randomTransactions.xml', 'r') as f:
    input_string = f.read()
    xml_string = input_string.split('\n', 1)[1].strip()
# xml_string=generate_xml(100)
cores = int(input("how many of cores do you want to use: "))
start_time = time.time()
response = stock_market.readRequest(xml_string, cores)
end_time = time.time()
print(response)
used_time = end_time-start_time
print("executation time", used_time)
