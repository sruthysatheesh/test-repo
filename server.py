import socket
import logging
import threading

# 1. SETUP SECURE LOGGING
# We use a proper logging library instead of executing shell commands.
logging.basicConfig(
    filename='secure_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def handle_client(conn, addr):
    """Handles individual client connections in a separate thread."""
    with conn:
        print(f"Securely connected by {addr}")
        try:
            while True:
                # 2. LIMIT BUFFER SIZE
                # Prevents a client from sending gigabytes of data to crash the server.
                data = conn.recv(1024)
                if not data:
                    break

                # 3. SAFE DECODING & VALIDATION
                try:
                    user_msg = data.decode('utf-8').strip()
                except UnicodeDecodeError:
                    conn.sendall(b"Error: Invalid encoding.")
                    continue

                # 4. DATA-ONLY LOGGING
                # This is a 'parameterized' approach. The message is treated 
                # strictly as data, never as a command.
                logging.info(f"Client {addr}: {user_msg}")
                print(f"Logged safely: {user_msg}")

                conn.sendall(b"Message logged securely via Astraea Protocol.")
                
        except Exception as e:
            print(f"Error handling client {addr}: {e}")

def start_secure_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow address reuse (good for testing/restarting)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    host = '127.0.0.1'
    port = 65432
    server_socket.bind((host, port))
    server_socket.listen(5) # Support a queue of 5 waiting connections
    
    print(f"Astraea Secure Server listening on {host}:{port}...")

    while True:
        # 5. MULTI-THREADED ACCEPT
        # The server can now handle multiple 'Hacker' attempts simultaneously 
        # without crashing or locking up.
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_secure_server()
