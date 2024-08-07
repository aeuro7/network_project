import socket
import threading
from datetime import datetime
from security import login, movies
from board import print_board
from encrypt import encrypt_message, decrypt_message
from protocol import protocol_handler

user_number_lock = threading.Lock()
current_user_number = 1

def protocol_client(client_socket, client_address):
    global current_user_number

    if not login(client_socket):
        client_socket.close()
        return

    with user_number_lock: 
        user_n = current_user_number
        current_user_number += 1

    send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{send_time}] User {user_n} from {client_address} using 6510450399 Protocol")
    
    selected_board = None

    def select_movie():
        while True:
            try:
                data = decrypt_message(client_socket.recv(1024))
                receive_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{receive_time}] Received from client {client_address}: {data}")

                selected_movie_idx = int(data.strip()) - 1

                if selected_movie_idx < 0 or selected_movie_idx >= len(movies):
                    response = "405_ERROR_Invalid_selection_Please_try_again\n"
                    status_number = "405"
                else:
                    selected_movie = list(movies.keys())[selected_movie_idx]
                    selected_board = movies[selected_movie]
                    board_str = print_board(selected_board)
                    response = f"204_OK_You_selected:{selected_movie}\n\n{board_str}"
                    status_number = "204"
                
                client_socket.sendall(encrypt_message(response))
                send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")
                if selected_movie_idx >= 0 and selected_movie_idx < len(movies):
                    return selected_board  # Return the selected board
            except ValueError:
                response = "406_ERROR_Invalid_input_Please_enter_a_number\n"
                status_number = "406"
                client_socket.sendall(encrypt_message(response))
                send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")

    selected_board = select_movie()  # Select movie initially

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
                        response = f"201_OK_Position_({row_label},{col + 1})_updated_to_'X'"
                        status_number = "201"
                    else:
                        response = f"401_ERROR_Position_({row_label},{col + 1})_already_taken"
                        status_number = "401"
                else:
                    response = "402_ERROR_Position_out_of_bounds"
                    status_number = "402"

            except (ValueError, IndexError):
                response = "403_ERROR_Invalid_command_format"
                status_number = "403"
            
            # Update board after command
            board_str = print_board(selected_board)
            client_socket.sendall(encrypt_message(f"{response}\n\n{board_str}"))
            send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")
            continue

        elif data.lower() == "change":
            response = "205_OK_Changing_movie_selection..."
            status_number = "205"
            movie_selection_message = "Select_a_movie:\n"
            for idx, movie in enumerate(movies.keys(), 1):
                movie_selection_message += f"{idx}. {movie}\n"  
            client_socket.sendall(encrypt_message(f"{response}\n\n{movie_selection_message}"))
            send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")
            selected_board = select_movie()  # Allow the user to change the movie
            continue  # Skip to the next iteration to avoid sending the board string yet

        elif data.lower() == "quit":
            response = "202_OK_Connection_closed"
            status_number = "202"
            client_socket.sendall(encrypt_message(response))
            send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")
            break
        elif data.lower() == "shutdown":
            response = "203_OK_Server_shutting_down"
            status_number = "203"
            client_socket.sendall(encrypt_message(response))
            send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")
            client_socket.close()
            print("Server is shutting down...")
            server_socket.close()
            return
        else:
            response = "400_ERROR_Invalid_command"
            status_number = "400"
            board_str = print_board(selected_board)
            client_socket.sendall(encrypt_message(f"{response}\n\n{board_str}"))
            send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{send_time} {status_number}] Sent to client {client_address}: {response}")

    client_socket.close()
    print(f"Connection with {client_address} closed")


def start_server(host='localhost', port=12345):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(4)
    print("Server started using 6510450399 Protocol, waiting for clients...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=protocol_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
