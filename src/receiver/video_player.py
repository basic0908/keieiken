import cv2
import pygame
import time
import numpy as np

# Shared PLV state
shared_state = {"plv": 0.0}

def plv_overlay(frame):
    plv = shared_state.get("plv", 0.0)

    # Remap PLV range [0.93, 1.00] → [0, 1]
    adjusted = (plv - 0.93) / 0.07
    adjusted = np.clip(adjusted, 0.0, 1.0)

    # Interpolate blue → red
    r = int(255 * adjusted)
    g = 0
    b = int(255 * (1 - adjusted))
    tint = (b, g, r)  # OpenCV = BGR

    overlay = frame.copy()
    overlay[:] = tint
    return cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)



class VideoPlayer:
    def __init__(self, video_path, audio_path=None):
        self.video_path = video_path
        self.audio_path = audio_path
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

        self.frame_rate = self.cap.get(cv2.CAP_PROP_FPS)
        self.delay = int(1000 / self.frame_rate)

    def play(self, window_name="Music Video", overlay_func=None):
        if self.audio_path:
            pygame.mixer.init()
            pygame.mixer.music.load(self.audio_path)
            pygame.mixer.music.play()

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        enlargeBy = 1.0
        cv2.resizeWindow(window_name, int(640 * enlargeBy), int(360 * enlargeBy))

        start_time = time.time()
        frame_index = 0

        while self.cap.isOpened():
            elapsed_time = time.time() - start_time
            expected_frame = int(elapsed_time * self.frame_rate)

            while frame_index < expected_frame - 1:
                self.cap.grab()
                frame_index += 1

            ret, frame = self.cap.read()
            if not ret:
                print("End of video.")
                break

            frame_index += 1

            if overlay_func:
                frame = overlay_func(frame)

            frame = cv2.resize(frame, (640, 360))
            cv2.imshow(window_name, frame)

            next_frame_time = (frame_index / self.frame_rate)
            time_to_wait = next_frame_time - (time.time() - start_time)
            if time_to_wait > 0:
                time.sleep(time_to_wait)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Playback interrupted.")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        if self.audio_path:
            pygame.mixer.music.stop()

    def get_frame_dimensions(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
