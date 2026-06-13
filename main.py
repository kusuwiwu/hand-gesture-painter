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