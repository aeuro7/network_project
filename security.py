

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
    username = client_socket.recv(1024).decode().strip()
    password = client_socket.recv(1024).decode().strip()

    # Validate username and password
    if username in users and users[username] == password:
        movie_selection_message = "Select a movie:\n"
        for idx, movie in enumerate(movies.keys(), 1):
            movie_selection_message += f"{idx}. {movie}\n"        

        client_socket.sendall(f"200 OK Login successful\n{movie_selection_message}".encode())
        return True
    else:
        client_socket.sendall("403 Forbidden Login failed\n".encode())
        return False
