import socket
import threading
from datetime import datetime
from security import login, movies
from board import print_board
from encrypt import encrypt_message, decrypt_message

# Initialize a lock for thread-safe increment of user number
user_number_lock = threading.Lock()
current_user_number = 1

def handle_client(client_socket, client_address):
    global current_user_number

    if not login(client_socket):
        client_socket.close()
        return

    with user_number_lock:  # Lock this section to safely increment the user number
        user_n = current_user_number
        current_user_number += 1

    print(f"User {user_n} from {client_address} using JKPQ Protocol")
    
    selected_board = None

    while True:
        try:
            selected_movie_idx = int(decrypt_message(client_socket.recv(1024)).strip()) - 1

            if selected_movie_idx < 0 or selected_movie_idx >= len(movies):
                client_socket.sendall(encrypt_message("405 ERROR Invalid selection. Please try again.\n"))
            else:
                selected_movie = list(movies.keys())[selected_movie_idx]
                selected_board = movies[selected_movie]
                board_str = print_board(selected_board)
                client_socket.sendall(encrypt_message(f"204 OK You selected: {selected_movie}\n\n{board_str}"))
                break  
        except ValueError:
            client_socket.sendall(encrypt_message("406 ERROR Invalid input. Please enter a number.\n"))

    print(f"User {user_n} selected {selected_movie}")

    while True:
        data = decrypt_message(client_socket.recv(1024))
        if not data:
            break

        receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{receive_time}] Received from client {client_address}: {data}")

        if data.startswith("send"):
            try:
                command, row_label, col = data.split()
                col = int(col)
                row = ord(row_label.lower()) - ord('a')

                if 0 <= row < 10 and 1 <= col <= 10:
                    col -= 1
                    if selected_board[row][col] == 'o':
                        selected_board[row][col] = 'x'
                        response = f"201 OK Position ({row_label},{col + 1}) updated to 'X'"
                    else:
                        response = f"401 ERROR Position ({row_label},{col + 1}) already taken"
                else:
                    response = "402 ERROR Position out of bounds"

                board_str = print_board(selected_board)

            except (ValueError, IndexError):
                response = "403 ERROR Invalid command format"
                client_socket.sendall(encrypt_message(response))
        elif data.lower() == "quit":
            response = "202 OK Connection closed"
            client_socket.sendall(encrypt_message(response))
            break
        elif data.lower() == "shutdown":
            response = "203 OK Server shutting down"
            client_socket.sendall(encrypt_message(response))
            client_socket.close()
            print("Server is shutting down...")
            server_socket.close()
            return
        else:
            response = "400 ERROR Invalid command"

        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_socket.sendall(encrypt_message(f"{response}\n\n{board_str}"))

        print(f"[{send_time}] Sent to client {client_address}: {response}")
        

    client_socket.close()
    print(f"Connection with {client_address} closed")


def start_server(host='localhost', port=12345):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(4)
    print("Server started using JKPQ Protocol, waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
