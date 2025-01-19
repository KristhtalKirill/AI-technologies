import cv2
import numpy as np
import os

def gamma_correction(image, gamma=2.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(256)]).astype("uint8")
    return cv2.LUT(image, table)

def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    # Конвертируем одноцветное изображение обратно в BGR
    edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return edges_bgr

def main():
    input_path = 'images/input.jpg'
    output_gamma = 'images/output_gamma.jpg'
    output_edges = 'images/output_edges.jpg'

    # Проверяем, существует ли входное изображение
    if not os.path.exists(input_path):
        print(f"Не удалось найти изображение по пути: {input_path}")
        return

    # Считываем изображение
    image = cv2.imread(input_path)
    if image is None:
        print(f"Не удалось загрузить изображение по пути: {input_path}")
        return

    # Гамма-коррекция
    gamma_corrected = gamma_correction(image, gamma=2.0)
    cv2.imwrite(output_gamma, gamma_corrected)
    print(f"Гамма-коррекция сохранена: {output_gamma}")

    # Выделение контуров
    edges = detect_edges(image)
    cv2.imwrite(output_edges, edges)
    print(f"Контуры сохранены: {output_edges}")

if __name__ == "__main__":
    main()
