import socket
import os  # Added for the buggy "logging" feature

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 65432
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Buggy Server listening on {host}:{port}...")

    conn, addr = server_socket.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data: break
            
            user_msg = data.decode('utf-8')
            print(f"Received: {user_msg}")

            # --- THE BUG: COMMAND INJECTION ---
            # The server tries to log the message using a shell command.
            # If a user sends: "; rm -rf /", the server will execute it.
            os.system(f"echo {user_msg} >> log.txt") 

            conn.sendall(b"Log updated via system shell.")

if __name__ == "__main__":
    start_server()
