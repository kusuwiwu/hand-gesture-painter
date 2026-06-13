import cv2
import mediapipe as mp


class HandDetector:
    """MediaPipe Hands를 사용하여 손의 랜드마크를 감지하고 시각화하는 기반 클래스."""

    # [마법의 숫자 제거] 주요 관절 포인트 인덱스를 전역 상수로 전면 지정
    INDEX_FINGER_TIP = 8
    INDEX_FINGER_PIP = 6
    MIDDLE_FINGER_TIP = 12
    MIDDLE_FINGER_PIP = 10

# 좌표 접근용 축 인덱스 상수를 클래스 변수로 격상하여 함수 내 대문자 규정 위반 방지
    X_AXIS_IDX = 1
    Y_AXIS_IDX = 2
    Y_COORD_IDX = 2

    def __init__(
        self,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    ):
        """MediaPipe 엔진을 초기화하고 환경 설정을 완료합니다."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_positions(self, frame):
        """프레임에서 손을 감지하여 21개 랜드마크의 픽셀 좌표 리스트를 추출합니다.

        :param frame: 입력 이미지 픽셀 배열 (None 가능)
        :return: [[ID, X좌표, Y좌표], ...] 구조의 리스트 (감지 실패 시 빈 리스트)
        """
        # [테스트 에러 해결] None 입력에 대한 방어 코드 추가
        if frame is None:
            return []

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        # [도우미 메서드 활용] 랜드마크 추출 및 픽셀 변환 로직을 내부 비공개 메서드로 위임
        return self._parse_hand_landmarks(frame)

    def draw_skeleton(self, frame):
        """감지된 손의 관절 포인트와 연결선(스켈레톤)을 화면에 렌더링합니다.

        :param frame: 시각화를 진행할 원본 이미지 프레임 (numpy.ndarray 또는 None)
        :return: 스켈레톤이 그려진 이미지 프레임, 입력이 None인 경우 None 반환 (numpy.ndarray 또는 None)
    """
        if frame is None:
            return None

        if self.results and self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_lms,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def _is_valid_list(self, lm_list):
        """랜드마크 연산 데이터 배열의 정성적 유효성을 검증합니다.
        
        MediaPipe는 손 전체가 나오지 않아도 일부만 감지되면 데이터를 주므로,
        엄격한 21개 개수 검사보다 비어있지 않은지만 검사합니다.
        """
        # [테스트 에러 해결] None 타입에 대한 방어 코드 추가
        if lm_list is None or not isinstance(lm_list, list):
            return False
        return len(lm_list) > 0

    def _parse_hand_landmarks(self, frame):
        """[Protected Helper] 미디어파이프의 정규화된 좌표를 화면 크기에 맞는 픽셀 좌표로 변환하는 도우미 메서드."""
        lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            # 첫 번째로 검출된 손 데이터 활용
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = frame.shape
            for lm_id, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([lm_id, cx, cy])
        return lm_list