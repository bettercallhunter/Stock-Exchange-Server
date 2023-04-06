import multiprocessing
import socket
import xml.etree.ElementTree as ET
from parsexml import *
from handler import *
from database import *


def receiveStr(sfile):
    num = sfile.readline()
    # if num != "":
    return sfile.read(int(num))
    raise Exception("received nothing")


def acceptCon(socket):
    while 1:
        conn, address = socket.accept()
        handleCon(conn)
        conn.close()


def handleCon(conn):

    sfile = conn.makefile('rw', 1)
    num = sfile.readline()
    # if num != "":
    #     return
    msg = sfile.read(int(num))
    # msg = receiveStr(sfile)
    # print(msg)
    root = ET.fromstring(msg)
    response = handle(root)
    # sfile.write(str(len(response)))
    sfile.write(response)
    print(response)
    return
    # return
    #     data = connection.recv(1000000)
    #        if data == "":
    #             break
    #         root = ET.fromstring(data.decode())
    #         response = handle(root)
    #         connection.sendall(response.encode())
    # except:
    #     connection.close()
    # finally:

    #     connection.close()


class Server(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        processes = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))

        self.socket.listen()

        print("Server started.\n")
        for i in range(4):
            process = multiprocessing.Process(
                target=acceptCon, args=(self.socket, ))
            process.daemon = True
            process.start()
            processes.append(process)

        for process in processes:
            process.join()


if __name__ == "__main__":

    server = Server("0.0.0.0", 8000)

    server.start()
