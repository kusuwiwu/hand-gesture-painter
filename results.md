pytest 실행결과
(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pytest -v
======================================= test session starts ========================================
platform win32 -- Python 3.11.0, pytest-8.1.1, pluggy-1.6.0 -- C:\Users\User\Desktop\hand_gesture_painter_work\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\User\Desktop\hand_gesture_painter_work
collected 13 items                                                                                  

tests/test_core.py::test_find_positions_none_image PASSED                                     [  7%]
tests/test_core.py::test_is_valid_list_normal_data PASSED                                     [ 15%]
tests/test_core.py::test_is_valid_list_none_input INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
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

======================================== 13 passed in 1.94s ========================================
W0000 00:00:1781443286.060330  171588 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
W0000 00:00:1781443286.073978  172252 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.
W0000 00:00:1781443286.080406  173776 inference_feedback_manager.cc:114] Feedback manager requires a model with a single signature inference. Disabling support for feedback tensors.

![pytest실행결과](pytest_result.png)


pycodestyle 실행결과

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pycodestyle my_package/

![pycodestyle 실행결과1](pycodestyle_result.png)

pip install . 출력 캡처

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pip install .   
Processing c:\users\user\desktop\hand_gesture_painter_work
  Preparing metadata (setup.py) ... done
Requirement already satisfied: opencv-python==4.9.0.80 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from hand-gesture-painter-work==1.0.0) (4.9.0.80)
Requirement already satisfied: mediapipe==0.10.14 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from hand-gesture-painter-work==1.0.0) (0.10.14)
Requirement already satisfied: numpy==1.26.4 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from hand-gesture-painter-work==1.0.0) (1.26.4)
Requirement already satisfied: absl-py in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (2.4.0)
Requirement already satisfied: attrs>=19.1.0 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (26.1.0)
Requirement already satisfied: flatbuffers>=2.0 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (25.12.19)
Requirement already satisfied: jax in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (0.7.1)
Requirement already satisfied: jaxlib in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (0.7.1)
Requirement already satisfied: matplotlib in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (3.11.0)
Requirement already satisfied: opencv-contrib-python in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (4.11.0.86)
Requirement already satisfied: protobuf<5,>=4.25.3 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (4.25.9)
Requirement already satisfied: sounddevice>=0.4.4 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (0.5.5)
Requirement already satisfied: cffi in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from sounddevice>=0.4.4->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (2.0.0)
Requirement already satisfied: ml_dtypes>=0.5.0 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from jax->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (0.5.4)
Requirement already satisfied: opt_einsum in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from jax->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (3.4.0)
Requirement already satisfied: scipy>=1.12 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from jax->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (1.17.1)
Requirement already satisfied: contourpy>=1.0.1 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (1.3.3)
Requirement already satisfied: cycler>=0.10 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (0.12.1)
Requirement already satisfied: fonttools>=4.22.0 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (4.63.0)
Requirement already satisfied: kiwisolver>=1.3.1 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (1.5.0)
Requirement already satisfied: packaging>=20.0 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (26.2)
Requirement already satisfied: pillow>=9 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (12.2.0)
Requirement already satisfied: pyparsing>=3 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (3.3.2)
Requirement already satisfied: python-dateutil>=2.7 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (2.9.0.post0)
Requirement already satisfied: six>=1.5 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from python-dateutil>=2.7->matplotlib->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (1.17.0)
Requirement already satisfied: pycparser in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from cffi->sounddevice>=0.4.4->mediapipe==0.10.14->hand-gesture-painter-work==1.0.0) (3.0)
Installing collected packages: hand-gesture-painter-work
  DEPRECATION: hand-gesture-painter-work is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for hand-gesture-painter-work ... done
Successfully installed hand-gesture-painter-work-1.0.0

![pip_install_실행결과1](pip install .result.png)
![pip_install_실행결과2](pip install .result1.png)