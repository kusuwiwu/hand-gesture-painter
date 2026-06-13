(1)프로젝트 개요.
본 프로그램은 python 프로그래밍(8257)기말과제 대체 python 프로그래밍 기말 프로젝트를 위해 제작되었음.
제작목적은 웹캠이 손을 인식해서 랜드마크로 추적하고 마우스를 움직이는 기능을 수행 및 검지손가락을 인식해서 빨간색 선을 긋게 하는기능을 수행.  마우스 포인터를 대체할수 있는 기능을 테스트 하는것임.
핵심 기능 검지손가락 만을 펼쳤을때 그리기 모드가 활성화되어 검지손가락으로 빨간선을 그을수 있음.
종료 메커니즘 q를눌러 리소스 헤제 및 프로그램을 종료시킴.


(2)설치방법
필수 설치 라이브러리
opencv-python>=4.5.0
numpy>=1.20.0
mediapipe>= 0.8.0
pytest >= 7.0.0
(requirements.txt에 나와있음.)
반드시 python 3.11.0 버전에서 실행

프로젝트 루트 디렉토리에서 아래명령어 수행 및 다운
pip install .

(3)빠른 시작
main.py실행시 또는 아래 코드를 실행시 가능.

import cv2

from my_package.subclass import GesturePainter

# [마법의 숫자 제거] 최상단 공간에 메인 시스템 제어용 상수를 전면 전역화.
CAMERA_ID = 0
FLIP_MIRROR = 1
DELAY_MS = 1

HUD_POSITION = (10, 50)
FONT_SCALE = 1
HUD_COLOR_BGR = (0, 255, 0)
LINE_THICKNESS = 2


def main():
    """실시간 웹캠 인터페이스를 제어하고 화면에 감지 결과를 렌더링합니다.

    :return: 변환값 없음(None)
    """
    painter = GesturePainter(
        max_num_hands=1,
        min_detection_confidence=0.7,
        draw_color=(0, 0, 255)
    )

    cap = cv2.VideoCapture(CAMERA_ID)
    print("프레임 캡처를 시작합니다. 종료하려면 'q'를 누르세요.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("카메라 프레임을 읽을 수 없습니다.")
            break

        frame = cv2.flip(frame, FLIP_MIRROR)

        # [SRP 준수] 순수하게 연산 데이터 배열만 추출합니다.
        lm_list = painter.find_positions(frame)

        # [SRP 준수] 시각화 기능 작동이 필요할 때 명시적으로 별도 호출.
        frame = painter.draw_skeleton(frame)

        # [SRP 준수] 손가락의 궤적을 영구 캔버스에 그리고 비디오 프레임 위에 합성합니다.
        frame = painter.draw_canvas(frame, lm_list)

        # 상단 HUD 정보 상태창 렌더링
        if painter.is_drawing_mode(lm_list):
            cv2.putText(
                frame, "Drawing Mode Active", HUD_POSITION,
                cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE,
                HUD_COLOR_BGR, LINE_THICKNESS
            )

        cv2.imshow("Hand Gesture Painter", frame)

        if cv2.waitKey(DELAY_MS) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

(4)주요기능설명
부모 클래스의 전처리와 랜드마크를 통해 손을 추적하며 이를 자식클래스의 고유 손동작 모델과 결합하여 코드의 효율성을극대화함. 

웹캠에서 손을 확인할수 없는 상황에서도 프로그램이 종료되지않게(크래시 없이) 코드를 짜고 안전하게 반환되도록 설계함.

윈도우 맥 등의 다양한 환경을 지원하며 다양한 환경에서 독립적으로 작동하도록 속성과 버전을 구성했습니다.
pytest를 통한 12개의 단위테스트를 언제든지 통과가능하도록 설계되었습니다.

(5)테스트방법
pytest -v를통해 디렉토리에서 12개의 테스트 케이스를 거치게됨.
cmd 기준
python -m venv .venv 가상환경 설정
call .venv\Scripts\activate 가상환경 활성화
pip install -r requirements.txt 목록 라이브러리 설치
pip install -e . 개발모드 패키지 등록
pytest -v 파이테스트 실행


(5-1)pytest 결과
============================================================ test session starts =============================================================
platform win32 -- Python 3.11.0, pytest-8.1.1, pluggy-1.6.0 -- C:\Users\User\Desktop\hand_gesture_painter_work\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\User\Desktop\hand_gesture_painter_work
collected 11 items                                                                                                                            

tests/test_core.py::test_find_positions_none_image PASSED                                                                               [  9%]
tests/test_core.py::test_is_valid_list_normal_data PASSED                                                                               [ 18%]
tests/test_core.py::test_is_valid_list_none_or_empty INFO: PASSEDCreated TensorFlow Lite XNNPACK delegate for CPU.
                                                                             [ 27%]
tests/test_subclass.py::test_gesture_painter_color_initialization PASSED                                                                [ 36%]
tests/test_subclass.py::test_is_drawing_mode_none_input PASSED                                                                          [ 45%]
tests/test_subclass.py::test_is_drawing_mode_empty_list PASSED                                                                          [ 54%]
tests/test_subclass.py::test_is_drawing_mode_boundary_equal_coordinates PASSED                                                          [ 63%]
tests/test_subclass.py::test_draw_canvas_accumulates_lines PASSED                                                                       [ 72%]
W0000 00:00:1781354139.148867  111288 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
tests/test_utils.py::test_calculate_distance_normal_coordinates PASSED                                                                  [ 81%]
tests/test_utils.py::test_calculate_distance_boundary_zero PASSED                                                                       [ 90%]
tests/test_utils.py::test_calculate_distance_invalid_primitive_type PASSED                                                              [100%]W0000 00:00:1781354139.158704  120436 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.


============================================================= 11 passed in 3.78s =============================================================

5-2 프로젝트 구조
hand_gesture_painter_work
my_package 핵심 엔진 폴더
 __init__.py
 core.py 부모클레스 영상잔처리 및 랜드마크 추출 예외차단.
 subclass.py 자식클래스 손동작분석 및 동작에따른 모드 판단.
 utils.py 좌표간 거리계산 함수

tests 테스트용 파일
 __init__.py
 test_core.py 부모클레스 영상잔처리 및 랜드마크 추출 예외차단.
 test_subclass.py 자식클래스 손동작분석 및 동작에따른 모드 판단.
 test_utils.py 좌표간 거리계산 함수
main.py 메인코드
READEM.md 설명서
requirements.txt 필요한 외부라이브러리
self_review.md 스스로 점검
stepup.py 패키지 배포 및 빌드 설정 파일

(6)작성자정보 
소속학교 건국대학교 글로컬캠퍼스
학번/학년 202620888 1학년 
소속학과 컴퓨터공학과 
이름 이현우 (Hyun-Woo Lee)