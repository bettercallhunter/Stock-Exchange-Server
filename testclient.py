import socket
import time
import xml.etree.ElementTree as ET
from multiprocessing import Process

processes = [] 
def sendString(sfile, string):
    sfile.write(str(len(string)))
    sfile.write(string)


def receiveResponse(sfile):
    num = sfile.readline()
    response = sfile.read(int(num))
    return ET.fromstring(response)

def one_client(file,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open(file, 'r') as f:
        input_string = f.read()
        # xml_string = input_string.split('\n', 1)[1].strip()
    # sfile = sock.makefile('rw', 1)
    # sendString(sfile, input_string)
    sock.sendall(input_string.encode())
    # response = receiveResponse(sfile)
    response = sock.recv(8192).decode()
    #print(response)
    sock.close()
    
def run_all(file,times,port):
    for i in range(times):
        one_client(file,port)
        if i==99:
            print(i)
def get_time(times, nums,port):
    print("testing times for " + str(times*nums))
    start_time = time.time()
    for i in range(nums):
        p = Process(target=run_all, args=('randomTransactions.xml', times,port))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    
    stop_time = time.time()
    diff = stop_time - start_time
    print("Time elapsed: " + str(diff))
    print("Speed is {} quries/s".format(times * nums / diff))

   
if __name__ == "__main__":
    get_time(100,4,8000)