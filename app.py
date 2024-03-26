# Подключаем библиотеку отвечающую за создание интерфейса приложения
import flet as ft
# Подключаем библиотеку позволяющую получать корректный путь к картинке
import os
# Загружаем из api функцию отправки фото
from api1 import send_photo


# Переменные ширины и высоты окна приложения
window_width = 1265
window_height = 710
# Перемененная отвечающая за то будет ли полноэкранным приложение
fullscreen = False

# Создаем класс представляющий основное окно приложения
class MainPage:
    # Задаем параметры инициализации класса, page = приложение на котором появится это окно
    def __init__(self, page):
        # Объявляем параметр приложения для использования его в дальнейшем
        self.page = page
        # Создаем элемент заголовка приложения
        self.main_title = ft.Text("Определение автомобильного номера", size=40, text_align=ft.TextAlign.CENTER)
        # Создаем элемент картинки который будет хранить результат в виде фото
        self.img = ft.Image(
            border_radius=ft.border_radius.all(10),
            width=850, height=420
                            )
        # Создаем элемент контейнера который будет хранить картинку (предыдущий элемент), вокруг которой будет белая обводка
        self.img_container = ft.Container(
                                    border=ft.border.all(4, ft.colors.WHITE),
                                    border_radius=ft.border_radius.all(10),
                                    width=850, height=420)
        # Создаем элемент текста который будет хранить результат в виде текста
        self.result_text = ft.Text(size=25, text_align=ft.TextAlign.CENTER)
        # Создаем элемент полосы загрузки для отображения процесса загрузки фотографии в api
        self.pb = ft.Container(content=ft.ProgressBar(width=400, color="blue"), opacity=0, animate_opacity=300)
        # Создаем элемент контейнера внутри которого находится кнопка для отправки фотографии в api
        self.load_btn = ft.Container(
                                    ft.ElevatedButton(
                                        text="Выбрать фото",
                                        icon=ft.icons.FILE_UPLOAD,
                                        on_click=self.load_photo
                                    ), animate=ft.animation.Animation(600, ft.AnimationCurve.BOUNCE_OUT)
                                )
        # Создаем основной вид (окно), который хранит в себе все предыдущие элементы
        self.main_view = ft.View(
                route='/',
                controls=[
                    self.main_title,
                    ft.Container(
                        content=ft.Column(
                            [
                                self.img_container,
                                ft.Container(self.result_text),
                                self.pb,
                                self.load_btn
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ), alignment=ft.alignment.center
                    )
                    ],
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        # Создаем элемент захватчика файлов (выбор файла)
        self.file_picker = ft.FilePicker(on_result=self.pick_files_result)
        self.page.overlay.append(self.file_picker)
        # Обновляем приложение для появления вида (окна)
        self.page.update()
        self.prev_path = ''
        self.new_path = ''
        self.clone_image = 0

    # Функция получения фото для интерфейса (по стандартам ООП)
    def pick_files_result(self, e):
        # Задаем условие: если выбор пользователя не пустой то - выполняется следующий код
        if self.file_picker.result!= None and self.file_picker.result.files != None:
            # Появляется полоса загрузки
            self.pb.opacity = 100
            # Блокируется элемент кнопки для избежания загрузки фотографии до окончания появления результата api
            self.load_btn.disabled = True
            # Обновляем страницу для изменения элементов
            self.page.update()
            # Сохранем в переменную результат выполнения функции отправки фотографии в api
            self.result = send_photo(self.file_picker.result.files[0].path)
            self.prev_path = self.result[1]
            if os.path.exists(self.prev_path):
                self.clone_image = self.clone_image+1
                head, tail = os.path.split(self.prev_path)
                os.rename(self.prev_path, f"{head}/image{self.clone_image}.jpg")
                self.new_path = os.path.join(head, f"image{self.clone_image}.jpg")
                self.img.src = self.new_path
            else:
                # Выводим результат работы api в виде фотографии с определенным номером
                self.img.src = self.result[1]
            # Выводим результат работы api в виде текста распознанного номера
            self.result_text.value = self.result[0]
            # Загружаем фотографию в элемент контейнера интерфейса
            self.img_container.content = self.img
            # Убираем полосу загрузки
            self.pb.opacity = 0
            # Разблокируем элемент кнопки
            self.load_btn.disabled = False
            # Обновляем странцу для изменения элементов и появления результата
            self.page.update()

    # Функция выбора фото пользователем
    def load_photo(self, e):
        # Захват фотографии в результате выбора пользователя
        self.file_picker.pick_files(
                file_type = ft.FilePickerFileType.IMAGE, # Выборка происходит исключительно из фотографий (.jpg, .png, .bmp и тд)
                initial_directory = os.getcwd())


# Основная функция запуска приложения и настройка основных параметров окна приложения
def main(page: ft.Page):
    # Задаем название окну приложения
    page.title = "Определение номера"
    # Задаем цветовую тему приложения
    page.theme_mode = "dark"
    # Задаем ширину и высоту окна приложения
    page.window_width = window_width
    page.window_height = window_height
    # Задаем автоматическое появление полосы прокрутки при необходимости
    page.scroll = ft.ScrollMode.AUTO
    # Задаем горизонтальное положения элементов в приложении посередине
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # Задаем переменную отвечающую за полноэкранность приложения
    page.window_full_screen = fullscreen

    # Создаем основное окно приложения
    main_page = MainPage(page=page)


    # Функция обработки видов (окон) приложения
    def views_handler(page):
        return {
            '/':main_page.main_view,
        }

    # Функция изменения вида (окна) приложения
    def route_change(route):
        page.views.clear()
        page.views.append(views_handler(page)[page.route])

    # Привязываем обработчик к виду (окну) приложения
    page.on_route_change = route_change
    # Запускаем основной вид (окно) приложения
    page.go('/')

# Проверяем условие, что если наша программа основная (запускается из основного файла), то мы запускаем приложение
if __name__ == "__main__":
    # Задаем параметры приложения
    ft.app(target=main)
