# import Pyro4
# from parsexml import *
# from handler import *
# import multiprocessing
# from multiprocessing import Pool
# import time
# from database import *


# @Pyro4.expose
# class StockMarket:
#     def readRequest(self, xml_string):
#         root = ET.fromstring(xml_string)
#         response = handle(root)

#         closeDb()
#         return response


# if __name__ == "__main__":
#     with Pool(4) as pool:

#         daemon = Pyro4.Daemon(port=12345)

#         uri = daemon.register(StockMarket, "stockmarket")
#         print(f"Server URI: {uri}")
#         ns = Pyro4.locateNS()
#         ns.register("stockmarket", uri)
#         for i in range(4):
#             pool.apply_async(daemon.requestLoop)
#         pool.close()
#         pool.join()
# import Pyro4
# import xml.etree.ElementTree as ET
# from parsexml import *
# from handler import *
# from database import *
# import threading

# Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')


# @Pyro4.expose
# class StockMarket:
#     def readRequest(self, xml_string):
#         root = ET.fromstring(xml_string)
#         response = handle(root)
#         closeDb()
#         return response


# class RequestHandlerThread(threading.Thread):
#     def __init__(self, daemon):
#         super().__init__()
#         self.daemon = daemon

#     def run(self):
#         self.daemon.requestLoop()


# if __name__ == "__main__":
#     # Create Pyro4 daemon
#     daemon = Pyro4.Daemon(port=12345)
#     uri = daemon.register(StockMarket, "stockmarket")
#     print(f"Server URI: {uri}")

#     # Start multiple request handler threads
#     handler_threads = []
#     for i in range(4):
#         handler_thread = RequestHandlerThread(daemon)
#         handler_thread.start()
#         handler_threads.append(handler_thread)

#     # Wait for all handler threads to finish
#     for handler_thread in handler_threads:
#         handler_thread.join()
from flask import Flask, request
import xml.etree.ElementTree as ET
from parsexml import *
from handler import *
from database import *

app = Flask(__name__)


@app.route('/readRequest', methods=['POST'])
def readRequest():
    xml_string = request.data.decode('utf-8')
    root = ET.fromstring(xml_string)
    response = handle(root)
    return response


def close():
    closeDb()


if __name__ == '__main__':
    app.run(port=12345, threaded=True)
