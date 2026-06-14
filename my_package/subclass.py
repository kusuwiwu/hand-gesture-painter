import cv2
import numpy as np

from .core import HandDetector
from .utils import calculate_distance


class GesturePainter(HandDetector):
    """HandDetector를 상속받아 특정 제스처를 분석
    검지 손가락의 움직임을 캔버스에 그림으로 저장하는 클래스

    Example:
        >>> painter = GesturePainter()
        >>> painter.is_drawing_mode([])
        False
    """

    #숫자 상수화
    DISTANCE_THRESHOLD = 65 # 손가락 좌표가 갑자기 크게 튀는 경우 
    LINE_THICKNESS = 10 # 잘못된 선이 그려지는 것을 방지하기 위한 최대 허용 거리

    # 부모 클래스 상수가 없을 때를 대비한 기본 인덱스 값 상수화
    FALLBACK_X_AXIS_IDX = 1
    FALLBACK_Y_AXIS_IDX = 2

    def __init__(
        self,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        draw_color=(0, 0, 255),
    ):
        """부모 생성자를 호출 선을 기록할 독립 캔버스 메모리를 할당

        :param max_num_hands: 검출할 최대 손의 개수 (int)
        :param min_detection_confidence: 검출 최소 신뢰도 임계값 (float)
        :param min_tracking_confidence: 추적 최소 신뢰도 임계값 (float)
        :param draw_color: 캔버스에 그릴 선의 BGR 색상 튜플 (tuple)
        """
        super().__init__(
            max_num_hands, min_detection_confidence, min_tracking_confidence
        )
        self.draw_color = draw_color
        # 사용자가 그린 선을 계속 저장하기 위한 별도 캔버스
        self.canvas = None 
        self.prev_x, self.prev_y = 0, 0 #이전 손가락 좌표저장 현재좌표랑연결

    def _get_x_axis_index(self):
        """랜드마크 [id,x,y]구조 x좌표 가져오기위한 함수. 부모 클래스의 상수 변경 대비"""
        if hasattr(self, "X_AXIS_IDX"):#부모 상수 바뀌어도 안전한접근
            return self.X_AXIS_IDX
        if hasattr(self, "X_AXIS"):
            return self.X_AXIS
        return self.FALLBACK_X_AXIS_IDX

    def _get_y_axis_index(self):
        """랜드마크 [id,x,y]구조 y좌표 가져오기위한 함수. 부모 클래스의 상수 변경 대비"""
        if hasattr(self, "Y_AXIS_IDX"):
            return self.Y_AXIS_IDX
        if hasattr(self, "Y_AXIS"):
            return self.Y_AXIS
        return self.FALLBACK_Y_AXIS_IDX

    def is_drawing_mode(self, lm_list):
        """검지 손가락만 명확하게 펼쳐진 그리기 모드 상태인지 판별 검지펴지고중지 접으면 그리기모드

        :param lm_list: find_positions 메서드에서 추출된 21개 랜드마크 픽셀 좌표 리스트 (list)
        :return: 그리기 모드(검지 오픈 및 중지 클로즈) 조건 충족 여부 (bool)

        Example:
        >>> painter = GesturePainter()
        >>> painter.is_drawing_mode(None)
        False
        >>> painter.is_drawing_mode([])
        False
        """

        # 부모의 방어 코드를 활용해 유효성 검사
        if not self._is_valid_list(lm_list):
            return False

        y_idx = self._get_y_axis_index()

        # 부모 클래스의 전역 상수를 바인딩하여 함수 내 대문자 변수 선언 경고 회피
        is_index_up = (
            lm_list[self.INDEX_FINGER_TIP][y_idx] # 검지 끝이 검지 중간관절보다 위에 있으면
            < lm_list[self.INDEX_FINGER_PIP][y_idx] # 검지가 펴진 상태로 판단
        )
        is_middle_down = (
            lm_list[self.MIDDLE_FINGER_TIP][y_idx] # 중지 끝이 중간관절보다 아래에 있으면
            > lm_list[self.MIDDLE_FINGER_PIP][y_idx] # 중지가 접힌 상태로 판단
        )

        return is_index_up and is_middle_down

    def draw_canvas(self, frame, lm_list):
        """검지 손가락의 궤적을 투명 캔버스에 선으로 누적하고 원본 프레임과 캔버스를 합성

        :param frame: 웹캠으로부터 입력받은 현재 이미지 프레임 (numpy.ndarray 또는 None)
        :param lm_list: find_positions 메서드에서 추출된 랜드마크 픽셀 좌표 리스트 (list)
        :return: 캔버스 선 궤적이 누적 합성된 최종 이미지 프레임 (numpy.ndarray 또는 None)
        """
        if frame is None: #None 입력오류방지
            return None

        # 캔버스가 비어있을시 카메라 프레임 크기와 동일한 도화지 생성
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

        if self.is_drawing_mode(lm_list):
            self._accumulate_trajectory(lm_list)
        else:
            self.prev_x, self.prev_y = 0, 0  #이전 손가락 좌표저장 현재좌표랑연결

        gray_canvas = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        # 선이 그어진 부분(값이 0이 아닌 부분)을 흰색(255)으로 추출
        _, mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)

        foreground = cv2.bitwise_and(self.canvas, self.canvas, mask=mask) # 캔버스에서 그림이 있는 부분만 추출
        background = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask)) # 원본 영상에서 그림이 없는 부분만 추출

        return cv2.add(background, foreground) # 그림과 카메라 영상을 합성

    def _accumulate_trajectory(self, lm_list):
        """내부적으로 손가락 이동 궤적을 계산 선을 누적하는 도우미 메서드."""

        # 부모 클래스의 변수명 불일치 문제를 완벽하게 우회하는 안전장치 (X=1, Y=2)
        x_idx = self._get_x_axis_index()
        y_idx = self._get_y_axis_index()

        cx = lm_list[self.INDEX_FINGER_TIP][x_idx]#검지끝의 x좌표 추출
        cy = lm_list[self.INDEX_FINGER_TIP][y_idx]#검지끝의 y좌표 추출

        if self.prev_x == 0 and self.prev_y == 0: #좌표가 0,0이면
            self.prev_x, self.prev_y = cx, cy #이전위치로 저장

        # 좌표가 너무 멀리 이동했다면 인식 오류로 판단하고 선을 그리지 않음
        dist = calculate_distance((self.prev_x, self.prev_y), (cx, cy))

        # 오차 범위 이내의 정상적인 움직임일 때만 연속된 부드러운 선으로 연결
        if dist < self.DISTANCE_THRESHOLD:
            cv2.line(
                self.canvas,
                (self.prev_x, self.prev_y),
                (cx, cy),
                self.draw_color,
                thickness=self.LINE_THICKNESS,
            )

        # 다음 프레임을 위한 좌표 저장
        self.prev_x, self.prev_y = cx, cy
