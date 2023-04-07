
import socket
def one_client(file, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("0.0.0.0", port))
    with open("randomTransactions.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())
    response = sock.recv(8192).decode()
    print(response)
    sock.close()

one_client('randomTransactions.xml',12345)