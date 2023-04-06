import multiprocessing
import socket
import xml.etree.ElementTree as ET
from parsexml import *
from handler import *
from database import *
from multiprocessing import Lock
import cProfile
import pstats
import os
# Create the engine and sessionmaker instances
engine = create_engine(
    "postgresql://postgres:0000@localhost:5432/stock?sslmode=disable")
Session = sessionmaker(bind=engine)


def receiveStr(sfile):
    num = sfile.readline()
    # if num != "":
    return sfile.read(int(num))
    raise Exception("received nothing")


def acceptCon(socket, lock):
    session = Session()
    handler = stockhandler(session)
    while 1:
        conn, address = socket.accept()
        handleCon(conn, lock, handler)
        conn.close()


def handleCon(conn, lock, handler):

    sfile = conn.makefile('rw', 1)
    num = sfile.readline()
    # if num != "":
    #     return
    msg = sfile.read(int(num))
    # msg = receiveStr(sfile)
    # print(msg)
    root = ET.fromstring(msg)
    response = handler.handle(lock, root)
    # sfile.write(str(len(response)))
    sfile.write(response)
    print(response)
    return


class Server(object):
    def __init__(self, port, num):
        self.port = port
        self.num = num
        self.lock = Lock()
        self.processes = []

    def start(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("localhost", self.port))
        self.socket.listen(5)

        print("Server started.\n")
        for i in range(self.num):
            process = multiprocessing.Process(
                target=acceptCon, args=(self.socket, self.lock))
            process.daemon = True
            process.start()
            self.processes.append(process)

        for process in self.processes:
            process.join()


if __name__ == "__main__":

    server = Server(12345, 4)
    server.start()
