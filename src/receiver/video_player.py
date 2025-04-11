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

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        enlargeBy = 1.0 # ウィンドウサイズ
        cv2.resizeWindow(window_name, int(640*enlargeBy), int(360*enlargeBy))

        start_time = time.time()
        frame_index = 0

        while self.cap.isOpened():
            elapsed_time = time.time() - start_time # 再生時間
            expected_frame = int(elapsed_time * self.frame_rate) # 現在のフレーム数

            # 遅れたフレームをスキップして追いつく
            while frame_index < expected_frame - 1:
                self.cap.grab()
                frame_index += 1

            # Read the actual frame to display
            ret, frame = self.cap.read()
            if not ret:
                print("End of video.")
                break

            frame_index += 1

            if overlay_func:
                frame = overlay_func(frame)

            frame = cv2.resize(frame, (640, 360))
            cv2.imshow(window_name, frame)

            # 映像が早すぎる場合
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

if __name__ == "__main__":
    song = "青と夏"
    video_path = f"C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/{song}.mp4"
    audio_path = f"C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets/{song}.mp3"

    vp = VideoPlayer(video_path, audio_path)
    vp.play()
