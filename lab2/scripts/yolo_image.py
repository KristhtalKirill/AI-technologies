import torch
import numpy as np
import cv2
import os
import time
from ultralytics import YOLO

class ObjectDetection:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("\n\nИспользуемое устройство:", self.device)
        self.model = self.load_model()
        self.classes = self.model.names

    def load_model(self):
        model = YOLO('yolov5s.pt')
        model.to(self.device)
        return model

    def score_image(self, frame):
        """
        Обрабатывает одно изображение с использованием модели YOLOv5.
        :param frame: Изображение в формате numpy.
        :return: Метки, координаты и уверенность обнаруженных объектов.
        """
        results = self.model(frame)
        result = results[0]  # Предполагается, что обрабатывается одно изображение

        # Извлечение классов, координат и уверенности
        labels = result.boxes.cls.cpu().numpy().astype(int)
        cords = result.boxes.xyxy.cpu().numpy()  # Координаты в формате [x1, y1, x2, y2]
        confidences = result.boxes.conf.cpu().numpy()

        return labels, cords, confidences
    def class_to_label(self, x):
        """
        Преобразует числовую метку в строковое название класса.
        :param x: Числовая метка.
        :return: Название класса.
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Рисует bounding boxes и метки на изображении.
        :param results: Результаты модели (метки, координаты и уверенность).
        :param frame: Исходное изображение.
        :return: Изображение с нарисованными bounding boxes.
        """
        labels, cords, confidences = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]

        for i in range(n):
            if confidences[i] >= 0.2:  # Порог уверенности
                x1, y1, x2, y2 = map(int, cords[i])
                confidence = confidences[i]
                label = self.class_to_label(labels[i])
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                text = f"{label} {confidence:.2f}"
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        return frame

    def process_images(self, input_dir, output_dir):
        """
        Обрабатывает все изображения из папки input и сохраняет результаты в папку output.
        :param input_dir: Путь к папке с исходными изображениями.
        :param output_dir: Путь к папке для сохранения обработанных изображений.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

        for image_file in image_files:
            input_path = os.path.join(input_dir, image_file)
            output_path = os.path.join(output_dir, f"output_{image_file}")

            frame = cv2.imread(input_path)
            if frame is None:
                print(f"Не удалось загрузить изображение: {input_path}")
                continue

            start_time = time.perf_counter()
            results = self.score_image(frame)
            frame = self.plot_boxes(results, frame)
            end_time = time.perf_counter()
            fps = 1 / np.round(end_time - start_time, 3)

            cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

            cv2.imwrite(output_path, frame)
            print(f"Обработано и сохранено: {output_path}")

if __name__ == "__main__":
    detection = ObjectDetection()
    input_dir = 'images/input/'
    output_dir = 'images/output/'
    detection.process_images(input_dir, output_dir)
