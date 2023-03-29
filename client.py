import sys
import xml.etree.ElementTree as ET
import argparse
import Pyro4

uri = "PYRO:stockmarket@localhost:12345"
stock_market = Pyro4.Proxy(uri)
order1 = sys.argv

matched_order = stock_market.match_orders(order1, order2)


print("Matched order:", matched_order)
