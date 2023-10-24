import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDialog,QMessageBox

class DeveloperInfo(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setGeometry(100, 100, 200, 200)
        self.setWindowTitle('INFO')

        self.initUI()

    def initUI(self):
        # 윈도우 설정
        # 레이아웃 설정
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 이름 출력
        name_layout = QVBoxLayout()
        layout.addLayout(name_layout)
        name_button = QPushButton("배창현", self)
        name_button.clicked.connect(self.show_personal_info)
        name_layout.addWidget(name_button)

        # 깃허브 출력
        github_layout = QVBoxLayout()
        layout.addLayout(github_layout)
        github_button = QPushButton("Github", self)
        github_button.clicked.connect(self.open_github)
        github_layout.addWidget(github_button)

        # 인스타그램 출력
        instagram_layout = QVBoxLayout()
        layout.addLayout(instagram_layout)
        instagram_button = QPushButton("Instagram", self)
        instagram_button.clicked.connect(self.open_instagram)
        instagram_layout.addWidget(instagram_button)

        # 이메일 출력
        email_layout = QVBoxLayout()
        layout.addLayout(email_layout)
        email_button = QPushButton("E-mail", self)
        email_button.clicked.connect(self.open_email_client)
        email_layout.addWidget(email_button)

        ver_layout = QHBoxLayout()
        layout.addLayout(ver_layout)
        ver_button = QPushButton("Ver 1.1", self)
        ver_button.clicked.connect(self.open_VER)
        ver_layout.addWidget(ver_button)

        self.show()

    def open_github(self):
        url = QUrl('https://github.com/Bae-ChangHyun/home')
        QDesktopServices.openUrl(url)

    def open_VER(self):
        QMessageBox.warning(self,"VERSION","Last update 23.05.03")

    def open_instagram(self):
        url = QUrl("https://www.instagram.com/raeps_dlog_/")
        QDesktopServices.openUrl(url)

    def open_university(self):
        url = QUrl("http://www.sejong.ac.kr/")
        QDesktopServices.openUrl(url)

    def open_lab(self):
        url = QUrl("https://sites.google.com/view/wschoi-sejong/home")
        QDesktopServices.openUrl(url)

    def open_email_client(self):
        url = QUrl('mailto:matthew624@naver.com')
        QDesktopServices.openUrl(url)

    def call_phone(self):
        phone_number='010-4691-4204'
        QDesktopServices.openUrl(QUrl("tel:{}".format(phone_number)))

    def show_personal_info(self):
        # 개인 정보 출력
        personal_info = QDialog(self)
        personal_info.setGeometry(100, 100, 150, 150)
        personal_info.setWindowTitle('More')

        personal_layout = QVBoxLayout()
        personal_info.setLayout(personal_layout)

        # 나이 출력
        age_layout = QHBoxLayout()
        personal_layout.addLayout(age_layout)
        age_button = QPushButton("나이:24", self)
        personal_layout.addWidget(age_button)

        # 전화번호 출력
        phone_layout = QHBoxLayout()
        personal_layout.addLayout(phone_layout)
        phone_button = QPushButton("Phone", self)
        phone_button.clicked.connect(self.call_phone)
        personal_layout.addWidget(phone_button)

        school_layout = QHBoxLayout()
        personal_layout.addLayout(school_layout)
        school_button = QPushButton("University", self)
        school_button.clicked.connect(self.open_university)
        personal_layout.addWidget(school_button)

        laboratory_layout = QHBoxLayout()
        personal_layout.addLayout(laboratory_layout)
        laboratory_button = QPushButton("Laboratory", self)
        laboratory_button.clicked.connect(self.open_lab)
        personal_layout.addWidget(laboratory_button)

        personal_info.exec_()

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = DeveloperInfo()
#    sys.exit(app.exec_())

