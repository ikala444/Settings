# Импортируем библиотеку для unittest-oв
import unittest
# Из нашего api.py импортируем функции
from api import detect_car_number, send_car_number

# Создаем класс унаследованный от класса встроенного в unittest
class TestCarNumberDetection(unittest.TestCase):
    # Создаем функцию для тестирования функции detect_car_number
    def test_detect_car_number(self):
        # Сохраняем в переменную путь проверяемого изображения
        image_path = r'D:\NumbersProject\Модуль Б\dataset\images\test\1_11_2014_12_13_41_965.bmp'
        # Сохраняем в переменную результат работы функции
        result = detect_car_number(image_path)
        # Проверяем результат полученный и ожидаемый
        self.assertIsInstance(result, str)

# Проверяем условие, что если наша программа основная, то мы выполняем код
if __name__ == '__main__':
    unittest.main()
