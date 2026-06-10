import cv2
import numpy as np

class HandDetector:
    """오픈세스 기반으로 카메라 영상에서 손을 검출하는 부모 클래스입니다.

    Example:
        >>> import cv2
        >>> detector = HandDetector()
        >>> img = cv2.imread("blank.jpg")
        >>> if img is not None:
        ...     labs = detector.find_positions(img)
    """

    def __init__(self, max_num_hands=1, min_detection_confidence=0.5):
        """HandDetector 클래스를 초기화합니다.

        :param max_num_hands: 인식할 최대 손의 개수 (기본값 1)
        :param min_detection_confidence: 검출 최소 신뢰도 (기본값 0.5)
        """
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        
        try:
            import mediapipe as mp
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                max_num_hands=self.max_num_hands,
                min_detection_confidence=self.min_detection_confidence
            )
        except ImportError:
            # 실무형 예외 처리: broad exception 방지
            self.mp_hands = None
            self.hands = None

    def _preprocess_image(self, img):
        """이미지를 MediaPipe 래퍼가 인식할 수 있도록 BGR에서 RGB로 변환합니다.

        :param img: OpenCV 이미지 프레임
        :return: RGB로 변환된 이미지 프레임
        """
        if img is None:
            return None
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def find_positions(self, img):
        """이미지에서 손의 21개 랜드마크 좌표를 찾아 리스트로 반환합니다.

        :param img: OpenCV 이미지 프레임
        :return: (id, x, y) 튜플을 담은 21개의 랜드마크 리스트
        """
        lm_list = []
        if img is None or self.hands is None:
            return lm_list

        img_rgb = self._preprocess_image(img)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            h, w, _ = img.shape
            for hand_lms in results.multi_hand_landmarks:
                for idx, lm in enumerate(hand_lms.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append((idx, cx, cy))
        return lm_list