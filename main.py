import cv2
from my_package.subclass import GesturePainter

def main():
    # 패키지화된 자식 클래스 인스턴스 생성 (README 가이드라인 일치)
    painter = GesturePainter(max_num_hands=1, min_detection_confidence=0.7, draw_color=(0, 0, 255))
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("🚨 에러: 웹캠을 열 수 없습니다.")
        return

    print("\n=== [최종 패키지 프로그램 가동 성공] ===")
    print("- 검지 손가락을 펼치면 마우스가 부드럽게 움직입니다.")
    print("- 창에서 'q' 키를 누르면 종료됩니다.\n")

    cv2.namedWindow("Hand Gesture Mouse", cv2.WINDOW_AUTOSIZE)
    cv2.setWindowProperty("Hand Gesture Mouse", cv2.WND_PROP_TOPMOST, 1)

    while True:
        success, frame = cap.read()
        if not success: 
            break

        # 거울 모드 좌우 반전
        frame = cv2.flip(frame, 1)
        
        # 1. 부모로부터 상속받은 메서드로 랜드마크 추출
        lm_list = painter.find_positions(frame)
        
        # 2. 자식 클래스의 고유 로직으로 마우스 제어 및 합성 드로잉 처리
        frame = painter.draw_and_move(frame, lm_list, smoothening=5)

        cv2.imshow("Hand Gesture Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()