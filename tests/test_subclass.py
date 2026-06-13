import pytest
import numpy as np
import cv2

from my_package.subclass import GesturePainter


def test_gesture_painter_color_initialization():
    """[정상] 자식 클래스 생성 시 지정한 BGR 색상 값이 올바르게 세팅되는가?"""
    custom_color = (255, 0, 0)
    painter = GesturePainter(draw_color=custom_color)
    assert painter.draw_color == custom_color


def test_is_drawing_mode_none_input():
    """[엣지: None] 제스처 판별기에 None 주입 시 크래시 없이 False 반환."""
    painter = GesturePainter()
    assert painter.is_drawing_mode(None) is False


def test_is_drawing_mode_empty_list():
    """[엣지: 빈 입력] 빈 리스트([]) 주입 시 인덱스 에러 없이 False 반환."""
    painter = GesturePainter()
    assert painter.is_drawing_mode([]) is False


def test_is_drawing_mode_boundary_equal_coordinates():
    """[엣지: 경계값] 손가락 마디 Y좌표가 완전히 일치할 때의 판정 임계점 검증."""
    painter = GesturePainter()
    mock_lms = [[i, 100, 200] for i in range(21)]

    # 검지 끝(8)과 검지 마디(6)의 Y좌표를 200으로 완전히 일치시킴 (경계값)
    mock_lms[painter.INDEX_FINGER_TIP] = [8, 100, 200]
    mock_lms[painter.INDEX_FINGER_PIP] = [6, 100, 200]

    assert painter.is_drawing_mode(mock_lms) is False

def test_is_drawing_mode_invalid_primitive_type():
    """[엣지: 잘못된 타입] 랜드마크 리스트 자리에 무결하지 않은 정수형 데이터 주입 시 에러 없이 False 반환 조치."""
    painter = GesturePainter()
    # 리스트나 내부 인덱싱 구조가 전혀 없는 잘못된 타입 주입 시 예외 발생 여부 검증
    assert painter.is_drawing_mode(99999) is False
    assert painter.is_drawing_mode("InvalidStringData") is False


def test_draw_canvas_accumulates_lines():
    """[기능] 그리기 모드 상태일 때 영구 캔버스 공간에 선이 정상적으로 축적되는지 검증."""
    painter = GesturePainter()
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    mock_lms = [[i, 100, 200] for i in range(21)]

    # 검지 펼침 및 중지 접음 (그리기 모드 활성화 환경 강제 조성)
    mock_lms[painter.INDEX_FINGER_TIP] = [8, 100, 100]
    mock_lms[painter.INDEX_FINGER_PIP] = [6, 100, 200]
    mock_lms[painter.MIDDLE_FINGER_TIP] = [12, 300, 300]
    mock_lms[painter.MIDDLE_FINGER_PIP] = [10, 300, 250]

    # 프레임 1: 시작점 동기화 (아직 한 점이라 선이 안 생김)
    painter.draw_canvas(mock_frame, mock_lms)
    
    # 프레임 2: 손가락을 이동시켜 선 궤적 누적 유도
    mock_lms[painter.INDEX_FINGER_TIP] = [8, 110, 110]
    painter.draw_canvas(mock_frame, mock_lms)

    # 캔버스에 실제로 선(0이 아닌 색상 값)이 활성화되었는지 판단
    gray_canvas = cv2.cvtColor(painter.canvas, cv2.COLOR_BGR2GRAY)
    assert np.sum(gray_canvas > 0) > 0