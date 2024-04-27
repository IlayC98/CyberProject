import pyautogui
import win32api
from screeninfo import get_monitors
from vidstream import StreamingServer
import keyboard
import time

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
    client_socket.send(f'{width},{height},1'.encode())

    host = StreamingServer(HOST, PORT-1)
    host.start_server()

    data = client_socket.recv(1024).decode().split(",")
    width_client, height_client = int(data[0]), int(data[1])
    print(width_client, height_client)
    print(width, height)
    ratio_width = width_client / width
    ratio_height = height_client / height


    while True:
        try:
            currentMouseX, currentMouseY = pyautogui.position()
            mouse_x = int(currentMouseX * ratio_width)
            mouse_y = int(currentMouseY * ratio_height) - 20

            for i in keyboard_keys:
                if keyboard.is_pressed(i):
                    client_socket.send(f'{mouse_x},{mouse_y},3,{i}'.encode())
                    print(f"Sent {i}")
                    time.sleep(0.2)
                    # print(f"{i} is pressed")

            if left_button_pressed(mouse_keys[0]):
                print("Left click")
                client_socket.send(f'{mouse_x},{mouse_y},1'.encode())
                print("Sent True")
            elif right_button_pressed(mouse_keys[1]):
                print("Right click")
                client_socket.send(f'{mouse_x},{mouse_y},2'.encode())
            else:
                client_socket.send(f'{mouse_x},{mouse_y},0'.encode())

            res = client_socket.recv(1024).decode()

        except Exception as e:
            print(f"Error in share_screen: {e}")
            break

    host.stop_server()
    print("Screen sharing stopped")

# If this code is meant to be part of a larger program, make sure to integrate it properly with your existing codebase.
