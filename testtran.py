import socket


def test3(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open("testing/transactions3.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())

    response = sock.recv(8192).decode()
    print(response)
    sock.close()


test3(8000)
