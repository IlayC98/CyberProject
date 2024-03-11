import pyautogui
import win32api
from screeninfo import get_monitors
from vidstream import StreamingServer

# mouse_keys =[0]*2
state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
state_right = win32api.GetKeyState(0x02)  # Right button down = 0 or 1. Button up = -127 or -128
# mouse_keys[0] = state_left

def left_button_pressed(state_left):

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
    return left_button_pressed


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
    width, height=get_your_screen_resolution()[0],get_your_screen_resolution()[1]
    client_socket.send(f'{width},{height},1'.encode())
    host = StreamingServer(HOST, PORT-1)
    host.start_server()

    data = client_socket.recv(1024).decode().split(",")
    width_client, height_client = int(data[0]), int(data[1])
    print(width_client,height_client)
    print(width,height)
    ratio_width=width_client/width
    ratio_height=height_client/height

    while True:
        try:
            currentMouseX, currentMouseY = pyautogui.position()
            # print("current mouse:",currentMouseX,currentMouseY)


            mouse_x=int(currentMouseX*ratio_width)
            mouse_y=int(currentMouseY*ratio_height)-20

            # print("mouse on client:", mouse_x, mouse_y)
            # Check if the left mouse button is pressed
            if left_button_pressed(state_left):
                print("on click")
                # Send message with additional information when the left button is pressed
                client_socket.send(f'{mouse_x},{mouse_y},1'.encode())
                print("sent True")
            else:
                client_socket.send(f'{mouse_x},{mouse_y},0'.encode())
                # print("sent False")

            res = client_socket.recv(1024).decode()
            # print(res)

        except Exception as e:
            print(f"Error in share_screen: {e}")
            break


    host.stop_server()
    print("Screen sharing stopped")
