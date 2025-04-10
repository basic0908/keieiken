import argparse
from video_player import VideoPlayer

def main():
    parser = argparse.ArgumentParser(description="play music video")
    parser.add_argument('--video',default="青と夏", help='ビデオのタイトル')
    args = parser.parse_args()

    song = args.video
    base_path = "C:/Users/ryoii/OneDrive/Documents/GitHub/keieiken/assets"

    video_path = f"{base_path}/{song}.mp4"
    audio_path = f"{base_path}/{song}.mp3"

    vp = VideoPlayer(video_path, audio_path)
    vp.play()

if __name__ == "__main__":
    main()
