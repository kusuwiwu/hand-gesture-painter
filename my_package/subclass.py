import cv2
import numpy as np

from .core import HandDetector
from .utils import calculate_distance


class GesturePainter(HandDetector):
    """HandDetector를 상속받아 특정 제스처(그리기 모드)를 판별하고 누적 선을 그리는 클래스."""

    def __init__(
        self,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        draw_color=(0, 0, 255)
    ):
        """부모 생성자를 호출하고 선을 영구 기록할 독립 캔버스 메모리를 할당합니다.

        :param max_num_hands: 검출할 최대 손의 개수 (int)
        :param min_detection_confidence: 검출 최소 신뢰도 임계값 (float)
        :param min_tracking_confidence: 추적 최소 신뢰도 임계값 (float)
        :param draw_color: 캔버스에 그릴 선의 BGR 색상 튜플 (tuple)
        """
        super().__init__(
            max_num_hands,
            min_detection_confidence,
            min_tracking_confidence
        )
        self.draw_color = draw_color
        # 영구적인 그림 궤적 저장을 위한 투명 캔버스와 실시간 이전 좌표 기억 장치
        self.canvas = None
        self.prev_x, self.prev_y = 0, 0

    def is_drawing_mode(self, lm_list):
        """검지 손가락만 명확하게 펼쳐진 그리기 모드 상태인지 판별합니다.

        :param lm_list: find_positions 메서드에서 추출된 21개 랜드마크 픽셀 좌표 리스트 (list)
        :return: 그리기 모드(검지 오픈 및 중지 클로즈) 조건 충족 여부 (bool)
        """
        # 부모의 방어 코드를 활용해 유효성 검사
        if not self._is_valid_list(lm_list):
            return False


        try:
            # 부모 클래스의 전역 상수를 바인딩하여 함수 내 대문자 변수 선언 경고 회피
            idx_tip_y = lm_list[self.INDEX_FINGER_TIP][self.Y_COORD_IDX]
            idx_pip_y = lm_list[self.INDEX_FINGER_PIP][self.Y_COORD_IDX]
            mid_tip_y = lm_list[self.MIDDLE_FINGER_TIP][self.Y_COORD_IDX]
            mid_pip_y = lm_list[self.MIDDLE_FINGER_PIP][self.Y_COORD_IDX]
        except IndexError:
            # 리스트 크기가 부족해 좌표를 가져오지 못하면 false
            return False

        index_finger_open = idx_tip_y < idx_pip_y
        middle_finger_closed = mid_tip_y > mid_pip_y

        return index_finger_open and middle_finger_closed

    def draw_canvas(self, frame, lm_list):
        """검지 손가락의 궤적을 투명 캔버스에 선으로 누적하고 원본 프레임과 마스크 합성합니다.

        :param frame: 웹캠으로부터 입력받은 현재 이미지 프레임 (numpy.ndarray 또는 None)
        :param lm_list: find_positions 메서드에서 추출된 랜드마크 픽셀 좌표 리스트 (list)
        :return: 캔버스 선 궤적이 누적 합성된 최종 이미지 프레임 (numpy.ndarray 또는 None)
        """
        if frame is None:
            return None

        # 캔버스가 비어있다면 현재 카메라 프레임 크기와 동일한 검은색 도화지 생성
        if self.canvas is None:
            self.canvas = np.zeros_like(frame)

        if self.is_drawing_mode(lm_list):
            # [도우미 메서드 활용] 복잡한 좌표 계산 및 실시간 선 드로잉 로직을 비공개 메서드로 위임
            self._accumulate_trajectory(lm_list)
        else:
            # 그리기 모드가 해제(손을 접음)되면 선이 엉뚱하게 이어지지 않도록 원점 초기화
            self.prev_x, self.prev_y = 0, 0

        # 캔버스에 그려진 빨간 선들을 원본 프레임에 정밀 병합 (이진 마스크 연산)
        gray_canvas = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        # 선이 그어진 부분(값이 0이 아닌 부분)을 흰색(255)으로 추출
        _, mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)

        foreground = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        background = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))

        return cv2.add(background, foreground)

    def _accumulate_trajectory(self, lm_list):
        """[Protected Helper] 외부에 노출하지 않고 내부적으로 손가락 이동 궤적을 계산하여 선을 누적하는 도우미 메서드."""
        

        # 부모 클래스 상수를 참조하여 PEP 8 Naming 관동 완벽 방어
        cx = lm_list[self.INDEX_FINGER_TIP][self.X_AXIS_IDX]
        cy = lm_list[self.INDEX_FINGER_TIP][self.Y_AXIS_IDX]

        # 처음 그리기를 시작할 때 이전 좌표를 현재 좌표로 초기 동기화
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = cx, cy

        # [utils.py 활용] 손가락의 프레임 간 찰나의 이동 거리를 계산 (순간이동 튐 현상 제어)
        dist = calculate_distance((self.prev_x, self.prev_y), (cx, cy))

        # 오차 범위(65픽셀) 이내의 정상적인 움직임일 때만 연속된 부드러운 선으로 연결
        if dist < 65:
            cv2.line(
                self.canvas, (self.prev_x, self.prev_y), (cx, cy),
                self.draw_color, thickness=10
            )

        # 다음 프레임을 위한 좌표 저장
        self.prev_x, self.prev_y = cx, cy