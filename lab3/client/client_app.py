import sys
import os
import requests
import base64
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PIL import Image
from io import BytesIO


class ClientApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.api_url = "http://91.222.130.250:8000/process-image/"

    def init_ui(self):
        self.setWindowTitle('Image Processing Client')
        self.setGeometry(100, 100, 800, 600)

        # Кнопка загрузки изображения
        self.load_button = QtWidgets.QPushButton('Загрузить изображение', self)
        self.load_button.clicked.connect(self.load_image)

        # Отображение загруженного изображения
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setFixedSize(400, 400)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Отображение обработанного изображения
        self.processed_image_label = QtWidgets.QLabel(self)
        self.processed_image_label.setFixedSize(400, 400)
        self.processed_image_label.setStyleSheet("border: 1px solid black;")
        self.processed_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Расположение элементов
        hbox = QtWidgets.QHBoxLayout()
        vbox_left = QtWidgets.QVBoxLayout()
        vbox_right = QtWidgets.QVBoxLayout()

        vbox_left.addWidget(self.load_button)
        vbox_left.addWidget(self.image_label)

        vbox_right.addWidget(QtWidgets.QLabel('Обработанное изображение:'))
        vbox_right.addWidget(self.processed_image_label)

        hbox.addLayout(vbox_left)
        hbox.addLayout(vbox_right)

        self.setLayout(hbox)

    def load_image(self):
        # Открытие диалогового окна для выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', os.getenv('HOME'),
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            # Загрузка и отображение изображения
            image = Image.open(file_path)
            image.thumbnail((400, 400))
            img_bytes = BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()
            qimg = QtGui.QImage.fromData(img_bytes)
            pixmap = QtGui.QPixmap.fromImage(qimg)
            self.image_label.setPixmap(pixmap)

            # Отправка изображения на сервер
            self.send_image(file_path)

    def send_image(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'image/jpeg')}
                response = requests.post(self.api_url, files=files)

            if response.status_code == 200:
                data = response.json()
                detections = data.get('detections', 'No detections.')
                processed_image_base64 = data.get('image', None)

                if processed_image_base64:
                    # Декодирование обработанного изображения
                    image_data = base64.b64decode(processed_image_base64)
                    image = Image.open(BytesIO(image_data))
                    image.thumbnail((400, 400))
                    img_bytes = BytesIO()
                    image.save(img_bytes, format='JPEG')
                    img_bytes = img_bytes.getvalue()
                    qimg = QtGui.QImage.fromData(img_bytes)
                    pixmap = QtGui.QPixmap.fromImage(qimg)
                    self.processed_image_label.setPixmap(pixmap)

                # Отображение результатов
                QMessageBox.information(self, "Обработка завершена", f"Детекции:\n{detections}")

            else:
                QMessageBox.warning(self, "Ошибка", f"Сервер вернул статус код {response.status_code}: {response.text}")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при отправке изображения: {str(e)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ClientApp()
    window.show()
    sys.exit(app.exec())
