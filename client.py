# import sys
# import xml.etree.ElementTree as ET
# import argparse
# import Pyro4
# import time
# from xmlGenerate import *

# uri = "PYRO:stockmarket@localhost:12345"
# stock_market = Pyro4.Proxy(uri)
# order1 = sys.argv
# with open('randomTransactions.xml', 'r') as f:
#     input_string = f.read()
#     xml_string = input_string.split('\n', 1)[1].strip()

# start_time = time.time()
# for i in range(1000):
#     response = stock_market.readRequest(xml_string)
#     print(response)
# end_time = time.time()
# used_time = end_time-start_time
# print("executation time", used_time)
import sys
import xml.etree.ElementTree as ET
import argparse
import requests
import time
from xmlGenerate import *

url = 'http://localhost:12345/readRequest'
order1 = sys.argv
with open('randomTransactions.xml', 'r') as f:
    input_string = f.read()
    xml_string = input_string.split('\n', 1)[1].strip()

start_time = time.time()
response = requests.post(url, data=xml_string).text
print(response)
end_time = time.time()
used_time = end_time-start_time
print("execution time", used_time)
