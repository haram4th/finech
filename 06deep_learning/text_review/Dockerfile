# TensorFlow 공식 CPU 이미지 (Jupyter 포함)
FROM tensorflow/tensorflow:2.17.0

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# JAVA 환경변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
COPY text_review_requirements.txt ./
RUN pip install --no-cache-dir -r text_review_requirements.txt

# 앱 및 모델 복사
COPY . .

# 포트 개방
EXPOSE 7860

# 실행
CMD ["python", "text_review.py"]
