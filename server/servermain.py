import socket
import DBhandle
import HashMD5 as md
import TOTPencrypt as tp
import threading
import time
import serverControl

HOST = "10.100.102.32"
PORT = 4444

users_list = []


def add_user(users_list, client_socket, client_address):
    users_list.append((client_socket, client_address))


def check_user_can_controlled(users_list, client_socket, client_address):
    return users_list and users_list[0] == (client_socket, client_address)


def remove_user(users_list, client_socket, client_address):
    users_list.remove((client_socket, client_address))


def login(data):
    username, password = data.decode('utf-8').split(':')
    return DBhandle.login(username, md.hash_pass(password))


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    try:
        flag = True
        while flag:
            data = client_socket.recv(1024)
            if not data:
                print('No data received, closing connection')
                break

            print(f"Received from {client_address}: {data.decode('utf-8')}")

            if login(data):
                while flag:
                    totp_code = tp.auth_code()
                    code = totp_code[1]
                    num = totp_code[0]

                    client_socket.send(
                        f'successful login, please enter the code: {code} to accept control by server'.encode())

                    totp_check = tp.auth_check(client_socket, client_address, num)

                    if totp_check == "exit":
                        flag = False
                        break
                    elif totp_check:
                        client_socket.send("best".encode())
                        time.sleep(2)
                        print('good code by client')

                        add_user(users_list, client_socket, client_address)

                        while not check_user_can_controlled(users_list, client_socket, client_address):
                            continue

                        if check_user_can_controlled(users_list, client_socket, client_address):
                            serverControl.share_screen(HOST, PORT, client_socket, client_address)

                        print("Sharing screen")
                        flag = False
                    else:
                        print('bad code by client, close connection')
                        client_socket.send("bad".encode())
                        flag = False
            else:
                client_socket.send("bad".encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print(f"Connection from {client_address} closed.")
        client_socket.close()
        remove_user(users_list, client_socket, client_address)


def start_server():
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
