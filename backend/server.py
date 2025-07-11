import socket
import datetime

HOST = '127.0.0.1'
PORT = 5000

# Standardized log message with timestamp and message
def log(msg):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] [Server] {msg}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    log(f'Server running on http://{HOST}:{PORT}/')
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            lines = data.split(b'\r\n')
            is_get = any(line.startswith(b'GET /') for line in lines)
            is_from_ext = any(line.strip().lower() == b'x-from-extension: true' for line in lines)
            if is_get and is_from_ext:
                log(f'Received request from {addr}')
                response = b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from Python backend!'
                conn.sendall(response)
            elif is_get:
                log(f'Received request from {addr} but not from extension')
                conn.sendall(b'HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain\r\n\r\nForbidden')
            else:
                conn.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
