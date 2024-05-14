import socket
from vidstream import ScreenShareClient
import pyautogui
from screeninfo import get_monitors
import time
from pynput.mouse import Controller as MouseController
import ctypes
from server import encoding_sharing
from clientGUI import AuthApp  # Ensure this matches the filename where the class is defined

HOST = '10.100.102.32'
PORT = 4444
pyautogui.FAILSAFE = False

dec = encoding_sharing.EncryptionManager()


def get_taskbar_height():
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", ctypes.c_long),
            ("top", ctypes.c_long),
            ("right", ctypes.c_long),
            ("bottom", ctypes.c_long)
        ]

    hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    taskbar_height = rect.bottom - rect.top

    return taskbar_height


def get_your_screen_resolution():
    monitors = get_monitors()

    if monitors:
        primary_monitor = monitors[0]
        width = primary_monitor.width
        height = primary_monitor.height
        return width, height
    else:
        return 1920, 1080  # Default values


def receive_screen(HOST, PORT, client_socket):
    print('got in')
    data = client_socket.recv(1024).decode().split(",")
    print(data)
    width_server, height_server = int(data[0]), int(data[1])
    taskbar_height = get_taskbar_height()
    sender = ScreenShareClient(HOST, PORT - 1, width_server, height_server - taskbar_height)

    sender.start_stream()
    print("receiving screen")

    width, height = get_your_screen_resolution()
    client_socket.send(f'{width},{height},1'.encode())

    time.sleep(7)

    while True:
        xy1 = client_socket.recv(1024).decode()
        xy = xy1.split(",")
        x, y = float(xy[0]), float(xy[1])
        x = dec.decrypt_number(int(x))
        y = dec.decrypt_number(int(y))
        pressed = float(str(xy[2]))
        pressed = dec.decrypt_number(int(pressed))
        # print(x, y)
        pyautogui.moveTo(x, y)

        def scroll(steps):
            mouse = MouseController()
            mouse.scroll(0, steps)
        if not bool(pressed):
            pass
        elif pressed == 1:
            print("got left pressed")
        elif pressed == 2:
            print("got right pressed")
        elif pressed == 3:
            key = str(xy[3])
            key = dec.caesar_cipher_decrypt(key)
            print(f"{key} pressed")
            if key == 'q':
                break
        elif pressed == 4:
            key = str(xy[3])
            key = dec.caesar_cipher_decrypt(key)
            if key == 'up':
                print("scroll up")
            elif key == 'down':
                print("scroll down")
        client_socket.send("second".encode())
    sender.stop_stream()


def login_check(client_socket, data):
    if data.lower() == 'exit':
        return "exit"

    client_socket.send(data.encode('utf-8'))
    echoed_message = client_socket.recv(1024).decode('utf-8')
    return echoed_message


def connect_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("1")
    server_address = (HOST, PORT)
    print("2")
    try:
        client_socket.connect(server_address)
        print("connected")

        auth_app = AuthApp(client_socket)
        flag = True

        while True:
            if not flag:
                print('close flag=false ')
                break
            app_details = auth_app.login_screen()
            print(app_details)
            check = login_check(client_socket, app_details)
            print(app_details)
            if len(app_details.split(":")) == 3:
                break

            if check == "exit":
                auth_app.bye()
                break
            elif check != "bad":
                print(f"Server echoed: {check}")
                while True:
                    if not flag:
                        break
                    totp_code = auth_app.auth_encrypt_screen(check)
                    print('got message')
                    if totp_code == "exit":
                        flag = False
                        break
                    elif totp_code != "bad":
                        print("waiting for control")
                        receive_screen(HOST, PORT, client_socket)
                        print("out")
                        flag = False
                    else:
                        print('Incorrect number, closing connection')
                        flag = False
            else:
                auth_app.incorrect_details()
                break

    except Exception as e:
        error_message = f"Error connecting to the server: {e}"
        auth_app.show_error_message(error_message)

    finally:
        auth_app.show_end_message("Closing connection")
        client_socket.close()


if __name__ == "__main__":
    connect_server()
