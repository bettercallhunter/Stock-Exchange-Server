import socket

import xml.etree.ElementTree as ET


def sendString(sfile, string):
    sfile.write(str(len(string)))
    sfile.write(string)


def receiveResponse(sfile):
    num = sfile.readline()
    response = sfile.read(int(num))
    return ET.fromstring(response)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 8000))
    with open('randomTransactions.xml', 'r') as f:
        input_string = f.read()
        # xml_string = input_string.split('\n', 1)[1].strip()
    # sfile = sock.makefile('rw', 1)
    # sendString(sfile, input_string)
    sock.sendall(input_string.encode())
    # response = receiveResponse(sfile)
    response = sock.recv(8192).decode()
    print(response)

    sock.close()
