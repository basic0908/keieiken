import argparse
import threading
from src.receiver.video_player import VideoPlayer
from src.utils.HandTracker import HandTracker

def run_video(video_path, audio_path):
    vp = VideoPlayer(video_path, audio_path)
    vp.play()

def run_hand_tracker():
    tracker = HandTracker(track_hand="Left")
    tracker.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, required=True, help="Video name without extension")
    args = parser.parse_args()

    base_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/"
    video_path = f"{base_path}{args.video}.mp4"
    audio_path = f"{base_path}{args.video}.mp3"

    # Start video and audio in one thread
    video_thread = threading.Thread(target=run_video, args=(video_path, audio_path))
    # Start webcam hand tracker in another thread
    hand_thread = threading.Thread(target=run_hand_tracker)

    hand_thread.start()
    video_thread.start()

    hand_thread.join()
    video_thread.join()
