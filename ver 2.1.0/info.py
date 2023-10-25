"""MIT 라이선스 Copyright (c) <2023> <Bae_chang_hyun>
이 소프트웨어의 복제본과 관련된 문서화 파일(“소프트웨어”)을 획득하는 사람은 누구라도 소프
트웨어를 별다른 제한 없이 무상으로 사용할 수 있는 권한을 부여 받는다. 여기에는 소프트웨어
의 복제본을 무제한으로 사용, 복제, 수정, 병합, 공표, 배포, 서브라이선스 설정 및 판매할 수 있
는 권리와 이상의 행위를 소프트웨어를 제공받은 다른 수취인들에게 허용할 수 있는 권리가 포함
되며, 다음과 같은 조건을 충족시키는 것을 전제로 한다.
위와 같은 저작권 안내 문구와 본 허용 문구가 소프트웨어의 모든 복제본 및 중요 부분에 포함되
어야 한다.
이 소프트웨어는 상품성, 특정 목적 적합성, 그리고 비침해에 대한 보증을 포함한 어떠한 형태의
보증도 명시적이나 묵시적으로 설정되지 않은 “있는 그대로의” 상태로 제공된다.
소프트웨어를 개발한 프로그래머나 저작권자는 어떠한 경우에도 소프트웨어나 소프트웨어의 사용
등의 행위와 관련하여 일어나는 어떤 요구사항이나 손해 및 기타 책임에 대해 계약상, 불법행위
또는 기타 이유로 인한 책임을 지지 않는다."""

import sys
import os
import subprocess
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QMessageBox

def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

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
            ("License", self.open_VER),
        ]

        for label, action, *args in buttons_info:
            button = QPushButton(label, self)
            button.clicked.connect(action)
            layout.addWidget(button)

    def open_github(self):
        QDesktopServices.openUrl(QUrl('https://github.com/Bae-ChangHyun'))

    def open_VER(self):
        path=resource_path("License.txt")
        subprocess.Popen(['notepad', path], shell=True)

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
