import cv2, time, threading
import mediapipe as mp

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),(0,17)
]

class LandmarksTracker:
    def __init__(self, model_path):
        self.model_path = model_path
        self.lock = threading.Lock()
        self.latest = []   # lista de manos; cada mano: lista de (x,y,z) normalizados
        self.running = False

    def start(self):
        self.running = True
        t = threading.Thread(target=self._run, daemon=True)
        t.start()

    def stop(self):
        self.running = False

    def get_latest(self):
        with self.lock:
            return [hand[:] for hand in self.latest]

    def _run(self):
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=2
        )

        cap = cv2.VideoCapture(0)
        start_time = time.perf_counter()

        with HandLandmarker.create_from_options(options) as landmarker:
            while self.running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

                timestamp_ms = int((time.perf_counter() - start_time) * 1000)
                result = landmarker.detect_for_video(mp_image, timestamp_ms)

                hands = []
                if result.hand_landmarks:
                    for hand in result.hand_landmarks:
                        hands.append([(lm.x, lm.y, lm.z) for lm in hand])

                with self.lock:
                    self.latest = hands

        cap.release()