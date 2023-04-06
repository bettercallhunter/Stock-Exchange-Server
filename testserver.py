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

def receiveStr(sfile):
    num = sfile.readline()
    # if num != "":
    return sfile.read(int(num))
    raise Exception("received nothing")


def acceptCon(socket,lock):
    count = 0
    while 1:
        conn, address = socket.accept()
        handleCon(conn,lock)
        count += 1
        #conn.close()


def handleCon(conn,lock):

    sfile = conn.makefile('rw', 1)
    num = sfile.readline()
    # if num != "":
    #     return
    msg = sfile.read(int(num))
    # msg = receiveStr(sfile)
    # print(msg)
    root = ET.fromstring(msg)
    response = handle(lock, root)
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
    def __init__(self, port, num):
        self.port = port
        self.num = num
        self.lock = Lock()
        self.processes = []

    def start(self):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("localhost", self.port))
        self.socket.listen(5)

        print("Server started.\n")
        for i in range(self.num):
            process = multiprocessing.Process(
                target=self.acceptCon_with_profile, args=(self.socket, self.lock))
            process.daemon = True
            process.start()
            self.processes.append(process)

        for process in self.processes:
            process.join()
            
    def acceptCon_with_profile(self, socket, lock):
        pr = cProfile.Profile()
        pr.enable()
        acceptCon(socket, lock)
        pr.disable()
        pr.dump_stats(f'profile_worker_{os.getpid()}.prof')



if __name__ == "__main__":

    server = Server(8000,2)

    server.start()

    # merge the profiling reports and print the statistics
    stats = pstats.Stats()
    for i in range(server.num):
        stats.add(f'profile_worker_{i+1}.prof')
    stats.sort_stats('cumulative').print_stats(20)