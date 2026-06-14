import cv2
import mediapipe as mp


class HandDetector:
    """MediaPipe Hands를 사용하여 손의 랜드마크를 감지하고 시각화하는 부모 클래스.
    Example:
        >>> detector = HandDetector()
        >>> detector is not None
        >>> detector.find_positions(None)
        []
        True
    """

    # 주요 관절 포인트 인덱스를 전역 상수로 전면 지정 검지,중지 끝 중간상수 설정
    INDEX_FINGER_TIP = 8 #검지 끝
    INDEX_FINGER_PIP = 6 #검지 중간
    MIDDLE_FINGER_TIP = 12 # 중지 끝
    MIDDLE_FINGER_PIP = 10 # 중지 중간

    # 인덱스 상수를 클래스 변수로 격상, 대문자 오류방지 x위치1 y위치2
    X_AXIS_IDX = 1 #[id,x,y] 중 x는1번
    Y_AXIS_IDX = 2 #[id,x,y] 중 y는2번

    def __init__( #MediaPipe Hands 객체를 생성하고 손 인식 환경 설정
        self,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    ):
        """MediaPipe 엔진을 초기화하고 환경 설정을 완료"""
        self.mp_hands = mp.solutions.hands # MediaPipe Hands 모듈 가져오기
        self.hands = self.mp_hands.Hands( #손검출객체 생성 이후 find_positions()에서 사용
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mp_draw = mp.solutions.drawing_utils # 손 뼈대를 그리는 MediaPipe 도구
        self.results = None #손인식 결과 저장변수 처음에는 변수 없으니까 None

    def find_positions(self, frame):
        """손을 감지 21개 랜드마크의 픽셀 좌표 추출.

        :param frame: 입력 이미지 픽셀 배열 (None 가능)
        :return: [[ID, X좌표, Y좌표], ...] 구조의 리스트 (감지 실패 시 빈 리스트)
        """
        #None 입력오류방지.
        if frame is None:
            return [] #리스트기준동작 하므로 리스트반환

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #OPEN CV는 BGR MEDIAPIPE는 RGB 사용
        self.results = self.hands.process(img_rgb) #실제 손인식 결과를 SELF.RESULTS에저장

        #랜드마크 추출 및 픽셀 변환 로직 내부 비공개 메서드로 손추출기능 별도함수로
        return self._parse_hand_landmarks(frame)

    def draw_skeleton(self, frame):
        """감지된 손의 관절 연결선(스켈레톤)을 화면에 렌더링.

        :param frame: 시각화를 진행할 원본 이미지 프레임
        :return: 스켈레톤이 그려진 이미지 프레임, 입력이 None인 경우 None 반환
        """
        if frame is None: #None입력 오류방지
            return None

        if self.results and self.results.multi_hand_landmarks: #MEDIAPIPE제공함수. 손뼈대그림
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_lms, self.mp_hands.HAND_CONNECTIONS
                )
        return frame

    def _is_valid_list(self, lm_list):
        """랜드마크 연산 데이터 배열의 정성적 유효성을 검증

        MediaPipe는 손 전체가 나오지 않아도 일부만 감지되면 데이터를 주므로,
        엄격한 21개 개수 검사보다 비어있지 않은지만 검사.

        Example:
            >>> detector = HandDetector()
            >>> detector._is_valid_list([[0, 100, 100]])
            True
            >>> detector._is_valid_list([])
            False
            >>> detector._is_valid_list(None)
        False
        """

        #None 입력 오류방지
        if lm_list is None or not isinstance(lm_list, list):
            return False
        return len(lm_list) > 0 #비어있지않으면 True

    def _parse_hand_landmarks(self, frame):
        """# MediaPipe 랜드마크 데이터를 실제 화면 좌표로 변환"""
        lm_list = []
        if self.results and self.results.multi_hand_landmarks:
            # 첫 번째로 검출된 손 데이터 활용
            my_hand = self.results.multi_hand_landmarks[0]
            h, w, c = frame.shape #높이 너비 색상수
            for lm_id, lm in enumerate(my_hand.landmark): #손관절 순회
                cx, cy = int(lm.x * w), int(lm.y * h)#정규화좌표 실제픽셀좌표로변환
                lm_list.append([lm_id, cx, cy]) #[관절번호,x좌표,y좌표로 저장]
        return lm_list #반환
