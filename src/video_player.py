import cv2
import pygame
import time

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

        start_time = time.time()

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("End of video.")
                break

            if overlay_func:
                frame = overlay_func(frame)

            cv2.imshow(window_name, frame)

            elapsed_time = (time.time() - start_time) * 1000  # in ms
            wait_time = max(1, int(self.delay - elapsed_time % self.delay))
            if cv2.waitKey(wait_time) & 0xFF == ord('q'):
                print("Playback interrupted.")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        if self.audio_path:
            pygame.mixer.music.stop()

    def get_frame_dimensions(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

video_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/sugarcoat.mp4"
audio_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/sugarcoat.mp3"

vp = VideoPlayer(video_path, audio_path)
vp.play()
