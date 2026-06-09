def calculate_distance(pt1, pt2):
    """두 랜드마크 좌표 (x, y) 사이의 거리를 계산하는 도우미 함수입니다.

    :param pt1: (x1, y1) 튜플
    :param pt2: (x2, y2) 튜플
    :return: 두 점 사이의 유클리드 거리 (float)
    """
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5