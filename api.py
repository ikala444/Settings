# Импортиурем библиотеку opencv для python
import cv2
# Импортиурем библиотеку pytesseract для использования преобученной модели NLP
import pytesseract
# Из бибилиотеку ultralytics импортируем модуль YOLO для использования модели обучения YOLO
from ultralytics import YOLO

# Передаем путь до tesseract.exe к нашему pytesseract
pytesseract.pytesseract.tesseract_cmd = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
# Загружаем лучшие веса, которые были получены при обучение в переменную model
model = YOLO(r'D:\NumbersProject\Модуль Б\runs\detect\yolo43\weights\best.pt')

# Создаем функцию для детекции номера и определение текста на номере
def detect_car_number(image_path):
    # Загружаем в переменную фото по переданному пути
    image = cv2.imread(image_path)
    # Предиктим bouding box для загруженной картинки
    prediction = model.predict(image)
    # Проверяем условии, если на картинки обнаружен номер, то продолжаем, если нет, то возвращается текст, что номер не обнаружен
    if len(prediction[0].boxes.xyxy) > 0:
        # Достаем координаты bouding box-a
        x_min, y_min, x_max, y_max = prediction[0].boxes.xyxy[0]
        # Преобразуем координаты к целочиленному типу
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
        # Обрезаем изображение по полученному bouding box-y и увеличиваем размер нашего изображение
        resized_image = cv2.resize((image[y_min:y_max, x_min:x_max]), None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        # Применяем к изображению фильтр Гауса, чтобы улучшить качество изображения
        smoothed_image = cv2.GaussianBlur(resized_image, (5, 5), 0)
        # Изменяем контраст и яркость изображения
        adjusted_image = cv2.convertScaleAbs(smoothed_image, alpha=1.5, beta=0)
        # Передаем в переменную конфиг для pytesseract и сохраняем в переменную полученный текст с номера
        car_number = pytesseract.image_to_string(adjusted_image, config=r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCEHKMNOPTXY')
        # Если длина полуенного текста меньше 7 или больше 10, то вероятнее всего были ошибки в детекции, необходимо загрузить более качественную фотографию
        if len(car_number) < 3 or len(car_number) > 12:
            return f'При определение номера произошла ошибка, попробуйте загрузить более понятную фотографию.\nНомер авто: {car_number}'
        else:
            return f'Вроятнее всего номер изображенный на изображение: {car_number}'
    else:
        return 'На картинке номера не обнаружено.'

# Создаем функцию для отправки данных из функции detect_car_number в интерфейс
def send_car_number(image_path):
    # Возвращаем полученные данные
    return detect_car_number(image_path)
