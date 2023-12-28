import pyotp
def auth_check(client_socket, client_address, secret):
    # Verify a TOTP code
    user_provided_code = client_socket.recv(1024).decode('utf-8')
    if not user_provided_code: return "exit"
    totp = pyotp.TOTP(secret, interval=300)
    is_valid = totp.verify(user_provided_code)

    print(f"Expected Code: {totp.now()}")
    print(f"User Code: {user_provided_code}")

    if is_valid:
        print(f"{client_address} Code is valid!")
    else:
        print(f"{client_address} Code is not valid.")
    return is_valid

def auth_code():
    # Generate a new TOTP secret
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    secret = totp.secret

    # Get the current TOTP code
    current_code = totp.now()
    print(f"Current TOTP Code: {current_code}")

    return secret, current_code
