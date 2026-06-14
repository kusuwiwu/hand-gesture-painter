pycodestyle 실행결과

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pip install black                                 
Collecting black
  Downloading black-26.5.1-cp311-cp311-win_amd64.whl (1.5 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.5/1.5 MB 4.1 MB/s eta 0:00:00
Collecting click>=8.0.0
  Downloading click-8.4.1-py3-none-any.whl (116 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 116.6/116.6 kB ? eta 0:00:00
Collecting mypy-extensions>=0.4.3
  Downloading mypy_extensions-1.1.0-py3-none-any.whl (5.0 kB)
Requirement already satisfied: packaging>=22.0 in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from black) (26.2)
Collecting pathspec>=1.0.0
  Downloading pathspec-1.1.1-py3-none-any.whl (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 57.3/57.3 kB 2.9 MB/s eta 0:00:00
Collecting platformdirs>=2
  Downloading platformdirs-4.10.0-py3-none-any.whl (22 kB)
Collecting pytokens~=0.4.0
  Downloading pytokens-0.4.1-cp311-cp311-win_amd64.whl (103 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 103.3/103.3 kB 5.8 MB/s eta 0:00:00
Requirement already satisfied: colorama in c:\users\user\desktop\hand_gesture_painter_work\.venv\lib\site-packages (from click>=8.0.0->black) (0.4.6)
Installing collected packages: pytokens, platformdirs, pathspec, mypy-extensions, click, black
Successfully installed black-26.5.1 click-8.4.1 mypy-extensions-1.1.0 pathspec-1.1.1 platformdirs-4.10.0 pytokens-0.4.1

[notice] A new release of pip available: 22.3 -> 26.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>black my_package/
reformatted C:\Users\User\Desktop\hand_gesture_painter_work\my_package\__init__.py
error: cannot format C:\Users\User\Desktop\hand_gesture_painter_work\my_package\subclass.py: Cannot parse: 77:41
        def draw_canvas(self, frame, lm_list)
                                            ^
ParseError: bad input
reformatted C:\Users\User\Desktop\hand_gesture_painter_work\my_package\core.py
reformatted C:\Users\User\Desktop\hand_gesture_painter_work\my_package\utils.py

Oh no! 💥 💔 💥
3 files reformatted, 1 file failed to reformat.

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>black my_package/
reformatted C:\Users\User\Desktop\hand_gesture_painter_work\my_package\subclass.py

All done! ✨ 🍰 ✨
1 file reformatted, 3 files left unchanged.

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pycodestyle my_package/ --count
my_package\core.py:19:80: E501 line too long (88 > 79 characters)
my_package\core.py:53:80: E501 line too long (80 > 79 characters)
my_package\core.py:77:80: E501 line too long (80 > 79 characters)
my_package\subclass.py:110:80: E501 line too long (83 > 79 characters)
4

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>black my_package/ --line-length 79
reformatted C:\Users\User\Desktop\hand_gesture_painter_work\my_package\core.py

All done! ✨ 🍰 ✨
1 file reformatted, 3 files left unchanged.

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pycodestyle my_package/ --count
my_package\core.py:56:80: E501 line too long (80 > 79 characters)
my_package\core.py:80:80: E501 line too long (80 > 79 characters)
my_package\subclass.py:110:80: E501 line too long (83 > 79 characters)
3

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pycodestyle my_package/ --count
my_package\core.py:55:42: W291 trailing whitespace
my_package\core.py:56:57: W291 trailing whitespace
2

(.venv) C:\Users\User\Desktop\hand_gesture_painter_work>pycodestyle my_package/ --count

![pycodestyle 실행 결과1](pycodestyle_result.png)
![pycodestyle 실행 결과2](pycodestyle_result1.png)
![pycodestyle 실행 결과3](pycodestyle_result2.png)
