import socket
import DBhandle
import HashMD5 as md
import TOTPencrypt as tp
import threading
from vidstream import StreamingServer
import time
import pyautogui
import win32api
from screeninfo import get_monitors

HOST = '172.20.157.38'
PORT = 4444


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


def share_screen(HOST, PORT, client_socket, client_address):
    print(f'got in')
    print(f'{get_your_screen_resolution()[0]},{get_your_screen_resolution()[1]}')
    client_socket.send(f'{get_your_screen_resolution()[0]},{get_your_screen_resolution()[1]},1'.encode())
    host = StreamingServer(HOST, PORT-1)
    host.start_server()

    state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
    state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128

    while True:
        try:
            currentMouseX, currentMouseY = pyautogui.position()
            a = win32api.GetKeyState(0x01)
            b = win32api.GetKeyState(0x02)
            left_button_pressed = False
            if a != state_left:  # Button state changed
                state_left = a
                print(a)
                if a < 0:
                    print('Left Button Pressed')
                    left_button_pressed = True
                else:
                    print('Left Button Released')
                    left_button_pressed = False


            # Check if the left mouse button is pressed
            if left_button_pressed:
                print("on click")
                # Send message with additional information when the left button is pressed
                client_socket.send(f'{currentMouseX},{currentMouseY},1'.encode())
                print("sent True")
            else:
                client_socket.send(f'{currentMouseX},{currentMouseY},0'.encode())
                # print("sent False")

            res = client_socket.recv(1024).decode()
            # print(res)

        except Exception as e:
            print(f"Error in share_screen: {e}")
            break


    host.stop_server()
    print("Screen sharing stopped")

def login(data):
    username, password = data.decode('utf-8').split(':')
    return DBhandle.login(username, md.hash_pass(password))

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    # pyautogui.moveTo(100, 150)
    try:
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
                        client_socket.send("best".encode())
                        time.sleep(2)
                        print('good code by client')
                        share_screen(HOST,PORT, client_socket, client_address)
                        print("sharing screen")
                        flag=False
                    else:
                        print('bad code by client, close connection')
                        client_socket.send("bad".encode())
                        flag=False
            # if not correct username or password it returns to thestart and get again username, password from client
            else:
                client_socket.send("bad".encode())
    except Exception as e:
        print(f"Error handling client: {e}")

    finally:
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