import socket

HOST = '127.0.0.1'
PORT = 4444


def login():
    username = input('enter username')
    password = input('enter password')
    message = f'{username}:{password}'
    return message


def login_check(client_socket, data):
    if data.lower() == 'exit':
        return "exit"

    # Send the message to the server
    client_socket.send(data.encode('utf-8'))

    # Receive and print the echoed message from the server
    echoed_message = client_socket.recv(1024).decode('utf-8')
    return echoed_message


def auth_encrypt(client_socket):
    message = input("Enter the code (or 'exit' to quit): ")

    if message.lower() == 'exit':
        return 'exit'

    # Send the message to the server
    client_socket.send(message.encode('utf-8'))
    server_code_message = client_socket.recv(1024).decode('utf-8')
    return server_code_message


def connect_server():
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    # Connect to the server
    client_socket.connect(server_address)

    flag = True

    while True:
        if not flag:
            break
        details = login()
        # check if server logged client in or not
        check = login_check(client_socket, details)
        if check == "exit":
            break
        elif check != "bad":
            print(f"Server echoed: {check}")
            while True:
                if not flag:
                    break
                # check if the client code sent was right for the server
                totp_code = auth_encrypt(client_socket)
                if totp_code == "exit":
                    flag = False
                    break
                elif totp_code != "bad":
                    while True:
                        print("waiting for control")
                        break
                else:
                    print('Incorrect number, please try again')

        else:
            print('Incorrect username or password, please try again')

    # Close the connection
    client_socket.close()


if __name__ == "__main__":
    connect_server()
