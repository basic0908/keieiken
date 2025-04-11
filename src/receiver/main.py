import argparse
import threading
import time
import cv2
import csv
import os
from src.receiver.video_player import VideoPlayer
from src.utils.HandTracker import HandTracker
from src.utils.connection import setup_receiver_connection, receive_data

CSV_PATH = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/coordinates.csv"

# Clear CSV except for header
def initialize_csv():
    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['receiver_X', 'receiver_Y', 'receiver_Z', 'sender_X', 'sender_Y', 'sender_Z'])

# Append a new row to the CSV
def append_to_csv(receiver_data=None, sender_data=None):
    receiver_data = receiver_data or [None, None, None]
    sender_data = sender_data or [None, None, None]
    with open(CSV_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(receiver_data + sender_data)

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

        # Write receiver data (first point only)
        if tracker.locations:
            append_to_csv(receiver_data=list(tracker.locations[0]))

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
            if data:
                print("[RECEIVER] Data received from sender (first point):", data[0])
                append_to_csv(sender_data=list(data[0]))
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

    # Prepare CSV
    initialize_csv()

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