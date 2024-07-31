import socket
from datetime import datetime

def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to server using JKPQ Protocol")

    # Login process
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Send username and password to the server
    client_socket.sendall(f"{username}\n".encode())
    client_socket.sendall(f"{password}\n".encode())

    # Receive login response from the server
    login_response = client_socket.recv(1024).decode()
    print(f"Server response: {login_response}")

    if "Login successful" not in login_response:
        print("Login failed. Closing connection.")
        client_socket.close()
        return

    # If login successful, continue with the booking process
    while True:
        message = input("Enter message to send (or 'QUIT' to exit): ")
        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_socket.sendall(message.encode())
        print(f"[{send_time}] Sent to server: {message}")

        if message == "QUIT":
            break

        response = client_socket.recv(1024).decode()
        receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{receive_time}] Received from server: {response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
