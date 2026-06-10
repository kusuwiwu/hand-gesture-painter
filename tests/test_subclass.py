import pytest
from my_package.subclass import GesturePainter

def test_painter_initialization():
    """[Normal 3] 자식 클래스가 부모의 속성을 상속받고 고유 색상을 올바르게 초기화하는지 검증합니다."""
    painter = GesturePainter(draw_color=(255, 0, 0))
    assert painter.max_num_hands == 1
    assert painter.draw_color == (255, 0, 0)

def test_is_drawing_mode_true():
    """[Normal 4] 검지는 펴지고 중지는 접혔으며, 두 손가락 거리가 충분할 때 그리기 모드가 True가 되는지 검증합니다."""
    painter = GesturePainter()
    # 21개 기본 좌표 생성 (y값이 클수록 화면 아래쪽임)
    lm_list = [(i, 100, 100) for i in range(21)]
    
    # 검지 조건 성립: 끝마디(8번) y가 중간마디(6번) y보다 위(작음)에 있음
    lm_list[8] = (8, 100, 50)
    lm_list[6] = (6, 100, 100)
    
    # 중지 조건 성립: 끝마디(12번) y가 중간마디(10번) y보다 아래(큼)에 있음 (접힘)
    lm_list[12] = (12, 150, 150)
    lm_list[10] = (10, 150, 100)
    
    # 8번과 12번 사이의 거리는 (100,50)과 (150,150) -> 거리가 20보다 크므로 완벽 부합
    assert painter.is_drawing_mode(lm_list) is True

def test_is_drawing_mode_false_when_middle_finger_open():
    """[Normal 5] 검지와 중지가 둘 다 펼쳐졌을 때는 그리기 모드가 작동하지 않고 False가 되는지 검증합니다."""
    painter = GesturePainter()
    lm_list = [(i, 100, 100) for i in range(21)]
    
    # 검지 펴짐☝️
    lm_list[8] = (8, 100, 50)
    lm_list[6] = (6, 100, 100)
    
    # 중지도 같이 펴짐✌️ (끝마디 y가 중간마디 y보다 위에 위치)
    lm_list[12] = (12, 150, 50)
    lm_list[10] = (10, 150, 100)
    
    assert painter.is_drawing_mode(lm_list) is False

def test_is_drawing_mode_insufficient_landmarks():
    """[Edge 5] 손가락 검출 좌표 개수가 21개 미만으로 깨져서 들어올 때 index error 없이 인식을 차단하는지 검증합니다."""
    painter = GesturePainter()
    invalid_lm_list = [(0, 0, 0), (1, 10, 10)] # 좌표가 2개밖에 없는 상황
    assert painter.is_drawing_mode(invalid_lm_list) is False