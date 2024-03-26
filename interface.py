# Импортиурем бибилиотеку для операция над системой
import sys
# Из PyQt6.QtWidgets импортируем необходимые виджеты
from PyQt6.QtWidgets import QPushButton, QMainWindow, QApplication, QFileDialog, QLabel, QVBoxLayout, QWidget
# Из PyQt6.QtGui импортиурем PixMap для изображения
from PyQt6.QtGui import QPixmap
# Из api.py импортиурем функцию для получения результатов нашего api
from api import send_car_number

# Создаем класс, унаследованный от QMainWindow из PyQt6.QtWidgets
class GetImage(QMainWindow):
    # Создаем элементы, которые будут отображаться в нашем приложение
    def __init__(self):
        super().__init__()
        # Передаем название нашего окна
        self.setWindowTitle('Определение номера')
        # Создаем слой для эелементов
        layout = QVBoxLayout()
        # Создаем виджет
        widget = QWidget()
        # Ставим виджету слой из переменной layout
        widget.setLayout(layout)
        # В перемнную сохраняем элемент QLabel, в котором будет отображаться загруженное фото
        self.picture = QLabel()
        # В переменную сохраняем элемент QLabel, в котором будет отображаться текст с номера авто, а начальное значение элемента задаем сами
        self.label = QLabel('Добвьте изображение, чтобы отобразить номер.')
        # В переменную сохраняем элемент QPushButton, с текстом на кнопке "Добавить файл"
        button = QPushButton("Добавить файл")
        # При нажатие на кнопку подключаем к кнопке функцию clicked_to_use_API
        button.clicked.connect(self.clicked_to_use_API)

        # Добавляем в наш слой все добавленные элементы по порядку
        layout.addWidget(self.picture)
        layout.addWidget(self.label)
        layout.addWidget(button)
        # Ставим отображение перменной widget в центре
        self.setCentralWidget(widget)
    # Создаем функцию, которая будет отправлять фото в наше API
    def clicked_to_use_API(self):
        # Добавляем виджет, чтобы наша кнопка могла работать как добавление файлов
        result = QFileDialog.getOpenFileName(self, 'Выберите файл', '/Users/Server/Desktop/NumbersProject', 'BMP File(*.bmp)')
        # Сохраняем в переменную путь до переданного файла
        image_path = result[0]
        # Сохраняем в переменную PixMap
        pixmap = QPixmap(image_path)
        # Отображаем выбранное фото на экране
        self.picture.setPixmap(pixmap)
        # Проверяем условие, что путь до картинки существует
        if len(image_path) < 1:
            # Если пути нет, то выводим, что картинка не выбрана
            self.label.setText("Изображение не выбрано.")
        else:
            # Сохраняем в переменную работу нашего API, которое возвращает текст номера
            result_text = send_car_number(image_path)
            # Отображаем на экране текст из нашего API
            self.label.setText(result_text)

# Создаем наше приложение, а после запускаем его
app = QApplication(sys.argv)
window = GetImage()
window.show()
app.exec()
