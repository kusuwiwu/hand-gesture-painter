from setuptools import setup, find_packages

setup(
    name="hand_gesture_painter_work",
    version="1.0.0",
    author="이현우",
    author_email="lhynwu@kku.ac.kr",  # 필요시 수정 가능
    description="MediaPipe 기반 가상 마우스 포인터 및 제스처 인터랙션 프로토타입",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires="==3.11.0", 
    install_requires=[
        "opencv-python == 4.9.0.80",
        "mediapipe == 0.10.14",
        "numpy == 1.26.4",
    ],
    extras_require={
        "test": ["pytest == 8.1.1"],
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
)