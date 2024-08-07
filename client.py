import socket
from datetime import datetime
from encrypt import encrypt_message, decrypt_message
from protocol import protocol_handler

def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server using 6510450399 Protocol")

    username = input("Enter username: ")
    password = input("Enter password: ")

    client_socket.sendall(encrypt_message(username))
    client_socket.sendall(encrypt_message(password))

    encrypted_login_response = client_socket.recv(1024)
    login_response = decrypt_message(encrypted_login_response)
    protocol_handler(login_response)
    # print(f"Server response: {login_response1}")

    if "Login successful" not in login_response:
        print("Login failed. Closing connection.")
        client_socket.close()
        return

    while True:
        message = input("Enter message to send (or 'quit' to exit): ")
        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        encrypted_message = encrypt_message(message)
        client_socket.sendall(encrypted_message)
        print(f"[{send_time}] Sent to server: {message}")

        if message == "quit":
            break

        encrypted_response = client_socket.recv(1024)
        response = decrypt_message(encrypted_response)
        protocol_handler(response)
        # receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(f"[{receive_time}] Received from server: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
