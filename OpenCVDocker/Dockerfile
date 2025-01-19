# Используем базовый образ Ubuntu 22.04
FROM ubuntu:22.04

# Установим необходимые зависимости и обновим систему
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

# Установим переменную окружения для Python
ENV PYTHON_VERSION=3.10
ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/dist-packages

# Копируем файл с зависимостями Python в контейнер
COPY requirements.txt /tmp/

# Обновляем pip и устанавливаем Python-зависимости
RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# Скачиваем и собираем OpenCV 4.8.0 с модулями contrib и non-free
RUN mkdir -p /opt/opencv && cd /opt/opencv && \
    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.8.0.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.8.0.zip && \
    unzip opencv.zip && unzip opencv_contrib.zip && \
    rm opencv.zip opencv_contrib.zip && \
    cd opencv-4.8.0 && mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv/opencv_contrib-4.8.0/modules \
          -D OPENCV_ENABLE_NONFREE=ON \
          -D BUILD_EXAMPLES=OFF \
          .. && \
    make -j$(nproc) && make install && ldconfig

# Устанавливаем рабочую директорию
WORKDIR /workspace

# Копируем скрипты в контейнер
COPY scripts/ /workspace/scripts/

# Копируем изображения в контейнер
COPY images/ /workspace/images/

# По умолчанию запускаем bash
CMD ["bash"]
