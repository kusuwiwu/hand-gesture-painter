import cv2

from my_package.subclass import GesturePainter

# 메인 시스템 제어용 상수 정의
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


if __name__ == "__main__": #이파일으 직접실행했을때만 main()실행
    main()