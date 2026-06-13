import pytest

from my_package.core import HandDetector


def test_find_positions_none_image():
    """[엣지: None] 이미지에 None이 주입되어도 안전하게 빈 리스트를 반환."""
    detector = HandDetector()
    assert detector.find_positions(None) == []


# [변경] _preprocess_image 메서드는 새 기능 코드에서 통합 제거되었으므로 테스트 대상에서 제외합니다.


def test_is_valid_list_normal_data():
    """[정상] 유효한 랜드마크 데이터 배열이 들어오면 True를 반환."""
    detector = HandDetector()
    normal_landmarks = [(i, 100, 200) for i in range(21)]
    assert detector._is_valid_list(normal_landmarks) is True


def test_is_valid_list_none_input():
    """[엣지: None] 유효성 검사기에 명시적인 None 주입 시 False를 반환하는지 격리 검증."""
    detector = HandDetector()
    assert detector._is_valid_list(None) is False


def test_is_valid_list_empty_list():
    """[엣지: 빈 리스트] 요소가 전혀 없는 빈 배열 주입 시 False를 반환하는지 격리 검증."""
    detector = HandDetector()
    assert detector._is_valid_list([]) is False