import socket
from vidstream import ScreenShareClient
from pynput.mouse import Button,Controller
import pyautogui
from screeninfo import get_monitors
import time

HOST = '10.100.102.32'
PORT = 4444
pyautogui.FAILSAFE=False


def get_your_screen_resolution():
    # Get the screen resolution of the primary monitor
    monitors = get_monitors()

    if monitors:
        primary_monitor = monitors[0]
        width = primary_monitor.width
        height = primary_monitor.height
        return width, height
    else:
        # Default values if no monitors are found
        return 1920, 1080  # Update with your default values

def receive_screen(HOST,PORT, client_socket):
    print(f'got in')
    data= client_socket.recv(1024).decode().split(",")
    print(data)
    width_server, height_server=int(data[0]), int(data[1])
    sender = ScreenShareClient(HOST, PORT-1, width_server,height_server)

    sender.start_stream()
    print("receiving screen")

    width, height=get_your_screen_resolution()[0],get_your_screen_resolution()[1]
    client_socket.send(f'{width},{height},1'.encode())

    time.sleep(5)

    while True:
        xy1=client_socket.recv(1024).decode()
        # print(xy1)
        xy=xy1.split(",")
        x,y=int(xy[0]),int(xy[1])
        pressed=int(str(xy[2]))
        # print(x,y)
        pyautogui.moveTo(x,y)
        if bool(pressed):
            print("got pressed")
        #     pyautogui.click(x,y)
        client_socket.send("second".encode())
    sender.stop_stream()


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

    if message.lower() == 'exit' or not message:
        return 'exit'

    # Send the message to the server
    client_socket.send(message.encode('utf-8'))
    server_code_message = client_socket.recv(1024).decode('utf-8')
    print(f'the server sent {server_code_message}')
    return server_code_message


def connect_server():
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    try:
        # Connect to the server
        client_socket.connect(server_address)
        print("connected")
        # pyautogui.moveTo(100, 150)

        flag = True

        while True:
            if not flag:
                print('close flag=false ')
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
                    print('got message')
                    if totp_code == "exit":
                        flag = False
                        break
                    elif totp_code != "bad":
                        print("waiting for control")
                        while client_socket.recv().decode('utf8') != 'now can join': client_socket.send("ok".encode())
                        receive_screen(HOST,PORT,client_socket)
                        flag = False
                    else:
                        print('Incorrect number, closing connection')
                        flag=False

            else:
                print('Incorrect username or password, please try again')

    except Exception as e:
        print(f"Error connecting to the server: {e}")

    finally:
        # Close the connection
        print('Closing connection')
        client_socket.close()


if __name__ == "__main__":
    connect_server()