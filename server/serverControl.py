import pyautogui
import win32api
from screeninfo import get_monitors
from vidstream import StreamingServer
import keyboard
import time
from pynput import mouse
import ctypes
from encoding_sharing import EncryptionManager

enc= EncryptionManager()


mouse_keys = [win32api.GetKeyState(0x01), win32api.GetKeyState(0x02)]
keyboard_keys = (
    "Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
    "`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace",
    "Tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\",
    "Caps Lock", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "Enter",
    "Shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "Shift",
    "Ctrl", "Win", "Alt", "Space", "AltGr", "Win", "Menu", "Ctrl",
    "Print Screen", "Scroll Lock", "Pause",
    "Insert", "Home", "Page Up", "Delete", "End", "Page Down",
    "Up", "Left", "Down", "Right",
    "Num Lock", "/", "*", "-", "+", "Enter", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "Decimal"
)


def left_button_pressed(state_left):
    a = win32api.GetKeyState(0x01)
    left_button_got_pressed = False

    if a != state_left:  # Button state changed
        state_left = a
        #print(a)
        if a < 0:
            #print('Left Button Pressed')
            left_button_got_pressed = True
        else:
            #print('Left Button Released')
            left_button_got_pressed = False

    return left_button_got_pressed

def right_button_pressed(state_right):
    b = win32api.GetKeyState(0x02)
    right_button_got_pressed = False

    if b != state_right:  # Button state changed
        state_right = b
        #print(b)
        if b < 0:
            #print('Right Button Pressed')
            right_button_got_pressed = True
        else:
            #print('Right Button Released')
            right_button_got_pressed = False

    return right_button_got_pressed

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
    monitors = get_monitors()

    if monitors:
        primary_monitor = monitors[0]
        width = primary_monitor.width
        height = primary_monitor.height
        return width, height
    else:
        return 1920, 1080  # Default values

def share_screen(HOST, PORT, client_socket, client_address):
    print(f'Got in')
    width, height = get_your_screen_resolution()
    taskbar_height = get_taskbar_height()
    client_socket.send(f'{width},{height-taskbar_height},1'.encode())

    host = StreamingServer(HOST, PORT-1)
    host.start_server()

    data = client_socket.recv(1024).decode().split(",")
    width_client, height_client = float(data[0]), float(data[1])
    print(width_client, height_client)
    print(width, height)
    ratio_width = width_client / width
    ratio_height = (height_client) / (height-taskbar_height)


    while True:
        try:
            currentMouseX, currentMouseY = pyautogui.position()
            mouse_x = float(currentMouseX * ratio_width)
            mouse_y = float(currentMouseY * ratio_height)

            if mouse_y< height_client/2: mouse_y-=17
            else: mouse_y+=2

            encoding_x = enc.encrypt_number(int(mouse_x))
            encoding_y = enc.encrypt_number(int(mouse_y))
            def on_scroll(x, y, dx, dy):
                if dy > 0:
                    print('Mouse scrolled up')
                    client_socket.send(f'{encoding_x},{encoding_y},{enc.encrypt_number(4)},{enc.caesar_cipher_encrypt("up")}'.encode())

                elif dy < 0:
                    print('Mouse scrolled down')
                    client_socket.send(f'{encoding_x},{encoding_y},{enc.encrypt_number(4)},{enc.caesar_cipher_encrypt("down")}'.encode())

            with mouse.Listener(on_scroll=on_scroll) as listener:
                # Wait for 2 seconds
                time.sleep(0.2)
                # Stop the listener after 2 seconds
                listener.stop()

            for i in keyboard_keys:

                if keyboard.is_pressed(i):
                    client_socket.send(f'{encoding_x},{encoding_y},{enc.encrypt_number(3)},{enc.caesar_cipher_encrypt(i)}'.encode())
                    print(f"Sent {i}")

            if left_button_pressed(mouse_keys[0]):
                print("Left click")
                client_socket.send(f'{encoding_x},{encoding_y},{enc.encrypt_number(1)}'.encode())
                print("Sent True")
            elif right_button_pressed(mouse_keys[1]):
                print("Right click")
                client_socket.send(f'{encoding_x},{encoding_y},{enc.encrypt_number(2)}'.encode())
            else:
                client_socket.send(f'{encoding_x},{encoding_y},{enc.encrypt_number(0)}'.encode())

            res = client_socket.recv(1024).decode()

        except Exception as e:
            print(f"Error in share_screen: {e}")
            break

    host.stop_server()
    print("Screen sharing stopped")

# If this code is meant to be part of a larger program, make sure to integrate it properly with your existing codebase.