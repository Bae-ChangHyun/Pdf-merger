import os
import sys
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets, sip
from PyPDF4 import PdfFileReader
from PyPDF4 import PdfFileMerger
import test

class PDFMerger(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger(Ver 1.1)")
        self.setGeometry(200, 200, 600, 500)

        self.pdf_files = []
        self.pdf_labels = []
        self.pdf_images = []
        self.flag = 0

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menu = self.menuBar()
        developer_menu = menu.addMenu('Developer')
        developer_info = QtWidgets.QAction('Developer Information', self)
        developer_info.triggered.connect(lambda: test.DeveloperInfo().exec())
        developer_menu.addAction(developer_info)

    def create_widgets(self):
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.scrollbar = QtWidgets.QScrollBar(QtCore.Qt.Vertical)
        main_layout.addWidget(self.scrollbar)

        self.canvas = QtWidgets.QScrollArea()
        self.canvas.setWidgetResizable(True)
        main_layout.addWidget(self.canvas)

        self.inner_widget = QtWidgets.QWidget()
        self.canvas.setWidget(self.inner_widget)
        inner_layout = QtWidgets.QVBoxLayout()
        self.inner_widget.setLayout(inner_layout)

        self.scrollbar.valueChanged.connect(self.canvas.verticalScrollBar().setValue)

        self.canvas.viewport().installEventFilter(self)

        self.select_button = QtWidgets.QPushButton(
            "PDF파일을 선택하기",
            self,
            clicked=self.select_pdfs,
            font=QtGui.QFont("Arial", 12, QtGui.QFont.Bold),
        )
        self.select_button.setStyleSheet('''
                    QPushButton {
                        background-color: red;
                        color: white;
                        padding: 10px;
                        padding-left: 15px;
                        padding-right: 15px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #cc0000;
                    }
                    
        ''')
        main_layout.addWidget(self.select_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        self.merge_button = QtWidgets.QPushButton(
            "PDF파일을 병합하기",
            self,
            clicked=lambda: self.merge_pdfs(),
            font=QtGui.QFont("Arial", 12, QtGui.QFont.Bold),
        )
        self.merge_button.setStyleSheet('''
                            QPushButton {
                                background-color: #4CAF50;
                                color: white;
                                padding: 10px;
                                padding-left: 15px;
                                padding-right: 15px;
                                border-radius: 5px;
                            }
                            QPushButton:hover {
                                background-color: #3e8e41;
                            }
                ''')
        main_layout.addWidget(self.merge_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

    def restart(self):
        #self.canvas.setParent(None)
        sip.delete(self.canvas)
        self.create_widgets()
        return

    def clear_files(self):
        self.pdf_files = []
        self.flag = 0
        self.restart()

    def remove_file(self, image_idx):
        self.pdf_images.pop(image_idx)
        self.pdf_files.pop(image_idx)
        self.pdf_labels.pop(image_idx)
        self.restart()
        self.show_pdf_files()

    def move_up(self, index):
        if index > 0:
            # Move the item at the current index up by one
            self.pdf_files.insert(index - 1, self.pdf_files.pop(index))
            # Update the UI to reflect the new order
            self.restart()
            self.show_pdf_files()
        else:
            QMessageBox.warning(self,"Warning","현재 파일이 가장 위에 있습니다.")

    def move_down(self, index):
        if index < len(self.pdf_files) - 1:
            # Move the item at the current index down by one
            self.pdf_files.insert(index + 1, self.pdf_files.pop(index))
            # Update the UI to reflect the new order
            self.restart()
            self.show_pdf_files()
        else:
            QMessageBox.warning(self, "Warning", "현재 파일이 가장 아래에 있습니다.")

    def select_pdfs(self):
        if self.flag == 1:
            existing_pdf_files = self.pdf_files
            pdf_files = QFileDialog.getOpenFileNames(
                self,
                "Select PDF files",
                ".",
                "PDF files (*.pdf);;All files (*.*)"
            )[0]
            existing_pdf_files.extend(pdf_files)
            self.pdf_files = list(existing_pdf_files)
            self.restart()
        else:
            pdf_files = QFileDialog.getOpenFileNames(
                self,
                "Select PDF files",
                ".",
                "PDF files (*.pdf);;All files (*.*)"
            )[0]
            if len(pdf_files) > 10:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "최대 10개까지 선택 가능합니다."
                )
                return
            self.pdf_files = list(pdf_files)

        if len(self.pdf_files) > 0:
            self.show_pdf_files()

    def show_pdf_files(self):
        self.flag = 1
        self.canvas.deleteLater()
        self.pdf_labels = []
        self.pdf_images = []
        self.img_idx = 9999

        self.select_button.deleteLater()

        self.canvas = QtWidgets.QWidget(self)
        sizes=len(self.pdf_files)*150
        self.canvas.setMinimumSize(sizes,sizes)
        layout = QtWidgets.QVBoxLayout(self.canvas)
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        layout.addWidget(self.scroll_area)
        self.setCentralWidget(self.canvas)
        import fitz

        for i, pdf_file in enumerate(self.pdf_files):
            # Create a widget to hold both the image and the text
            open_pdf = fitz.open(pdf_file)
            pix = open_pdf[0].get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            qimg = QtGui.QImage(pix1.samples, pix1.width, pix1.height, pix1.stride, QtGui.QImage.Format_RGB888)
            # Convert the QImage to a QPixmap
            pixmap = QtGui.QPixmap(qimg).scaled(80,48)
            self.pdf_images.append(pixmap)

            # Create a widget to hold both the image and the text
            widget = QWidget(self.canvas)
            hbox = QHBoxLayout(widget)
            hbox.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            # Add the image to the layout
            image_label = QLabel(widget)
            image_label.setPixmap(pixmap)
            hbox.addWidget(image_label)

            pdf_reader = PdfFileReader(pdf_file)
            num_pages = pdf_reader.getNumPages()

            # Add the text to the layout
            label = QLabel(widget)
            label.setFont(QFont("Arial", 10))
            #label.setWordWrap(True) --> 글이 길어지면 줄바꿈
            print(num_pages)
            texts="  ("+os.path.basename(pdf_file)[:5]+"...전체 "+str(num_pages)+"p )"
            label.setText(texts)
            hbox.addWidget(label)

            delete_button = QtWidgets.QPushButton("Delete", self.canvas)
            delete_button.setFont(QtGui.QFont("Arial", 10))
            delete_button.setStyleSheet(
                "background-color: #F44336; color: white; padding: 5px 10px; margin-right: 10px; margin-bottom: 5px;")
            delete_button.clicked.connect(lambda _, idx=i: self.remove_file(idx))
            hbox.addWidget(delete_button)

            up_button = QtWidgets.QPushButton("Up", self.canvas)
            up_button.setFont(QtGui.QFont("Arial", 10))
            up_button.setStyleSheet(
                "background-color: gray; color: white; padding: 5px 10px; margin-right: 10px; margin-bottom: 5px;")
            up_button.clicked.connect(lambda _, idx=i: self.move_up(idx))
            hbox.addWidget(up_button)

            down_button = QtWidgets.QPushButton("Down", self.canvas)
            down_button.setFont(QtGui.QFont("Arial", 10))
            down_button.setStyleSheet(
                "background-color: gray; color: white; padding: 5px 10px; margin-right: 10px; margin-bottom: 5px;")
            down_button.clicked.connect(lambda _, idx=i: self.move_down(idx))
            hbox.addWidget(down_button)

            # Set the widget's layout and add to the list of label
            widget.setStyleSheet("padding: 10px 20px;")

            self.pdf_labels.append(widget)
            self.canvas.layout().addWidget(widget)

        # Add button to allow users to add more pdf files
        add_button = QtWidgets.QPushButton("Add Files", self.canvas)
        add_button.setFont(QtGui.QFont("Arial", 10))
        add_button.setStyleSheet("background-color: #2196F3; color: white;")
        add_button.clicked.connect(self.select_pdfs)
        add_button.setFixedSize(100, 35)
        layout.addWidget(add_button, alignment=QtCore.Qt.AlignCenter)

        # Add button to clear the pdf list
        clear_button = QtWidgets.QPushButton("Clear Files", self.canvas)
        clear_button.setFont(QtGui.QFont("Arial", 10))
        clear_button.setStyleSheet("background-color: #F44336; color: white;")
        clear_button.clicked.connect(self.clear_files)
        clear_button.setFixedSize(100, 35)
        layout.addWidget(clear_button, alignment=QtCore.Qt.AlignCenter)

        layout.addWidget(self.merge_button, alignment=QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        # self.scroll_area.setWidget(self.canvas)

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
            self.restart()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    merger = PDFMerger()
    merger.show()
    sys.exit(app.exec_())