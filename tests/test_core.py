import pytest
import numpy as np
from unittest.mock import MagicMock
from my_package.core import HandDetector

def test_find_positions_with_empty_image():
    """정상 케이스: 빈 이미지가 들어왔을 때 빈 리스트를 반환하는지 테스트"""
    detector = HandDetector()
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    result = detector.find_positions(dummy_img)
    assert result == []

def test_preprocess_image_with_none():
    """엣지 케이스: 이미지 대신 None이 들어왔을 때 안전하게 None을 반환하는지 테스트"""
    detector = HandDetector()
    result = detector._preprocess_image(None)
    assert result is None

def test_find_positions_with_mocking():
    """전문적 테스트: 환경 차이를 극복하기 위해 Mock 객체를 활용한 검출 로직 테스트"""
    detector = HandDetector()
    
    # 가짜 hands 객체와 결과물 조립 (버전 에러 우회)
    mock_hands = MagicMock()
    mock_results = MagicMock()
    
    # 가짜 랜드마크 데이터 생성 (x=0.5, y=0.5 자리에 손이 있다고 가공)
    mock_landmark = MagicMock()
    mock_landmark.x = 0.5
    mock_landmark.y = 0.5
    
    mock_hand_landmarks = MagicMock()
    mock_hand_landmarks.landmark = [mock_landmark]
    
    mock_results.multi_hand_landmarks = [mock_hand_landmarks]
    mock_hands.process.return_value = mock_results
    
    # 강제로 가짜 객체를 주입하여 로직 검증
    detector.hands = mock_hands
    
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    result = detector.find_positions(dummy_img)
    
    # 100x100 해상도의 0.5 비율이므로 (50, 50) 좌표가 잘 추출되었는지 검증
    assert len(result) == 1
    assert result[0][1] == 50
    assert result[0][2] == 50