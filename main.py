import cv2
import numpy as np
from my_package import GesturePainter

def main():
    # 💡 [원상복구] 다시 실제 물리 카메라(0번)를 직접 호출합니다.
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("에러: 실제 카메라를 열 수 없습니다. 웹캠 연결을 확인하세요.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 그림을 그릴 투명한 스케치북(검은색 빈 이미지)
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # 우리가 상속으로 구현한 자식 클래스 객체 생성 (그리기 색상: 빨간색)
    painter = GesturePainter(draw_color=(0, 0, 255))
    xp, yp = 0, 0

    print("=== [최종 완성] 손 제스처 페인터 시작 ===")
    print("- 검지 손가락만 펴기: 그림 그리기 모드 (빨간색 점)")
    print("- 검지+중지 모두 펴기: 이동 및 대기 모드 (보라색 점)")
    print("- 웹캠 창에서 'q' 키 누르기: 프로그램 종료")

    while True:
        # 실제 카메라로부터 프레임 읽어오기
        success, img = cap.read()
        if not success:
            print("영상을 읽어오는 데 실패했습니다.")
            break

        # 거울 보는 것처럼 자연스럽게 좌우 반전
        img = cv2.flip(img, 1)

        # 1. 부모 클래스에서 상속받은 메서드로 실제 손의 랜드마크 위치 찾기
        lm_list = painter.find_positions(img)

        if len(lm_list) == 21:
            # 검지 손가락 끝점(8번)의 실제 좌표 추출
            cx, cy = lm_list[8][1], lm_list[8][2]

            # 2. 자식 클래스에서 정의한 메서드로 '그리기 모드'인지 검사
            if painter.is_drawing_mode(lm_list):
                # 검지 끝에 작은 빨간색 점을 찍어 조준점 표시
                cv2.circle(img, (cx, cy), 7, painter.draw_color, cv2.FILLED)
                
                if xp == 0 and yp == 0:
                    xp, yp = cx, cy

                # 스케치북에 이전 좌표부터 현재 좌표까지 선 그리기
                cv2.line(canvas, (xp, yp), (cx, cy), painter.draw_color, 5)
                xp, yp = cx, cy
            else:
                # 그리기 모드가 아닐 때는 조준점을 보라색으로 표시하고 선은 안 그어짐
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
                xp, yp = 0, 0 # 좌표 초기화
        else:
            xp, yp = 0, 0

        # 원본 웹캠 영상 위에 우리가 스케치북에 그린 낙서 결합하기
        img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, canvas)

        # 최종 화면 표시
        cv2.imshow("Hand Gesture Painter", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()