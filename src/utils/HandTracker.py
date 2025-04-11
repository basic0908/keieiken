import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, track_hand='Right', max_num_hands=2, detection_conf=0.7, tracking_conf=0.6):
        self.track_hand = track_hand  # "Right" or "Left"
        self.locations = []  # List of (x, y, z) tuples for the tracked hand

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mp_draw = mp.solutions.drawing_utils

    def update(self, frame):
        self.locations.clear()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, hand_info in zip(result.multi_hand_landmarks, result.multi_handedness):
                label = hand_info.classification[0].label
                if label == self.track_hand:
                    for lm in hand_landmarks.landmark:
                        self.locations.append((lm.x, lm.y, lm.z))
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    break

        return frame

    def release(self):
        self.hands.close()

    def run(self):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.update(frame)
            print(self.locations)  # Optional: print landmark positions

            cv2.imshow("Hand Tracker", frame)
            if cv2.waitKey(1) & 0xFF == ord('w'):
                break

        cap.release()
        self.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = HandTracker(track_hand="Right")
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = tracker.update(frame)

        # Print landmark positions (optional)
        print(tracker.locations)

        cv2.imshow("Hand Tracker", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    tracker.release()
    cv2.destroyAllWindows()


