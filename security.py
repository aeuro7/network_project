from encrypt import encrypt_message
from encrypt import decrypt_message

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

    # Validate username and password
    if username in users and users[username] == password:
        movie_selection_message = "Select a movie:\n"
        for idx, movie in enumerate(movies.keys(), 1):
            movie_selection_message += f"{idx}. {movie}\n"        

        client_socket.sendall(encrypt_message(f"200 OK Login successful\n{movie_selection_message}"))
        return True
    else:
        client_socket.sendall(encrypt_message("404 Forbidden Login failed"))
        return False
