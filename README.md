## (1)제작 목적
 본 프로그램은 python 프로그래밍(8257)기말과제 대체 python 프로그래밍 기말 프로젝트를 위해 제작되었음.

## 수행하는기능
 웹캠이 손을 인식해서 랜드마크로 추적 및 검지손가락을 인식해서 빨간색 선을 긋게 하는기능을 수행.

## 핵심 기능
 검지손가락 만을 펼쳤을때 그리기 모드가 활성화되어 검지손가락으로 빨간선을 그을수 있음.종료 메커니즘 q를눌러 리소스 헤제 및 프로그램을 종료시킴.


## (2)설치방법필수 설치 라이브러리
 opencv-python == 4.9.0.80
 numpy == 1.26.4
 mediapipe == 0.10.14
 pytest == 8.1.1 
 (requirements.txt에 나와있음.)
 반드시 python 3.11.0 버전에서 실행

 프로젝트 루트 디렉토리에서 아래명령어 수행 및 다운
 pip install .

## (3)빠른 시작
 main.py실행시 또는 아래 코드를 실행시 가능.

 ```python
 import cv2

 from my_package.subclass import GesturePainter
  
 메인 시스템 제어용 상수 정의
 CAMERA_ID = 0 # 사용할카메라번호 0=기본웹캠
 FLIP_MIRROR = 1 # 화면좌우반전(거울처럼보이게)
 DELAY_MS = 1 # 키보드 입력 검사 주기(ms)
 
 HUD_POSITION = (10, 50) # 상태 메시지 출력 위치
 FONT_SCALE = 1 # 글자 크기
 HUD_COLOR_BGR = (0, 255, 0) # 상태 메시지 색상 초록색
 LINE_THICKNESS = 2 # 상태 메시지 두께

 def main():
    """실시간 웹캠 인터페이스를 제어하고 화면에 감지 결과를 렌더링

    :return: 변환값 없음(None)
    """
    painter = GesturePainter( # 손 인식 및 그림 그리기 객체 생성
        max_num_hands=1, # 최대 손 개수 = 1
        min_detection_confidence=0.7, # 인식 신뢰도 = 0.7
        draw_color=(0, 0, 255) # 그림 색상 = 빨간색
    )

    cap = cv2.VideoCapture(CAMERA_ID) # 웹캠열기
    print("프레임 캡처를 시작합니다. 종료하려면 'q'를 누르세요.")

    while cap.isOpened(): # 카메라가 열려있는 동안 계속 실행
        success, frame = cap.read() # 웹캠 영상 한 장 읽기
        if not success: #성공여부 확인
            print("카메라 프레임을 읽을 수 없습니다.")
            break

        frame = cv2.flip(frame, FLIP_MIRROR) #거울모드 활성화

        # 랜드마크 좌표 추출
        lm_list = painter.find_positions(frame)

        # 손 뼈대를 화면에 그림
        frame = painter.draw_skeleton(frame)

        # 손가락 움직임을 캔버스에 저장 저장된선 화면에 합성
        frame = painter.draw_canvas(frame, lm_list)

        # 상단 HUD 정보 상태창 렌더링
        if painter.is_drawing_mode(lm_list): # 현재 그리기 모드인지 확인
            cv2.putText( #화면상단에 Drawing Mode Active 출력
                frame, "Drawing Mode Active", HUD_POSITION, # 상태 확인 쉽게 하기 위해 hub출력
                cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, # 폰트,크기,색깔,굵기 정함
                HUD_COLOR_BGR, LINE_THICKNESS
            )

        cv2.imshow("Hand Gesture Painter", frame) #최종화면 출력

        if cv2.waitKey(DELAY_MS) & 0xFF == ord("q"): #q 입력시 종료
            break

    cap.release() #웹캠 사용 종료
    cv2.destroyAllWindows() # 모든 OpenCV 창 닫기
 if __name__ == "__main__": #이파일을 직접실행했을때만 main()실행
    main()
```

