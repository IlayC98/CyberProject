import tkinter as tk


class AuthApp:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.returning_message_to_server = []

    def auth_encrypt_screen(self, message):
        self.returning_message_to_server = []

        def logout():
            app.destroy()
            self.returning_message_to_server.append('exit')

        def auth_encrypt():
            message = entry_text.get()
            if message.lower() == 'exit' or not message:
                print(message)
                return 'exit'

            # Send the message to the server
            self.client_socket.send(message.encode('utf-8'))
            server_code_message = self.client_socket.recv(1024).decode('utf-8')
            response_label.config(text=f'The server sent: {server_code_message}')
            app.destroy()  # Destroy the window after login
            self.returning_message_to_server.append(server_code_message)
            return server_code_message

        app = tk.Tk()
        app.title("Authentication")
        app.geometry("1300x800")
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

        appbtn = tk.Button(app, text='continue', command=auth_encrypt)
        appbtn.grid(column=0, row=4)

        exitbtn = tk.Button(app, text='logout', command=logout)
        exitbtn.grid(column=0, row=5)

        app.mainloop()

        return self.returning_message_to_server[0]

    def login_screen(self):
        self.returning_message_to_server = []

        def register_screen():
            app.destroy()

            def register():
                new_username = entry_text_new_user.get()
                new_password = entry_text_new_pass.get()
                new_email = entry_text_email.get()

                # Here you can implement your registration logic
                # For example, you might want to store the new user information in a database

                print("New Username:", new_username)
                print("New Password:", new_password)
                print("Email:", new_email)

                message = f'{new_username}:{new_password}:{new_email}'
                self.returning_message_to_server.append(message)
                register_window.destroy()

            register_window = tk.Tk()
            register_window.title("Register")
            register_window.geometry("300x350")
            register_window.resizable(False, False)

            label_register = tk.Label(register_window, text="Register", font=('Arial Bold', 20))
            label_register.pack()

            label_new_user = tk.Label(register_window, text="New Username:")
            label_new_user.pack()
            entry_text_new_user = tk.StringVar()
            entry_new_user = tk.Entry(register_window, width=20, textvariable=entry_text_new_user)
            entry_new_user.pack()

            label_new_pass = tk.Label(register_window, text="New Password:")
            label_new_pass.pack()
            entry_text_new_pass = tk.StringVar()
            entry_new_pass = tk.Entry(register_window, width=20, textvariable=entry_text_new_pass, show='*')
            entry_new_pass.pack()

            label_email = tk.Label(register_window, text="Email:")
            label_email.pack()
            entry_text_email = tk.StringVar()
            entry_email = tk.Entry(register_window, width=20, textvariable=entry_text_email)
            entry_email.pack()

            register_button = tk.Button(register_window, text='Register', command=register)
            register_button.pack()

            register_window.mainloop()

        app = tk.Tk()
        app.title("Welcome")
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
            self.returning_message_to_server.append(message)

        appbtn = tk.Button(app, text='login', command=login)
        appbtn.grid(column=1, row=5)

        register_button = tk.Button(app, text='Register', command=register_screen)
        register_button.grid(column=1, row=6)

        app.mainloop()

        return self.returning_message_to_server[0]

    @staticmethod
    def bye():
        root = tk.Tk()
        root.geometry("300x300")

        label = tk.Label(root, text="bye bye")
        label.pack(pady=20)

        root.after(3000, root.destroy)
        root.mainloop()

    @staticmethod
    def incorrect_details():
        root = tk.Tk()
        root.geometry("500x300")

        error_label = tk.Label(root, text="Incorrect details or user already logged")
        error_label.pack(pady=20)

        root.after(3000, root.destroy)
        root.mainloop()

    @staticmethod
    def show_error_message(error_message):
        root = tk.Tk()
        root.geometry("1100x300")

        error_label = tk.Label(root, text=error_message)
        error_label.pack(pady=20)

        root.after(5000, root.destroy)
        root.mainloop()

    @staticmethod
    def show_end_message(message):
        root = tk.Tk()
        root.geometry("300x100")

        label = tk.Label(root, text=message)
        label.pack(pady=20)

        root.after(3000, root.destroy)
        root.mainloop()
