(1)프로젝트 개요.
본 프로그램은 python 프로그래밍(8257)기말과제 대체 python 프로그래밍 기말 프로젝트를 위해 제작되었으며 제작목적은 손동작을 인식해서 마우스를 움직이게하는 프로토타입 입니다.
q를눌러 나갈수있으며 특정손동작( 검지와 엄지를 모으는)을통해 마우스를 움직일수 있습니다.


(2)설치방법
필수 설치 라이브러리
opencv-python>=4.5.0
numpy>=1.20.0
mediapipe>= 0.8.0
pytest >= 7.0.0 (테스트용)

pip install .

(3)빠른 시작
main.py실행시 또는 아래 코드를 실행시 가능.

import cv2
from my_package.subclass import GesturePainter

def main():
    # 제스처 페인터 초기화 (그리기 색상: 빨간색)
    painter = GesturePainter(max_num_hands=1, min_detection_confidence=0.7, draw_color=(0, 0, 255))
    
    # 웹캠 비디오 캡처 시작
    cap = cv2.VideoCapture(0)
    print("프레임 캡처를 시작합니다. 종료하려면 'q'를 누르세요.")
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("카메라 프레임을 읽을 수 없습니다.")
            break
            
        # 좌우 반전 (거울 모드)
        frame = cv2.flip(frame, 1)
        
        # 손 랜드마크 검출
        lm_list = painter.find_positions(frame)
        
        # 그리기 모드 여부 판별 및 시각화
        if painter.is_drawing_mode(lm_list):
            cv2.putText(frame, "Drawing Mode Active", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 검지 손가락 끝(8번) 좌표에 드로잉 서클 표시
            cx, cy = lm_list[8][1], lm_list[8][2]
            cv2.circle(frame, (cx, cy), 15, painter.draw_color, cv2.FILLED)
        
        # 결과 화면 출력
        cv2.imshow("Hand Gesture Painter", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

(4)주요기능설명


(5)테스트방법
pytest -v를통해 디렉토리에서 10개의 테스트 케이스를 거치게됨.

(5-1)pytest 결과

(6)작성자정보 
소속학교 건국대학교 글로컬캠퍼스
학번/학년 202620888 1학년 
소속학과 컴퓨터공학과 
이름 이현우 