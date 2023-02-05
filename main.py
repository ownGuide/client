import os
import sys
from threading import Thread

from dirsync import sync
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QWidget)

from dog import monitor_folders
from yadisk import connect_disk


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Клиент Яндекс Диска")
        self.resize(500, 120)

        layout = QGridLayout()

        label_name = QLabel('<font size="4">Логин Яндекс</font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText(
            "Введите логин с окончанием @yandex.ru"
        )
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4">Пароль</font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_password.setPlaceholderText("Введите пароль приложения")

        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)
        label_url = QLabel(
            '<a href="https://id.yandex.ru/profile/generate-apppassword">получить пароль приложения</a>'
        )
        label_url.setOpenExternalLinks(True)
        layout.addWidget(label_url, 2, 1)

        label_folder = QLabel('<font size="4">Локальный каталог</font>')
        self.lineEdit_folder = QLineEdit()
        self.lineEdit_folder.setPlaceholderText(
            "Введите полный путь к каталогу"
        )
        layout.addWidget(label_folder, 3, 0)
        layout.addWidget(self.lineEdit_folder, 3, 1)

        button_login = QPushButton("Подключить")
        button_login.clicked.connect(self.start)
        layout.addWidget(button_login, 4, 0, 1, 2)

        layout.setRowMinimumHeight(2, 30)

        self.setLayout(layout)

    def show_message(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()

    def is_correct_path(self, path):
        return os.path.isdir(path) and not os.listdir(path)

    def start(self):
        text = "Операция не выполнена:\n"
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        local_path = self.lineEdit_folder.text()
        
        if not all([username, password, local_path]):
            self.show_message(text + "не все поля заполнены!")
            return
        
        if not self.is_correct_path(local_path):
            self.show_message("Указанный каталог не существует \nили не является пустым!")
            return

        try:
            code, description = connect_disk(
                self.lineEdit_username.text(), self.lineEdit_password.text()
            )    
            if not code:
                self.show_message(
                    f"Яндекс Диск подключен как {description}.\nНажмите OK для начала\nкопирования всех файлов в папку\n{local_path}"
                    )
    
                yadisk_path = f"{description}\\"
                sync(yadisk_path, local_path, "sync")
    
                sync_thread = Thread(target=monitor_folders, args=(yadisk_path, local_path))
                sync_thread.start()
            else:
                self.show_message(
                    f"Проблема с Яндекс Диском:\n{description}"
                )
        except Exception as e:
            self.show_message(f"Ошибка программы: {e}")
     


if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()

    sys.exit(app.exec())
