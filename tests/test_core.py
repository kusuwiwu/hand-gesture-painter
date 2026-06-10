import pytest
import numpy as np
from unittest.mock import MagicMock
from my_package.core import HandDetector

def test_detector_initialization_defaults():
    """[Normal 2] HandDetector 생성 시 기본 매개변수 인자가 정상적으로 할당되는지 검증합니다."""
    detector = HandDetector()
    assert detector.max_num_hands == 1
    assert detector.min_detection_confidence == 0.5

def test_preprocess_none_image():
    """[Edge 2] 이미지 데이터 자리에 None이 들어왔을 때 에러 없이 None을 반환하는지 검증합니다."""
    detector = HandDetector()
    assert detector._preprocess_image(None) is None

def test_find_positions_when_hands_none():
    """[Edge 3] MediaPipe 객체가 초기화되지 않았거나 손이 없을 때 빈 리스트를 반환하는지 검증합니다."""
    detector = HandDetector()
    detector.hands = None  # 임의로 라이브러리 연결을 끊음
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    assert detector.find_positions(dummy_img) == []

def test_find_positions_empty_results():
    """[Edge 4] 이미지는 정상이지만 영상 내에 손이 단 하나도 없을 때 빈 리스트를 검증합니다."""
    detector = HandDetector()
    detector.hands = MagicMock()
    # process 메서드가 손을 검출하지 못한 상황을 모킹
    detector.hands.process.return_value.multi_hand_landmarks = None
    
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    results = detector.find_positions(dummy_img)
    assert results == []