import socket
import time
import xml.etree.ElementTree as ET
from multiprocessing import Process
import statistics

def sendString(sfile, string):
    sfile.write(str(len(string)))
    sfile.write(string)


def receiveResponse(sfile):
    num = sfile.readline()
    response = sfile.read(int(num))
    return ET.fromstring(response)


def one_client(file, port):
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
    # print(response)
    sock.close()


def run_all(file, times, port):
    for i in range(times):
        one_client(file,port)
def get_time(times, nums,port):
    processes = [] 
    # print("total core number: " + str(1))
    print("total request number: " + str(times*nums))
    start_time = time.time()
    for i in range(nums):
        p = Process(target=run_all, args=(
            'randomTransactions.xml', times, port))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    stop_time = time.time()
    diff = stop_time - start_time
    throughput = times * nums / diff
    print("total running time: " + str(diff) + "s")
    print("throughput is {} request/s".format(throughput))
    return throughput


if __name__ == "__main__":
    print("total core number: " + str(4))
    results = []
    for i in range(10):
        throughput = get_time(1000,4,8000)
        print()
        results.append(throughput)
    avg_time = statistics.mean(results)
    std_dev = statistics.stdev(results)
    print("total core number: " + str(4))
    print("average throughput by running 10 times is {} request/s".format(avg_time))
    print("Standard deviation:", std_dev)
