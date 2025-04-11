import argparse
import threading
import time
from src.utils.HandTracker import HandTracker
from src.utils.connection import setup_sender_connection, send_data
import cv2


def wait_for_receiver(host='192.168.11.5', port=9999, timeout=30):
    print("[INFO] Attempting to connect to receiver...")
    start_time = time.time()
    while True:
        try:
            conn = setup_sender_connection(host, port, timeout)
            print(f"[INFO] Connected to receiver at {host}:{port}")
            return conn
        except Exception as e:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"[ERROR] Could not connect to receiver within {timeout} seconds.")
            print("[INFO] Retrying connection...")
            print(e)
            time.sleep(1)


def run_hand_tracker(conn):
    tracker = HandTracker(track_hand="Right")
    cap = cv2.VideoCapture(0)

    print("[INFO] Sending hand tracking data to receiver...")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = tracker.update(frame)

            # Continuously send location data
            send_data(conn, tracker.locations)

            # Show preview (optional)
            cv2.imshow("Sender - Hand Tracker", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('w'):
                print("[INFO] Exiting on key 'w'")
                break

            time.sleep(0.01)

    finally:
        cap.release()
        tracker.release()
        conn.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # Wait for connection to receiver
    conn = wait_for_receiver(host='192.168.11.5', port=9999)

    # Run hand tracker with connection
    run_hand_tracker(conn)