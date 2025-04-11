import argparse
import threading
import time
import cv2
from src.receiver.video_player import VideoPlayer
from src.utils.HandTracker import HandTracker
from src.utils.connection import setup_receiver_connection, receive_data

def run_video(video_path, audio_path):
    vp = VideoPlayer(video_path, audio_path)
    vp.play()

def run_hand_tracker():
    tracker = HandTracker(track_hand="Left")
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = tracker.update(frame)
        cv2.imshow("Receiver - Hand Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('w'):
            print("[INFO] Exiting local tracker on key 'w'")
            break

    cap.release()
    tracker.release()
    cv2.destroyAllWindows()

def run_data_receiver():
    conn = setup_receiver_connection(host='0.0.0.0', port=9999)
    print("[INFO] Receiving hand tracking data from sender...")
    try:
        while True:
            data = receive_data(conn)
            if data is not None:
                print("[RECEIVER] Data received from sender (first point):", data[0] if data else "Empty")
    except KeyboardInterrupt:
        print("[INFO] Stopping receiver...")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Video name without extension")
    args = parser.parse_args()

    base_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/"
    video_path = f"{base_path}{args.video}.mp4"
    audio_path = f"{base_path}{args.video}.mp3"

    # First, ensure connection is established
    print("[INFO] Waiting for sender to connect...")
    conn = setup_receiver_connection(host='0.0.0.0', port=9999)
    print("[INFO] Sender connected. Starting video, tracking, and receiving.")

    # Start video
    video_thread = threading.Thread(target=run_video, args=(video_path, audio_path))
    # Start webcam tracker on receiver
    hand_thread = threading.Thread(target=run_hand_tracker)
    # Start receiving from sender
    receiver_thread = threading.Thread(target=run_data_receiver)

    video_thread.start()
    hand_thread.start()
    receiver_thread.start()

    video_thread.join()
    hand_thread.join()
    receiver_thread.join()