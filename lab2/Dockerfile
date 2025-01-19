# Используем официальный PyTorch CPU образ с Python 3.10
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-devel

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    pkg-config \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /workspace

# Копируем файл с зависимостями Python в контейнер
COPY requirements.txt /tmp/

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Устанавливаем зависимости YOLOv5
RUN pip install -r https://raw.githubusercontent.com/ultralytics/yolov5/master/requirements.txt

# Копируем скрипты в контейнер
COPY scripts/ /workspace/scripts/

# Создаем директории для изображений (если еще не созданы)
RUN mkdir -p /workspace/images/input /workspace/images/output

# По умолчанию запускаем скрипт обработки изображений
CMD ["python3", "/workspace/scripts/yolo_image.py"]
