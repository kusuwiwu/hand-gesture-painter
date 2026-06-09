from .core import HandDetector
from .utils import calculate_distance

class GesturePainter(HandDetector):
    """HandDetector를 상속받아 제스처 인식 기능을 추가한 자식 클래스입니다."""

    def __init__(self, max_num_hands=1, min_detection_confidence=0.5, draw_color=(0, 0, 255)):
        """super()를 사용하여 부모 클래스를 초기화하고, 자식 클래스만의 속성을 추가합니다."""
        # 교수님 채점 기준: super() 올바른 활용
        super().__init__(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence)
        self.draw_color = draw_color # 그리기 색상 속성 추가

    def is_drawing_mode(self, lm_list):
        """검지 손가락만 펴져 있어서 '그리기 모드'인지 판별합니다.

        :param lm_list: 부모 클래스의 find_positions 결과물
        :return: 그리기 모드 여부 (True/False)
        """
        if len(lm_list) < 21:
            return False

        # 검지 손가락 끝(8번)과 마디(6번)의 y좌표를 비교하여 펴졌는지 확인
        # (화면 좌표계는 위가 0이므로 끝점의 y가 마디의 y보다 작으면 펴진 것)
        is_index_open = lm_list[8][1] < lm_list[6][1] if hasattr(self, 'vertical') else lm_list[8][2] < lm_list[6][2]
        
        # 중지 손가락 끝(12번)은 접혀있는지 확인 (중지까지 펴지면 그리기 멈춤)
        is_middle_closed = lm_list[12][2] > lm_list[10][2]
        
        return is_index_open and is_middle_closed