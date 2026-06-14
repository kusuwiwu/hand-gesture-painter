import math # 제곱근(sqrt) 계산을 위한 math 모듈 사용


def calculate_distance(p1, p2): #(id,x,y), (x,y) 둘다 지원
    """두 랜드마크 좌표 사이의 직선(유클리드) 거리를 연산하는 유틸리티 함수.

    :param p1: 첫 번째 포인트의 (ID, X, Y) 또는 (X, Y) 데이터 (tuple)
    :param p2: 두 번째 포인트의 (ID, X, Y) 또는 (X, Y) 데이터 (tuple)
    :return: 두 지점 사이의 수학적 직선 거리 (float)

    Example:
        >>> calculate_distance((0, 0), (3, 4))
        5.0
        >>> calculate_distance((8, 10, 10), (6, 13, 14))
        5.0
    """
    x_offset = -2 #뒤에서 2번째 x축좌표사용 (id,x,y), (x,y) 두가지형식다 처리하기위해서
    y_offset = -1 #뒤에서 1번째 y축 좌표사용 

    x1, y1 = p1[x_offset], p1[y_offset] #첫번째 점 좌표 추출
    x2, y2 = p2[x_offset], p2[y_offset] #두번째 점 좌표 추출

    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) # 유클리드 거리 공식 사용 두점사이 거리계산
