import cv2
import mediapipe as mp

class HandDetector:
    """미디어파이프를 이용해 손을 감지하고 랜드마크를 추출하는 부모 클래스"""
    
    def __init__(self, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def find_positions(self, img):
        """이미지에서 손의 랜드마크 고유 픽셀 좌표 리스트를 반환합니다.
        
        :param img: OpenCV BGR 이미지 프레임
        :return: [[id, x, y], ...] 구조의 랜드마크 리스트
        
        >>> # 테스트 프레임 유효성 검증 예시
        >>> detector = HandDetector()
        >>> detector._is_valid_list([])
        False
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        lm_list = []
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                for idx, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([idx, cx, cy])
        return lm_list

    def _is_valid_list(self, lm_list):
        """[비공개 메서드] 랜드마크 리스트가 유효한 손 구조(21개)를 갖추었는지 검증합니다."""
        return len(lm_list) == 21