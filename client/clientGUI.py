import tkinter as tk
from tkinter import ttk


def auth_encrypt_screen(client_socket, message):
    def auth_encrypt():
        message = entry_text.get()
        if message.lower() == 'exit' or not message:
            return 'exit'

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))
        server_code_message = client_socket.recv(1024).decode('utf-8')
        response_label.config(text=f'The server sent: {server_code_message}')
        app.destroy()  # Destroy the window after login
        return server_code_message

    app = tk.Tk()
    app.title("Authentication")
    app.geometry("1100x600")
    app.resizable(False, False)

    label1 = tk.Label(app, text=message, font=('Arial Bold', 14))
    label1.grid(column=0, row=0)

    label1 = tk.Label(app, text="Enter the code:", font=('Arial Bold', 16))
    label1.grid(column=0, row=1)

    entry_text = tk.StringVar()
    entry = tk.Entry(app, width=20, textvariable=entry_text)
    entry.grid(column=0, row=2, padx=10, pady=5)
    entry.focus()

    response_label = tk.Label(app, text='', font=('Arial', 12))
    response_label.grid(column=0, row=3, padx=10, pady=5)

    x = auth_encrypt
    appbtn = tk.Button(app, text='continue', command=x)
    appbtn.grid(column=0, row=4)

    app.mainloop()

    # This line is executed after the mainloop exits
    return x


def login_screen():
    app = tk.Tk()
    app.title("Remote RUN")
    app.geometry("500x500")
    app.resizable(False, False)

    label1 = tk.Label(app, text="Login", font=('Arial Bold', 50))
    label1.grid(column=1, row=0)

    label2 = tk.Label(app, text="User")
    label2.grid(column=1, row=1)

    entry_text_user = tk.StringVar()
    entry_user = tk.Entry(app, width=20, textvariable=entry_text_user)
    entry_user.grid(column=1, row=2, padx=10, pady=5)
    entry_user.focus()

    label3 = tk.Label(app, text="Password")
    label3.grid(column=1, row=3)

    entry_text_pass = tk.StringVar()
    entry_pass = tk.Entry(app, width=20, textvariable=entry_text_pass, show='*')
    entry_pass.grid(column=1, row=4, padx=10, pady=5)

    def login():
        username, password = entry_text_user.get(), entry_text_pass.get()
        message = f'{username}:{password}'
        app.destroy()  # Destroy the window after login
        return message

    appbtn = tk.Button(app, text='login', command=login)
    appbtn.grid(column=1, row=5)

    app.mainloop()

    username, password = entry_text_user.get(), entry_text_pass.get()
    message = f'{username}:{password}'

    # This line is executed after the mainloop exits
    return message  # Return the username and password



# def show_waiting_screen(client_socket, server_address):
#     print("f")
#     root = tk.Tk()
#     root.title("Waiting Screen")
#     root.geometry("500x300")
#
#     label = tk.Label(root, text="Connecting to server...")
#     label.pack(pady=10)
#
#     progressbar = ttk.Progressbar(root, mode='indeterminate')
#     progressbar.pack(fill='x', padx=20, pady=5)
#     progressbar.start(10)
#
#     try:
#         # Connect to the server
#         print(bool(client_socket.connect(server_address)))
#         print("Connected")
#         root.destroy()
#
#     except ConnectionRefusedError:
#         print("hi")  # Retry connection if failed
#
#     root.mainloop()
#     return root
#
# def close_waiting_screen(root):
#     root.destroy()


def bye():
    root = tk.Tk()
    root.geometry("200x100")

    label = tk.Label(root, text="bye bye")
    label.pack(pady=20)

    # Schedule the window to close after 3000 milliseconds (3 seconds)
    root.after(3000, root.destroy)

    root.mainloop()

def incorrect_details():
    root = tk.Tk()
    root.geometry("300x100")

    error_label = tk.Label(root, text="Incorrect username or password, please try again")
    error_label.pack(pady=20)

    # Schedule the window to close after 3000 milliseconds (3 seconds)
    root.after(3000, root.destroy)

    root.mainloop()


def show_error_message(error_message):
    root = tk.Tk()
    root.geometry("400x100")

    error_label = tk.Label(root, text=error_message)
    error_label.pack(pady=20)

    # Schedule the window to close after 5000 milliseconds (5 seconds)
    root.after(5000, root.destroy)

    root.mainloop()

def show_end_message(message):
    root = tk.Tk()
    root.geometry("300x100")

    label = tk.Label(root, text=message)
    label.pack(pady=20)

    # Schedule the window to close after 3000 milliseconds (3 seconds)
    root.after(3000, root.destroy)

    root.mainloop()