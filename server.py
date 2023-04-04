import Pyro4
from parsexml import *
from handler import *
import multiprocessing
from multiprocessing import Pool
import time
from database import *


@Pyro4.expose
class StockMarket:
    def readRequest(self, xml_string):
        root = ET.fromstring(xml_string)
        try:
            response = handle(root)

        # with Pool(processes=cores) as p:
        #     response = p.apply(handle, args=(root,))
            # closeDb()
        except Exception as e:
            return e
        return response


daemon = Pyro4.Daemon(port=12345)


uri = daemon.register(StockMarket, "stockmarket")

print("URI:", uri)

daemon.requestLoop()
