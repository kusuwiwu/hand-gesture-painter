import pytest
from my_package.utils import calculate_distance


def test_calculate_distance_normal_coordinates():
    """[정상] 정수 비례 배치의 3차원 좌표 간 유클리드 거리를 정확히 연산."""
    node_a = (8, 10, 10)
    node_b = (6, 13, 14)
    assert calculate_distance(node_a, node_b) == 5.0


def test_calculate_distance_boundary_zero():
    """[엣지: 경계값] 동일한 두 좌표 사이의 거리가 오차 없이 0.0이 되는지 검증."""
    node_a = (8, 10, 10)
    node_b = (8, 10, 10)
    assert calculate_distance(node_a, node_b) == 0.0


def test_calculate_distance_invalid_primitive_type():
    """[엣지: 잘못된 타입] 튜플 대신 정수 주입 시 TypeError가 정상 발생하느냐?"""
    with pytest.raises(TypeError):
        # 인덱서 가동이 불가능하므로 파이썬 내장 에러가 던져져야 정상 방어입니다.
        calculate_distance(12345, 67890)