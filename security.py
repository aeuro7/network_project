from encrypt import encrypt_message
from encrypt import decrypt_message
from datetime import datetime

users = {
    "user1": "password1",
    "user2": "password2"
}

movies = {
    "Top Gun: Maverick": [['o' for _ in range(10)] for _ in range(10)],
    "Avengers: Endgame": [['o' for _ in range(10)] for _ in range(10)],
    "The Matrix": [['o' for _ in range(10)] for _ in range(10)]
}

def login(client_socket):
    """Handle user login."""
    encrypted_username = client_socket.recv(1024)
    encrypted_password = client_socket.recv(1024)
    
    username = decrypt_message(encrypted_username)
    password = decrypt_message(encrypted_password)

    if username in users and users[username] == password:
        movie_selection_message = "Select a movie:\n"
        for idx, movie in enumerate(movies.keys(), 1):
            movie_selection_message += f"{idx}. {movie}\n"

        response = f"200 OK Login successful\n\n{movie_selection_message}"
        client_socket.sendall(encrypt_message(response))
        
        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{send_time}] Sent to client 200 OK Login successful and list of movies")
        
        return True
    else:
        response = "404 Forbidden Login failed"
        client_socket.sendall(encrypt_message(response))
        
        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{send_time}] Sent to client: {response}")
        
        return False
