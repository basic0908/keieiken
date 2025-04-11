import cv2
import time
import socket
from src.utils.HandTracker import HandTracker
from src.utils.connection import setup_sender_connection, send_data


def wait_for_receiver(host='localhost', port=9999, timeout=1, retry_delay=2):
    """Keep trying to connect to the receiver until successful."""
    while True:
        try:
            conn = setup_sender_connection(host, port, timeout)
            print(f"[INFO] Connected to receiver at {host}:{port}")
            return conn
        except (ConnectionRefusedError, socket.timeout):
            print(f"[INFO] Waiting for receiver... Retrying in {retry_delay}s")
            time.sleep(retry_delay)


def main():
    print("[INFO] Attempting to connect to receiver...")
    conn = wait_for_receiver(host='localhost', port=9999)

    tracker = HandTracker(track_hand="Right")
    cap = cv2.VideoCapture(0)

    print("[INFO] Sending hand tracking data to receiver...")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = tracker.update(frame)

            # Send location data
            if tracker.locations:
                send_data(conn, tracker.locations)

            # Show preview
            cv2.imshow("Sender - Hand Tracker", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('w'):
                print("[INFO] Exiting on key 'w'")
                break

            time.sleep(0.01)  # Avoid flooding
    finally:
        cap.release()
        tracker.release()
        conn.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
