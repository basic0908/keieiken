import argparse
import threading
import time
from src.receiver.video_player import VideoPlayer
from src.utils.HandTracker import HandTracker
from src.utils.connection import setup_receiver_connection, receive_data


def run_video(video_path, audio_path):
    vp = VideoPlayer(video_path, audio_path)
    vp.play()


def run_hand_tracker():
    tracker = HandTracker(track_hand="Left")
    tracker.run()


def wait_for_sender(host='localhost', port=9999):
    print("[INFO] Waiting for sender to connect...")
    conn = setup_receiver_connection(host, port)
    print(f"[INFO] Sender connected from {conn.getpeername()}")
    return conn


def run_receiver_listener():
    conn = wait_for_sender()
    try:
        while True:
            sender_data = receive_data(conn)
            if sender_data:
                print(f"[RECEIVED] {len(sender_data)} hand landmarks from sender.")
    except Exception as e:
        print(f"[ERROR] Connection closed: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Video name without extension")
    args = parser.parse_args()

    base_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/"
    video_path = f"{base_path}{args.video}.mp4"
    audio_path = f"{base_path}{args.video}.mp3"

    # Start receiver thread (wait for sender and print incoming hand tracking data)
    connection_thread = threading.Thread(target=run_receiver_listener)
    # Start webcam hand tracker in another thread
    hand_thread = threading.Thread(target=run_hand_tracker)
    # Start video and audio playback
    video_thread = threading.Thread(target=run_video, args=(video_path, audio_path))

    connection_thread.start()
    hand_thread.start()
    video_thread.start()

    connection_thread.join()
    hand_thread.join()
    video_thread.join()