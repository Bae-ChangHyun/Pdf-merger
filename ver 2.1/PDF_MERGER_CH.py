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

import os
import sys
import fitz
import info_2
from PyQt5.QtWidgets import QFileDialog, QMessageBox,QLabel, QHBoxLayout, QWidget, QVBoxLayout,QScrollArea,QAction,QPushButton,QDialog
from PyQt5.QtGui import QPixmap,QFont,QImage,QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyPDF4 import PdfFileReader,PdfFileMerger

# 파일 상대경로-> 절대경로
def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

class PDFMerger(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.pdf_files=[]
        self.image_label = HoverLabel(None, self)
        
        self.setWindowTitle('PDF Merger(23.10.24)')
        self.setGeometry(150, 150, 600, 400)
        
        icon = QIcon(resource_path('pdf_filetype_icon_177525.ico'))
        self.setWindowIcon(icon)
    
        self.setup_ui()
        self.init_menu_bar()
        
    def setup_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.canvas = QScrollArea()
        self.inner_widget = QWidget(self.canvas)
        self.main_layout.addWidget(self.canvas)

        self.inner_layout = QVBoxLayout(self.inner_widget)

        self.merge_button = self.create_button("Merge", self.show_current_order, "background-color: #4CAF50")

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.merge_button, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.setAcceptDrops(True)
        self.main_layout.addLayout(button_layout)
        
        label = QLabel('이 화면에 파일을 추가해주세요', self.central_widget)
        label.setAlignment(Qt.AlignCenter)  # 텍스트를 중앙 정렬
        self.main_layout.addWidget(label)

    def init_menu_bar(self):
        menubar = self.menuBar()
        # "File" 메뉴
        file_menu = menubar.addMenu("File")
        # "Add Files" 액션 추가
        add_files_action = QAction("Add Files", self)
        add_files_action.triggered.connect(self.select_pdfs)
        file_menu.addAction(add_files_action)
        # "Clear Files" 액션 추가
        clear_files_action = QAction("Clear Files", self)
        clear_files_action.triggered.connect(self.clear_files)
        file_menu.addAction(clear_files_action)
        # "Info" 메뉴
        Info_menu = menubar.addMenu("Info")
        run_info_action = QAction("Run Info", self)
        run_info_action.triggered.connect(lambda: info_2.DeveloperInfo().exec_())  # info.py의 함수 실행
        Info_menu.addAction(run_info_action)
        
        
    def create_button(self, text, click_handler, style):
        button = QtWidgets.QPushButton(text, self)
        button.setFont(QtGui.QFont("Arial", 10))
        button.setStyleSheet(f"{style}")
        button.clicked.connect(click_handler)
        button.setFixedSize(100, 35)
        return button
    
    def clear_files(self):
        if(self.pdf_files==[]):
            QMessageBox.warning(self,"Warning","현재 추가된 파일이 없습니다.")
        else:
            self.pdf_files = []
            self.setup_ui()

    def remove_file(self, image_idx):
        self.pdf_files.pop(image_idx)
        if(self.pdf_files!=[]):self.show_pdf_files()
        else:self.setup_ui()
  
    def move_up(self, index):
        if index > 0:
            self.pdf_files.insert(index - 1, self.pdf_files.pop(index))
            self.show_pdf_files()
        else:
            QMessageBox.warning(self,"Warning","현재 파일이 가장 위에 있습니다.")

    def move_down(self, index):
        if index < len(self.pdf_files) - 1:
            self.pdf_files.insert(index + 1, self.pdf_files.pop(index))
            self.show_pdf_files()
        else:
            QMessageBox.warning(self, "Warning", "현재 파일이 가장 아래에 있습니다.")

    def select_pdfs(self):
        existing_pdf_files = self.pdf_files
        pdf_files = QFileDialog.getOpenFileNames(self,"Select PDF files",".","PDF files (*.pdf);;All files (*.*)")[0]
        existing_pdf_files.extend(pdf_files)
        self.pdf_files = list(existing_pdf_files)
        if len(self.pdf_files) > 0:self.show_pdf_files()

    def create_image_widget(self, idx, pdf_file):
        img_size = (150, 80)
        pdf_document = fitz.open(pdf_file)
        first_page = pdf_document[0]
        image = first_page.get_pixmap()
        q_image = QImage(image.samples, image.width, image.height, image.stride, QImage.Format_RGB888)
        pixmap = QPixmap(q_image).scaled(*img_size)

        widget = QWidget(self.canvas)
        widget.pdf_file = pdf_file  # 파일 정보를 위젯에 연결
        widget.idx = idx  # 인덱스 정보를 위젯에 연결

        hbox = QHBoxLayout(widget)
        hbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        
        sub_hbox = QHBoxLayout()
        self.image_label = HoverLabel(widget, self)
        self.image_label.setPixmap(pixmap)
        sub_hbox.addWidget(self.image_label)

        hbox.addLayout(sub_hbox)

        delete_button = self.create_button("Delete", lambda _, idx=idx: self.remove_file(idx), "background-color: #F44336; color: white;")
        hbox.addWidget(delete_button)

        up_button = self.create_button("Up", lambda _, idx=idx: self.move_up(idx), "background-color: gray; color: white;")
        hbox.addWidget(up_button)

        down_button = self.create_button("Down", lambda _, idx=idx: self.move_down(idx), "background-color: gray; color: white;")
        hbox.addWidget(down_button)

        return widget
        
    def show_pdf_files(self):
        self.canvas.deleteLater()
        self.canvas = QScrollArea(self)
        self.canvas.setWidgetResizable(True)
        self.canvas.setFrameShape(QtWidgets.QFrame.NoFrame)

        if self.inner_widget.layout():
            sip.delete(self.inner_widget.layout())

        self.inner_widget = QWidget(self)
        self.inner_layout = QVBoxLayout(self.inner_widget)
        self.inner_widget.setLayout(self.inner_layout)

        for i, pdf_file in enumerate(self.pdf_files):
            widget = self.create_image_widget(i, pdf_file)
            self.inner_layout.addWidget(widget)  # QVBoxLayout을 사용하여 위젯을 아래로 추가

        self.inner_layout.addWidget(self.merge_button, alignment=Qt.AlignCenter | Qt.AlignBottom)

        self.canvas.setWidget(self.inner_widget)
        self.setCentralWidget(self.canvas)
        
    def show_current_order(self):
        order_dialog = QtWidgets.QDialog(self)
        order_dialog.setWindowTitle("Current Order")
        order_layout = QVBoxLayout(order_dialog)

        # 현재 순서를 나타내는 위젯(예: 리스트 위젯)을 생성하고 order_layout에 추가합니다.
        current_order_widget = QtWidgets.QListWidget(order_dialog)
        for pdf_file in self.pdf_files:
            current_order_widget.addItem(pdf_file)
        order_layout.addWidget(current_order_widget)

        # "예" 버튼을 추가하고 클릭 시 병합 작업을 시작합니다.
        merge_button = QPushButton("예", order_dialog)
        merge_button.clicked.connect(self.merge_pdfs)
        order_layout.addWidget(merge_button)

        # "아니오" 버튼을 추가하고 클릭 시 창을 닫고 병합 작업을 취소합니다.
        cancel_button = QPushButton("아니오", order_dialog)
        cancel_button.clicked.connect(order_dialog.reject)
        order_layout.addWidget(cancel_button)

        result = order_dialog.exec_()

    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            QtWidgets.QMessageBox.warning(self, "Warning", "파일을 최소 2개 이상 선택하세요.")
            return
    
        pdf_merger = PdfFileMerger()

        for pdf_file in self.pdf_files:
            pdf_reader = PdfFileReader(open(pdf_file, 'rb'))
            pdf_merger.append(pdf_reader)

        output_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "PDF파일 병합하기", ".", "PDF files (*.pdf)")
        
        if output_filename:
            pdf_merger.write(output_filename)
            QtWidgets.QMessageBox.information(self, "Success", "PDF 병합이 완료되었습니다.")
            self.clear_files()
        order_dialog = self.sender().parent()
        order_dialog.accept()
        
            
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        pdf_files = [file for file in files if file.lower().endswith('.pdf')]

        if pdf_files:
            existing_pdf_files = self.pdf_files
            existing_pdf_files.extend(pdf_files)
            self.pdf_files = list(existing_pdf_files)
            self.show_pdf_files()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "PDF 파일만 추가할 수 있습니다.")

    # PDF 파일을 열거나 실행하는 함수
    def open_pdf_file(self, pdf_file):
        os.startfile(pdf_file)  # Windows에서 파일 열기
    
        
class HoverLabel(QLabel):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.hovered = False
        self.main_window = main_window
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.hovered = True
        self.setStyleSheet("border: 1px solid black;")
        pdf_file = self.parent().pdf_file
        pdf_reader = PdfFileReader(pdf_file, strict=False)
        num_pages = pdf_reader.getNumPages()
        tooltip_text = f"{os.path.basename(pdf_file)}...전체 {num_pages}p"
        self.setToolTip(tooltip_text)  # 툴팁에 페이지 정보 표시

    def leaveEvent(self, event):
        self.hovered = False
        self.setStyleSheet("")  # Remove border

    def mousePressEvent(self, event):
        pdf_file = self.parent().pdf_file  # 위젯에서 파일 정보 가져오기
        self.main_window.open_pdf_file(pdf_file)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    merger = PDFMerger()
    merger.show()
    sys.exit(app.exec_())