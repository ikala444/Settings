# Импортируем библиотеку opencv для python
import cv2
# Импортируем библиотеку easyocr для использования преобученной модели OCR
import easyocr
# Из бибилиотеку ultralytics импортируем модуль YOLO для использования модели обучения YOLO
from ultralytics import YOLO
# Импортируем библиотеку os для сохранения корректного пути картинки результата
import os


# Загружаем лучшие веса, которые были получены при обучение в переменную model
model = YOLO(r'D:\NumbersProject\Модуль Б\runs\detect\yolo45\weights\best.pt')

# Создаем функцию получения фотографии и дальнейшей детекции номера и определения текста на номере
def detect_photo(image_path):
    # Загружаем в переменную фото по переданному пути
    image = cv2.imread(image_path)
    # Даем модели предсказать разметочный квадрат (bounding box) для загруженной картинки
    prediction = model.predict(image, save=True)
    # Проверяем в условии, если на картинки обнаружен номер, то продолжаем, если нет, то возвращается текст, что номер не обнаружен и картинку
    if len(prediction[0].boxes.xyxy) > 0:
        # Достаем координаты bounding box-a
        x_min, y_min, x_max, y_max = prediction[0].boxes.xyxy[0]
        # Преобразуем координаты к целочиленному типу
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
        # Обрезаем изображение по полученному bouding box-y (координатам)
        cropped_image = image[y_min:y_max, x_min:x_max]
        # Увеличиваем размер нашего изображение
        resized_image = cv2.resize(cropped_image, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Применяем к изображению фильтр Гауса, чтобы улучшить качество изображения
        smoothed_image = cv2.GaussianBlur(resized_image, (5, 5), 0)
        # Изменяем контраст и яркость изображения
        adjusted_image = cv2.convertScaleAbs(smoothed_image, alpha=1.5, beta=0)
        # Создаем экземпляр объекта reader с предзагруженной моделью под английский язык, для дальнейшего распознавания номера
        reader = easyocr.Reader(['en'])
        # Распознаем номер на обрезанной картинке с помощью ранее созданного экземляра объекта reader
        car_number = reader.readtext(
            image=adjusted_image,
            allowlist='ABCEHKMOPTXY0123456789', # Даем список символов которые должна стремится распознать модель исключая все остальные символы
            paragraph=True) # Выводим результаты детекции в удобочитаемом виде
        # Задаем условие: если длина полученного текста меньше 7 или больше 10, то вероятнее всего были ошибки в детекции и необходимо загрузить более качественную фотографию
        try:
            if len(car_number[0][1]) < 3 or len(car_number[0][1]) > 12:
                # Возвращаем распознанный номер в виде текста и/или фотографию с предсказанным разметочным квадратом (bounding box-ом)
                return [f'При определение номера произошла ошибка, попробуйте загрузить более понятную фотографию.\nНомер авто: {car_number[0][1]}', os.path.join(prediction[0].save_dir, prediction[0].path)]
            else:
                return [f'Вероятнее всего номер изображенный на картинке: {car_number[0][1]}', os.path.join(prediction[0].save_dir, prediction[0].path)]
        except:
            return ["При определение номера произошла ошибка, попробуйте загрузить более понятную фотографию.", os.path.join(prediction[0].save_dir, prediction[0].path)]
    else:
        return ['На картинке номер не был обнаружен.', os.path.join(prediction[0].save_dir, prediction[0].path)]

# Создаем функцию для отправки данных из функции detect_car_number в интерфейс
def send_photo(image_path):
    # Возвращаем полученные данные
    return detect_photo(image_path)
