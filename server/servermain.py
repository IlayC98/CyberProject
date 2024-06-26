import socket
import DBhandle
import HashMD5 as md
import TOTPencrypt as tp
import threading
import time
import serverControl
import smtplib
import tkinter as tk


HOST = "10.100.102.32"
PORT = 4444

users_list = []

def user_want_control(data):
    username= data.decode('utf-8').split(':')[0]

    root = tk.Tk()
    root.geometry("500x300")

    error_label = tk.Label(root, text=f"{username} accepted control")
    error_label.pack(pady=20)

    # Schedule the window to close after 3000 milliseconds (3 seconds)
    root.after(300, root.destroy)

    root.mainloop()


def send_email_to_client(data, code):
    username=data.decode("utf-8").split(":")[0]
    receiver_email=DBhandle.get_email_by_username(username)
    # Set up SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # For Gmail
    smtp_username = 'test10098ilay@gmail.com'
    smtp_password = "gefa qrfn fjmp agae"

    # Create the email message
    from_address = smtp_username
    to_address = receiver_email
    subject = "code verification for control"
    body = f"successful login, please enter the code: {code} to accept control by server"

    # Combine the email message parts
    message = f"From: {from_address}\r\n"
    message += f"To: {to_address}\r\n"
    message += f"Subject: {subject}\r\n\n"
    message += body

    # Create a secure SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email
    server.sendmail(from_address, to_address, message)

    # Close the SMTP connection
    server.quit()
    print("Email sent successfully!")


class UserHandler:
    def __init__(self, users_list=None):
        if users_list is None:
            users_list = []
        self.users_list = users_list

    def user_connected(self, data):
        username = data.decode('utf-8').split(':')[0]
        return DBhandle.is_user_connected(username)

    def connected_client(self, data):
        username, password = data.decode('utf-8').split(':')
        DBhandle.connected(username)

    def disconnect_client(self, data):
        username = data.decode('utf-8').split(':')[0]
        DBhandle.disconnected(username)

    def add_user(self, data):
        username = data.decode('utf-8').split(':')[0]
        self.users_list.append(username)

    def check_user_can_controlled(self, data):
        username = data.decode('utf-8').split(':')[0]
        return self.users_list and self.users_list[0] == username

    def remove_user(self, data):
        username = data.decode('utf-8').split(':')[0]
        if username in self.users_list:
            self.users_list.remove(username)

    def login(self, data):
        username, password = data.decode('utf-8').split(':')
        return DBhandle.login(username, md.hash_pass(password))

    def register(self, data):
        username, password, email = data.decode('utf-8').split(':')
        return DBhandle.add_user(username, password, email, 0)


handle_user=UserHandler(users_list)


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

            if len(data.decode('utf-8').split(':'))==2:
                if not handle_user.user_connected(data):
                    handle_user.add_user(data)
                else:
                    print("user already connected")
                    client_socket.send("bad".encode())
                    break
                print(users_list)
                if handle_user.login(data):
                    handle_user.connected_client(data)
                    DBhandle.showDB()
                    while flag:
                        totp_code = tp.auth_code()
                        code = totp_code[1]
                        num = totp_code[0]
                        print(num+"  gvs  "+code)

                        send_email_to_client(data, code)
                        client_socket.send(
                            f'successful login, please enter the code sent to your email to accept control by server'.encode())

                        totp_check = tp.auth_check(client_socket, client_address, num)

                        if totp_check == "exit":
                            flag = False
                            break
                        elif totp_check:
                            client_socket.send("best".encode())
                            time.sleep(2)
                            print('good code by client')


                            while not handle_user.check_user_can_controlled(data):
                                continue

                            if handle_user.check_user_can_controlled(data):
                                # user_want_control(data)
                                serverControl.share_screen(HOST, PORT, client_socket, client_address)

                            print("Sharing screen")
                            flag = False
                        else:
                            print('bad code by client, close connection')
                            client_socket.send("bad".encode())
                            flag = False
                else:
                    client_socket.send("bad".encode())
                    break
            elif len(data.decode('utf-8').split(':'))==3:
                x=handle_user.register(data)
                if x:
                    client_socket.send("Registration went successfully".encode())

                else:
                    client_socket.send("username already exist".encode())
                print("here")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print(f"Connection from {client_address} closed.")
        client_socket.close()
        handle_user.remove_user(data)
        handle_user.disconnect_client(data)
        DBhandle.showDB()




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
    DBhandle.createDB()
    DBhandle.disconnect_all()
    DBhandle.showDB()
    start_server()