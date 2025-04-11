import socket
import pickle


def setup_sender_connection(host='192.168.11.5', port=9999, timeout=30):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)  # Set connection timeout
    try:
        s.connect((host, port))
        print(f"[Sender] Connected to {host}:{port}")
        return s
    except socket.timeout:
        print(f"[Sender] Connection to {host}:{port} timed out after {timeout} seconds.")
        s.close()
        raise
    except Exception as e:
        print(f"[Sender] Failed to connect to {host}:{port}: {e}")
        s.close()
        raise


def setup_receiver_connection(host='0.0.0.0', port=9999):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    print(f"[Receiver] Listening on {host}:{port}...")
    conn, addr = s.accept()
    print(f"[Receiver] Connection from {addr}")
    return conn

def send_data(sock, data):
    try:
        serialized = pickle.dumps(data)
        sock.sendall(serialized)
    except Exception as e:
        print(f"[Sender] Send failed: {e}")

def receive_data(conn):
    try:
        data = conn.recv(4096)
        return pickle.loads(data)
    except Exception as e:
        print(f"[Receiver] Receive failed: {e}")
        return None
