import pytest
from my_package.subclass import GesturePainter
from my_package.utils import calculate_distance

def test_calculate_distance():
    """도우미 함수 테스트: 두 좌표 사이의 거리가 올바르게 계산되는지 검증"""
    pt1 = (0, 0)
    pt2 = (3, 4) # 3:4:5 직각삼각형 원리 이용
    assert calculate_distance(pt1, pt2) == 5.0

def test_is_drawing_mode_false_when_no_hand():
    """자식 클래스 테스트: 랜드마크 데이터가 부족할 때 그리기 모드가 False를 반환하는지 검증"""
    painter = GesturePainter()
    assert painter.is_drawing_mode([]) is False

def test_is_drawing_mode_true_condition():
    """자식 클래스 테스트: 검지만 펴지고 중지는 접혔을 때 그리기 모드(True)가 되는지 검증"""
    painter = GesturePainter()
    
    # 21개의 가짜 랜드마크 좌표 리스트 생성 (기본값 다 (0,0)으로 세팅)
    dummy_landmarks = [(i, 0, 0) for i in range(21)]
    
    # 검지 손가락: 끝(8번)의 y가 마디(6번)의 y보다 작아야 함 (펴짐)
    dummy_landmarks[8] = (8, 0, 100)
    dummy_landmarks[6] = (6, 0, 200)
    
    # 중지 손가락: 끝(12번)의 y가 마디(10번)의 y보다 커야 함 (접힘)
    dummy_landmarks[12] = (12, 0, 300)
    dummy_landmarks[10] = (10, 0, 200)
    
    assert painter.is_drawing_mode(dummy_landmarks) is True