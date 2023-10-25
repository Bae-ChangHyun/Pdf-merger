import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QDialog, QMessageBox

class DeveloperInfo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('INFO')
        self.setGeometry(100, 100, 200, 200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        buttons_info = [
            ("배창현", self.show_personal_info),
            ("Github", self.open_github, 'https://github.com/Bae-ChangHyun'),
            ("Instagram", self.open_instagram, 'https://www.instagram.com/raeps_dlog_/'),
            ("E-mail", self.open_email_client, 'mailto:matthew624@naver.com'),
            ("Ver 2.0.0", self.open_VER),
        ]

        for label, action, *args in buttons_info:
            button = QPushButton(label, self)
            button.clicked.connect(action)
            layout.addWidget(button)

    def open_github(self):
        QDesktopServices.openUrl(QUrl('https://github.com/Bae-ChangHyun'))

    def open_VER(self):
        QMessageBox.warning(self, "VERSION", "Last update 23.05.23")

    def open_instagram(self):
        QDesktopServices.openUrl(QUrl("https://www.instagram.com/raeps_dlog_/"))

    def open_university(self):
        QDesktopServices.openUrl(QUrl("http://www.sejong.ac.kr/"))

    def open_email_client(self):
        QDesktopServices.openUrl(QUrl('mailto:matthew624@naver.com'))

    def show_personal_info(self):
        personal_info = QDialog(self)
        personal_info.setGeometry(100, 100, 150, 150)
        personal_info.setWindowTitle('More')

        personal_layout = QVBoxLayout(personal_info)

        info_items = [
            "나이: 25",
            ("University", self.open_university, "http://www.sejong.ac.kr/")
        ]

        for item in info_items:
            if isinstance(item, str):
                label = QPushButton(item, self)
                personal_layout.addWidget(label)
            elif isinstance(item, tuple) and len(item) == 2:
                label, action = item
                button = QPushButton(label, self)
                button.clicked.connect(action)
                personal_layout.addWidget(button)
            elif isinstance(item, tuple) and len(item) == 3:
                label, action, url = item
                button = QPushButton(label, self)
                button.clicked.connect(action)
                personal_layout.addWidget(button)

        personal_info.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DeveloperInfo()
    ex.show()
    sys.exit(app.exec_())
