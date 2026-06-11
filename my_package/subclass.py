import cv2
import numpy as np
import ctypes
from my_package.core import HandDetector

class GesturePainter(HandDetector):
    """HandDetector를 상속받아 마우스 제어 및 실시간 캔버스 드로잉 기능을 수행하는 자식 클래스"""
    
    def __init__(self, max_num_hands=1, min_detection_confidence=0.7, draw_color=(0, 0, 255)):
        # 부모 클래스의 생성자 호출 (과제 필수 요구사항 보장)
        super().__init__(max_num_hands, min_detection_confidence)
        self.draw_color = draw_color
        
        # 모니터 해상도 획득
        self.user32 = ctypes.windll.user32
        self.screen_width = self.user32.GetSystemMetrics(0)
        self.screen_height = self.user32.GetSystemMetrics(1)
        
        # 드로잉 및 스무딩 상태 변수
        self.canvas = None
        self.xp, self.yp = 0, 0
        self.cloc_x, self.cloc_y = 0, 0

    def is_drawing_mode(self, lm_list):
        """검지 손가락만 올라와서 그리기/이동 모드 상태인지 판별합니다.
        
        :param lm_list: 21개 손 랜드마크 좌표 리스트
        :return: 모드 활성화 여부 (Boolean)
        """
        if not self._is_valid_list(lm_list):
            return False
        # 검지는 펼쳐지고(8번 끝이 6번보다 위), 중지는 접힌 상태(12번 끝이 10번보다 아래)
        return lm_list[8][2] < lm_list[6][2] and lm_list[12][2] > lm_list[10][2]

    def draw_and_move(self, img, lm_list, smoothening=5):
        """마우스를 이동시키고 그리기 모드일 때 자식 클래스의 고유 캔버스에 선을 그립니다."""
        h, w, c = img.shape
        if self.canvas is None:
            self.canvas = np.zeros((h, w, 3), dtype=np.uint8)

        if self._is_valid_list(lm_list):
            cx, cy = lm_list[8][1], lm_list[8][2]
            
            # 좌표 변환 및 평활화 (Smoothing)
            target_x = (cx / w) * self.screen_width
            target_y = (cy / h) * self.screen_height
            self.cloc_x += (target_x - self.cloc_x) / smoothening
            self.cloc_y += (target_y - self.cloc_y) / smoothening
            
            # 마우스 이동 (비공개 메서드 우회 호출)
            self._safe_move_mouse(int(self.cloc_x), int(self.cloc_y))
            
            if self.is_drawing_mode(lm_list):
                cv2.circle(img, (cx, cy), 7, self.draw_color, cv2.FILLED)
                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = cx, cy
                cv2.line(self.canvas, (self.xp, self.yp), (cx, cy), self.draw_color, 5)
                self.xp, self.yp = cx, cy
            else:
                cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
                self.xp, self.yp = 0, 0
        else:
            self.xp, self.yp = 0, 0

        # 캔버스 합성 연산
        img_gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
        img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, img_inv)
        img = cv2.bitwise_or(img, self.canvas)
        return img

    def _safe_move_mouse(self, x, y):
        """[비공개 메서드] 화면 해상도 범위를 벗어나지 않도록 안전하게 마우스를 이동시킵니다."""
        safe_x = max(0, min(x, self.screen_width - 1))
        safe_y = max(0, min(y, self.screen_height - 1))
        self.user32.SetCursorPos(safe_x, safe_y)