import cv2
from utils.HandTracker import HandTracker
from utils.connection import setup_sender_connection, send_data
import time


def main():
    tracker = HandTracker(track_hand="Right")
    cap = cv2.VideoCapture(0)

    conn = setup_sender_connection(host='localhost', port=9999)

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

            # Optional: add small sleep to avoid flooding
            time.sleep(0.01)

    finally:
        cap.release()
        tracker.release()
        conn.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
