import pytest
from my_package.utils import calculate_distance

def test_calculate_distance_normal():
    """[Normal 1] 일반적인 피타고라스 정리가 성립하는 직각삼각형 거리 계산을 검증합니다."""
    point1 = (0, 0)
    point2 = (3, 4)
    # 3^2 + 4^2 = 5^2 이므로 거리는 5.0이 나와야 합니다.
    assert calculate_distance(point1, point2) == pytest.approx(5.0)

def test_calculate_distance_same_point():
    """[Edge 1] 두 점이 완전히 동일한 위치에 있을 때 거리가 0.0이 되는지 검증합니다."""
    point1 = (100, 200)
    point2 = (100, 200)
    assert calculate_distance(point1, point2) == 0.0