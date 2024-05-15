import socket
from vidstream import ScreenShareClient
import tkinter as tk
from tkinter import ttk
import pyautogui
from screeninfo import get_monitors
import time
import clientGUI as cgui
from pynput.mouse import Controller as MouseController
import ctypes
from server import encoding_sharing

dec=encoding_sharing.EncryptionManager()


HOST = '10.100.102.32'
PORT = 4444
pyautogui.FAILSAFE=False


def get_taskbar_height():
    # Define the RECT structure
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long)
        ]

    # Get the handle to the taskbar window
    hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)

    # Get the dimensions of the taskbar window
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))

    # Calculate the height of the taskbar
    taskbar_height = rect.bottom - rect.top

    return taskbar_height


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
    taskbar_height = get_taskbar_height()
    sender = ScreenShareClient(HOST, PORT-1, width_server,height_server-taskbar_height)

    sender.start_stream()
    print("receiving screen")

    width, height=get_your_screen_resolution()[0],get_your_screen_resolution()[1]
    client_socket.send(f'{width},{height},1'.encode())

    time.sleep(7)

    while True:
        xy1=client_socket.recv(1024).decode()
        # print(xy1)
        xy=xy1.split(",")
        x,y=float(xy[0]),float(xy[1])
        x= dec.decrypt_number(int(x))
        y= dec.decrypt_number(int(y))
        # print(y)
        pressed=float(str(xy[2]))
        pressed=dec.decrypt_number(int(pressed))
        print(x,y)
        pyautogui.moveTo(x,y)
        # Function to simulate mouse scrolling
        def scroll(steps):
            mouse = MouseController()
            mouse.scroll(0, steps)
        if not bool(pressed):
            pass
        elif pressed==1:
            print("got left pressed")
        #     pyautogui.click(x,y)
        elif pressed==2:
            print("got right pressed")
        #     pyautogui.click(x,y, button='right')
        elif pressed==3:
            print(xy)
            key=str(xy[3])
            key=dec.caesar_cipher_decrypt(key)
            print(f"{key} pressed")
            # pyautogui.press(key)
            if key=='q':
                break
        elif pressed==4:
            print(xy)
            key=str(xy[3])
            key=dec.caesar_cipher_decrypt(key)
            print(f"{key} pressed")
            if key=='up':
                print("scroll up")
                # scroll(1)  # Scroll up
            elif key=='down':
                print("scroll down")
                # scroll(-1)  # Scroll down
        client_socket.send("second".encode())
    sender.stop_stream()


def login_check(client_socket, data):
    if data.lower() == 'exit':
        return "exit"

    # Send the message to the server
    client_socket.send(data.encode('utf-8'))

    # Receive and print the echoed message from the server
    echoed_message = client_socket.recv(1024).decode('utf-8')
    return echoed_message


def connect_server():
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("1")
    server_address = (HOST, PORT)
    print("2")
    try:
        # waiting_screen = cgui.show_waiting_screen(client_socket, server_address)
        client_socket.connect(server_address)
        # Connect to the server
        print("connected")
        # pyautogui.moveTo(100, 150)

        flag = True

        while True:
            if not flag:
                print('close flag=false ')
                break
            app_details = cgui.login_screen()
            print(app_details)
            #check if the server logged in or not
            check = login_check(client_socket, app_details)
            print(app_details)
            if len(app_details.split(":"))==3: break

            if check == "exit":
                cgui.bye()
                break
            elif check != "bad":
                print(f"Server echoed: {check}")
                while True:
                    if not flag:
                        break
                    # check if the client code sent was right for the server
                    totp_code = cgui.auth_encrypt_screen(client_socket, check)
                    print('got message')
                    if totp_code == "exit":
                        flag = False
                        break
                    elif totp_code != "bad":
                        print("waiting for control")
                        #while client_socket.recv().decode('utf8') != 'now can join': client_socket.send("ok".encode())
                        receive_screen(HOST,PORT,client_socket)
                        print("out")
                        flag = False
                    else:
                        print('Incorrect number, closing connection')
                        flag=False

            else:
                cgui.incorrect_details()
                break

    except Exception as e:
        error_message = f"Error connecting to the server: {e}"
        cgui.show_error_message(error_message)

    finally:
        # Close the connection
        cgui.show_end_message("Closing connection")
        client_socket.close()


if __name__ == "__main__":
    connect_server()