
# import database
import socket
import sys
sys.path.append('../')
from database import *
import xml.etree.ElementTree as ET


engine = create_engine("postgresql://postgres:0000@localhost:5432/stock")
Session = sessionmaker(bind=engine)


def test1(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open("create1.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())

    response = sock.recv(8192).decode()
    print(response)
    sock.close()


def test2(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open("create2.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())

    response = sock.recv(8192).decode()
    print(response)
    sock.close()


def check1():
    session = Session()
    account123456 = session.query(Account).filter_by(id="123456").first()
    account654321 = session.query(Account).filter_by(id="654321").first()
    assert account123456 is not None
    assert account123456.balance == 1000
    assert account123456.position["SYA"] == "100"
    assert account654321 is not None
    assert account654321.balance == 1000
    assert not account654321.position
    print("test1 passed")


def check2():
    session = Session()
    account123456 = session.query(Account).filter_by(id="123456").first()
    account654321 = session.query(Account).filter_by(id="654321").first()
    assert account123456 is not None
    assert account123456.balance == 1000
    assert str(account123456.position["SYA"]) == "200"
    assert str(account123456.position["SYB"]) == "200"
    assert str(account123456.position["SYC"]) == "200"
    assert account654321 is not None
    assert account654321.balance == 1000
    assert account654321.position["SYA"] == "100"
    assert account654321.position["SYB"] == "100"
    assert account654321.position["SYC"] == "100"

    print("test2 passed")


def test3(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open("transactions1.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())

    response = sock.recv(8192).decode()
    print(response)
    sock.close()


def check3():
    session = Session()
    account123456 = session.query(Account).filter_by(id="123456").first()
    account654321 = session.query(Account).filter_by(id="654321").first()
    assert account123456 is not None
    assert account123456.balance == 500
    assert str(account123456.position["SYA"]) == "10"
    assert str(account123456.position["SYB"]) == "200"
    assert str(account123456.position["SYC"]) == "200"
    assert account654321 is not None
    assert account654321.balance == 1000
    assert account654321.position["SYA"] == "100"
    assert account654321.position["SYB"] == "100"
    assert account654321.position["SYC"] == "100"

    order1 = session.query(Open).filter_by(id=1).first()
    assert order1 is not None
    assert order1.account_id == 123456
    assert order1.sym == "SYA"
    assert order1.limit == 60
    assert order1.amount == -100
    order2 = session.query(Open).filter_by(id=2).first()
    assert order2 is not None
    assert order2.account_id == 123456
    assert order2.sym == "SYB"
    assert order2.limit == 10
    assert order2.amount == 40
    order3 = session.query(Open).filter_by(id=3).first()
    assert order3 is not None
    order4 = session.query(Open).filter_by(id=4).first()
    assert order4 is not None
    print("test3 passed")


def test4(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open("transactions2.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())

    response = sock.recv(8192).decode()
    print(response)
    sock.close()
def check4():
    session = Session()
    account123456 = session.query(Account).filter_by(id="123456").first()
    account654321 = session.query(Account).filter_by(id="654321").first()
    assert account123456 is not None
    assert account123456.balance == 800
    assert str(account123456.position["SYA"]) == "10"
    assert str(account123456.position["SYB"]) == "240"
    assert str(account123456.position["SYC"]) == "200"
    assert account654321 is not None
    assert account654321.balance == 600
    assert str(account654321.position["SYA"]) == "105"
    assert str(account654321.position["SYB"]) == "60"
    assert str(account654321.position["SYC"]) == "100"
    open1 = session.query(Open).filter_by(id=1).first()
    assert open1.amount == -95
    open2 = session.query(Open).filter_by(id=2).first()
    assert open2 is None
    open5 = session.query(Open).filter_by(id=5).first()
    assert open5.sym == "SYA"
    assert open5.amount == 50
    assert open5.limit == 10
    assert open5.account_id == 654321
    executed1 = session.query(Executed).filter_by(id=1).first()
    assert executed1.transId == 2
    executed2 = session.query(Executed).filter_by(id=2).first()
    assert executed2.transId == 5
    executed3 = session.query(Executed).filter_by(id=3).first()
    assert executed3.transId == 6
    executed4 = session.query(Executed).filter_by(id=4).first()
    assert executed4.transId == 1
    print("test4 passed")

def test5(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", port))
    with open("transactions3.xml", 'r') as f:
        input_string = f.read()

    sock.sendall(input_string.encode())

    response = sock.recv(8192).decode()
    print(response)
    sock.close()
    return response
def check5(response):
    session = Session()
    account123456 = session.query(Account).filter_by(id="123456").first()
    assert account123456.balance == 800
    assert str(account123456.position["SYA"]) == "105"
    root = ET.fromstring(response)
    status_list=[]
    open_shares_list=[]
    cancel_shares_list=[]
    executed_shares_list=[]
    cancal_id_list=[]
    for status_elem in root.findall('status'):
        status_id = status_elem.get('id')
        status_list.append(status_id)       
        open_elem = status_elem.find('open')
        if open_elem is not None:
            open_shares = open_elem.get('shares')
            open_shares_list.append(open_shares)
        canceled_elem = status_elem.find('canceled')
        if canceled_elem is not None:
            canceled_shares = canceled_elem.get('shares')
            cancel_shares_list=cancel_shares_list.append(canceled_shares)
        executed_elem = status_elem.find('executed')
        if executed_elem is not None:
            executed_shares = executed_elem.get('shares')
            executed_shares_list.append(executed_shares)
    for canceled_elem in root.findall('canceled'):
        canceled_id = canceled_elem.get('id')
        cancal_id_list.append(canceled_id)
    assert status_list == ['1', '1', '4', '4']
    assert open_shares_list == ['-95', '-90','-90']
    assert executed_shares_list == ['5', '5']
    assert cancal_id_list ==['1']
    print("passed test5")

def run_tests(port):      
    test1(port)
    check1()
    test2(port)
    check2()
    test3(port)
    check3()
    test4(port)
    check4()
    response = test5(port)
    check5(response)

if __name__ == "__main__":
    run_tests(8000)

# assert
