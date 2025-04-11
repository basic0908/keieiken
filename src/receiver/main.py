import argparse
import threading
import time
import cv2
import csv
import numpy as np
from scipy.signal import hilbert
from src.receiver.video_player import VideoPlayer, plv_overlay, shared_state
from src.utils.HandTracker import HandTracker
from src.utils.connection import setup_receiver_connection, receive_data

CSV_PATH = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/coordinates.csv"

shared_data = {
    'receiver': None,
    'sender': None
}
lock = threading.Lock()

plv_buffer = []

def initialize_csv():
    with open(CSV_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['receiver_X', 'receiver_Y', 'sender_X', 'sender_Y'])

def compute_plv(receiver_y, sender_y):
    rec_analytic = hilbert(receiver_y)
    snd_analytic = hilbert(sender_y)
    rec_phase = np.angle(rec_analytic)
    snd_phase = np.angle(snd_analytic)
    phase_diff = np.arctan2(np.sin(rec_phase - snd_phase), np.cos(rec_phase - snd_phase))
    return np.abs(np.sum(np.exp(1j * phase_diff))) / len(phase_diff)

def logger():
    global plv_buffer
    while True:
        time.sleep(0.05)
        with lock:
            rec = shared_data['receiver'] or [None, None]
            snd = shared_data['sender'] or [None, None]

        rec_xy = [round(x, 3) if x is not None else None for x in rec[:2]]
        snd_xy = [round(x, 3) if x is not None else None for x in snd[:2]]

        with open(CSV_PATH, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(rec_xy + snd_xy)

        if None not in rec_xy and None not in snd_xy:
            plv_buffer.append((rec_xy[1], snd_xy[1]))

        if len(plv_buffer) >= 100:
            receiver_y, sender_y = zip(*plv_buffer)
            plv = compute_plv(np.array(receiver_y), np.array(sender_y))
            shared_state["plv"] = plv
            print(f"[SYNC] PLV (Y-axis): {plv:.5f}")
            plv_buffer = []

def run_video(video_path, audio_path):
    vp = VideoPlayer(video_path, audio_path)
    vp.play(overlay_func=plv_overlay)

def run_hand_tracker():
    tracker = HandTracker(track_hand="Left")
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = tracker.update(frame)
        cv2.imshow("Receiver - Hand Tracker", frame)

        if tracker.locations:
            with lock:
                shared_data['receiver'] = list(tracker.locations[0])

        if cv2.waitKey(1) & 0xFF == ord('w'):
            print("[INFO] Exiting local tracker on key 'w'")
            break

    cap.release()
    tracker.release()
    cv2.destroyAllWindows()

def run_data_receiver(conn):
    print("[INFO] Receiving hand tracking data from sender...")
    try:
        while True:
            data = receive_data(conn)
            if data:
                with lock:
                    shared_data['sender'] = list(data[0])
    except KeyboardInterrupt:
        print("[INFO] Stopping receiver...")
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default="青と夏", help="Video name without extension")
    args = parser.parse_args()

    base_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/"
    video_path = f"{base_path}{args.video}.mp4"
    audio_path = f"{base_path}{args.video}.mp3"

    initialize_csv()

    print("[INFO] Waiting for sender to connect...")
    conn = setup_receiver_connection(host='0.0.0.0', port=9999)
    print("[INFO] Sender connected! Starting tracking, video, and logger...")

    video_thread = threading.Thread(target=run_video, args=(video_path, audio_path))
    hand_thread = threading.Thread(target=run_hand_tracker)
    receiver_thread = threading.Thread(target=run_data_receiver, args=(conn,))
    logger_thread = threading.Thread(target=logger)

    video_thread.start()
    hand_thread.start()
    receiver_thread.start()
    logger_thread.start()

    video_thread.join()
    hand_thread.join()
    receiver_thread.join()
    logger_thread.join()
