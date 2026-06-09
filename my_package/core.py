import cv2

class HandDetector:
    """MediaPipe를 사용하여 영상에서 손을 검출하고 랜드마크를 추출하는 부모 클래스입니다."""

    def __init__(self, max_num_hands=1, min_detection_confidence=0.5):
        """HandDetector 클래스를 초기화합니다."""
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        
        # 버전 호환성 에러를 방지하기 위해 safe 로드 처리
        try:
            import mediapipe as mp
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=max_num_hands,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=0.5
            )
            self.mp_draw = mp.solutions.drawing_utils
        except (AttributeError, ImportError):
            # 호환성 에러 발생 시 시스템이 멈추지 않도록 예외 처리
            self.mp_hands = None
            self.hands = None
            self.mp_draw = None

    def _preprocess_image(self, img):
        """(비공개 메서드) OpenCV의 BGR 이미지를 RGB로 변환합니다."""
        if img is None or img.size == 0:
            return None
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def find_positions(self, img):
        """이미지에서 손을 검출하여 21개 랜드마크의 픽셀 좌표 목록을 반환합니다."""
        lm_list = []
        rgb_img = self._preprocess_image(img)
        if rgb_img is None:
            return lm_list

        # 환경 문제로 hands 객체가 생성되지 않았을 경우의 엣지 케이스 처리
        if self.hands is None:
            return lm_list

        try:
            results = self.hands.process(rgb_img)
            if results.multi_hand_landmarks:
                my_hand = results.multi_hand_landmarks[0]
                h, w, c = img.shape
                for lm_id, lm in enumerate(my_hand.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((lm_id, cx, cy))
        except Exception:
            pass
                
        return lm_list