## (4)주요기능설명
 1mediapipe를 통해서 손을 인식 가능하다.
 2랜드마크를 통해서 손관절 21개의 좌표를 추출하고 손관절의 연결선을 화면에 표시할수있다.
 3검지는 펴고 중지는 접은 상태인지 판별할수있다.
 4이전 좌표와 현재 좌표를 연결하여 지속적으로 그림 유지할수 있다.
 5손 인식이 순간적으로 튀는 경우 잘못된 선을 방지할수 있다.
 6현재 상태가 그리기 모드인지 화면에 표시할수있다.

## (5)테스트방법
 pytest -v를통해 디렉토리에서 13개의 테스트 케이스를 거치게됨.
 cmd 기준
 python -m venv .venv 가상환경 설정
 call .venv\Scripts\activate 가상환경 활성화
 pip install -r requirements.txt 목록 라이브러리 설치
 pip install . 파이썬 파일 다운
 pytest -v 파이테스트 실행

## (5-1)pytest 결과
 (.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pytest -v
 ======================================= test session starts ========================================
 platform win32 -- Python 3.11.0, pytest-8.1.1, pluggy-1.6.0 -- C:\Users\User\Desktop\hand_gesture_painter_work\.venv\Scripts\python.exe
 cachedir: .pytest_cache
 rootdir: C:\Users\User\Desktop\hand_gesture_painter_work
 collected 13 items                                                                                  
 
 tests/test_core.py::test_find_positions_none_image PASSED                                     [  7%]
 tests/test_core.py::test_is_valid_list_normal_data PASSED                                     [ 15%]
 tests/test_core.py::test_is_valid_list_none_input INFO: Created TensorFlow Lite XNNPACK  delegate for CPU.
 PASSED                                      [ 23%]
 tests/test_core.py::test_is_valid_list_empty_list PASSED                                      [ 30%]
 tests/test_subclass.py::test_gesture_painter_color_initialization PASSED                      [ 38%]
 tests/test_subclass.py::test_is_drawing_mode_none_input PASSED                                [ 46%]
 tests/test_subclass.py::test_is_drawing_mode_empty_list PASSED                                [ 53%]
 tests/test_subclass.py::test_is_drawing_mode_boundary_equal_coordinates PASSED                [ 61%]
 tests/test_subclass.py::test_is_drawing_mode_invalid_primitive_type PASSED                    [ 69%]
 tests/test_subclass.py::test_draw_canvas_accumulates_lines PASSED                             [ 76%]
 tests/test_utils.py::test_calculate_distance_normal_coordinates PASSED                        [ 84%]
 tests/test_utils.py::test_calculate_distance_boundary_zero PASSED                             [ 92%]
 tests/test_utils.py::test_calculate_distance_invalid_primitive_type PASSED                    [100%]
 W0000 00:00:1781443285.985803  170396 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
 
 ======================================== 13 passed in 1.94s   ========================================
 W0000 00:00:1781443286.060330  171588 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
 W0000 00:00:1781443286.073978  172252 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
 W0000 00:00:1781443286.080406  173776 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.

## 5-3 프로젝트 구조
 hand_gesture_painter_work/
 │
 ├── my_package/
 │   ├── __init__.py
 │   ├── core.py
 │   ├── subclass.py
 │   └── utils.py
 │
 ├── tests/
 │   ├── __init__.py
 │   ├── test_core.py
 │   ├── test_subclass.py
 │   └── test_utils.py
 │
 ├── .gitignore
 ├── main.py
 ├── README.md
 ├── requirements.txt
 ├── setup.py
 ├── self_review.md
 ├── results.md
 │
 ├── pip_install_result.png
 ├── pip_install_result1.png
 ├── pycodestyle_result.png
 ├── pycodestyle_result1.png
 ├── pycodestyle_result2.png
 └── pytest_result.png

## (6)작성자정보 
 소속학교 건국대학교 글로컬캠퍼스
 학번/학년 202620888 1학년 
 소속학과 컴퓨터공학과
 이름 이현우 (Lee Hyun-Woo )

## (7) github url
 https://github.com/kusuwiwu/hand-gesture-painter

