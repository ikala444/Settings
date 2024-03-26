# Файловая структура:
api.py - API приема и отправки детекции номера, а также текста с него
apitest.py - покрытие unittest для функций из файла api.py
data.yaml - конфигурационный файл с настройками для модели
Report.html - обоснование выбранного алгоритма
Report.ipynb - отчет о проделанной работе
train.ipynb - подгтовка данных для модели, а также обучение модели
Readme.md - документация

## Папки:
data - не разбитые данные
dataset - подготовленный датасет для модели
runs - запуски модели с графиками, весами и т.п

### Работа функции detect_car_number из api.py:
1. Подается путь до изображения
2. После подачи идет команда predict, детектирую bouding box для авто-номера на изображение
3. Если координаты bouding box-a существует, то его координаты сохраняются
4. Изображение обрезается
5. Улучшается видимость букв и цифр на номере, чтобы улучшить распознование текста
6. Воспользуемся библиотекой pytesseract с предобученной моделью под NLP и функцией оттуда: image_to_string, чтобы найти текст на картинке

#### Работа функции send_car_number из api.py
Данная функция активирует функцию detect_car_number, передавая туда путь до нашего изображения, а после возвращает ответ, отдавая его в наш интерфейс: interface.py
