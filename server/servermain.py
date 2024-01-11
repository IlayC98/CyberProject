import socket
import threading
import DBhandle
import HashMD5 as md
import TOTPencrypt as tp
import threading
from vidstream import ScreenShareClient

HOST = '127.0.0.1'
PORT = 4444

def share_screen(HOST, PORT):
    print(f'got in')
    server = ScreenShareClient(HOST,PORT)
    print(f'start sharing')

    t = threading.Thread(target=server.start_stream)
    t.start()
    print('threading')

    while input("") != 'STOP':
        continue

    print("HELLO")

    # Other Code

    # When You Are Done
    server.stop_stream()


def login(data):
    username, password = data.decode('utf-8').split(':')
    return DBhandle.login(username, md.hash_pass(password))

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    flag=True

    while True:
        if not flag:
            print('close flag=false ')
            break
        # Get username and password from client
        data = client_socket.recv(1024)
        if not data:
            print('close no data')
            break
        print(f"Received from {client_address}: {data.decode('utf-8')}")
        # Check if username and password are correct
        if login(data):
            while True:
                if not flag:
                    break
                totp_code=tp.auth_code()
                code=totp_code[1]
                num=totp_code[0]
                client_socket.send(f'successful login, please enter the code: {code} to accept control by server'.encode())
                totp_check=tp.auth_check(client_socket, client_address, num)
                if totp_check=="exit":
                    flag=False
                    break
                elif totp_check:
                    print('good code by client')
                    share_screen(HOST,PORT)
                    print("sharing screen")
                else:
                    print('bad code by client, close connection')
                    client_socket.send("bad".encode())
                    flag=False
        # if not correct username or password it returns to the start and get again username, password from client
        else:
            client_socket.send("bad".encode())
    # if client wrote exit or no data it will close the connection with him and the server
    print(f"Connection from {client_address} closed.")
    client_socket.close()

def start_server():
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server listening on port ", PORT)

    while True:
        client, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()

