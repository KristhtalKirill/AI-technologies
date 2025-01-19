from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import torch
import cv2
import numpy as np
import base64

app = FastAPI(title="Image Processing Server")

# Загрузка модели YOLOv5
print("Загрузка модели YOLOv5...")
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True,trust_repo=True)
model.eval()
print("Модель YOLOv5 загружена.")


@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    try:
        # Чтение файла
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return JSONResponse(status_code=400, content={"message": "Invalid image file."})

        # Обработка изображения моделью
        results = model(img)

        # Получение результатов
        results_json = results.pandas().xyxy[0].to_json(orient="records")

        # Рендеринг результатов на изображении
        processed_img = np.squeeze(results.render())

        # Кодирование обработанного изображения в base64
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "detections": results_json,
            "image": img_base64
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
