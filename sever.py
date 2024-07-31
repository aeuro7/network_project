import socket
import threading
from datetime import datetime
from security import login, movies

current_user_number = 1

def print_board(board):
    """Print the current state of the board."""
    print("\n    " + " ".join(str(i) for i in range(1, 11)))  # Column numbers from 1 to 10
    
    row_labels = 'abcdefghij'
    for i, row in enumerate(board):
        # Print row label
        print(f"{row_labels[i]}   ", end="")
        # Print row data
        print(' '.join(row))
    print()

def handle_client(client_socket, client_address):
    """Handle communication with a single client."""
    global current_user_number

    # Require login before proceeding
    if not login(client_socket):
        client_socket.close()
        return

    user_n = current_user_number
    print(f"User {user_n} from {client_address} using JKPQ Protocol")
    
    selected_board = None

    while True:
        # Receive movie selection from the client
        try:
            selected_movie_idx = int(client_socket.recv(1024).decode().strip()) - 1

            if selected_movie_idx < 0 or selected_movie_idx >= len(movies):
                client_socket.sendall("Invalid selection. Please try again.\n".encode())
            else:
                selected_movie = list(movies.keys())[selected_movie_idx]
                selected_board = movies[selected_movie]
                client_socket.sendall(f"You selected: {selected_movie}\n".encode())
                break  # Exit loop once a valid selection is made

        except ValueError:
            client_socket.sendall("Invalid input. Please enter a number.\n".encode())

    print(f"User {user_n} selected {selected_movie}")

    # Print the board of the selected movie
    print_board(selected_board)

    while True:
        data = client_socket.recv(1024).decode()  # Receive data from client
        if not data:
            break

        receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the time the message was received
        print(f"[{receive_time}] Received from client {client_address}: {data}")

        # Process command
        if data.startswith("send"):
            try:
                # Extract row and column from the data
                command, row_label, col = data.split()
                col = int(col)
                
                # Convert row label (a-j) to row index (0-9)
                row = ord(row_label.lower()) - ord('a')
                
                # Validate position
                if 0 <= row < 10 and 1 <= col <= 10:
                    col -= 1  # Convert column from 1-10 to 0-9
                    if selected_board[row][col] == 'o':
                        selected_board[row][col] = 'x'
                        response = f"200 OK Position ({row_label},{col + 1}) updated to 'X'"
                    else:
                        response = f"400 ERROR Position ({row_label},{col + 1}) already taken"
                else:
                    response = "400 ERROR Position out of bounds"

                # Print updated board of the selected movie
                print_board(selected_board)

            except (ValueError, IndexError):
                response = "400 ERROR Invalid command format"

        elif data.lower() == "quit":
            response = "200 OK Connection closed"
            client_socket.sendall(response.encode())
            break
        
        elif data.lower() == "shutdown":
            response = "200 OK Server shutting down"
            client_socket.sendall(response.encode())
            client_socket.close()
            print("Server is shutting down...")
            server_socket.close()
            return
        
        else:
            response = "400 ERROR Invalid command"

        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_socket.sendall(response.encode())
        print(f"[{send_time}] Sent to client {client_address}: {response}")

    client_socket.close()
    print(f"Connection with {client_address} closed")

def start_server(host='localhost', port=12345):
    """Start the server and listen for incoming connections."""
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
