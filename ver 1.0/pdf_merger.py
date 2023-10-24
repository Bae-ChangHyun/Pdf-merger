import os
import sys
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import developer

class PDFMerger:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger(Ver 1.0)")
        self.root.geometry("600x500")

        self.pdf_files = []
        self.pdf_labels = []
        self.pdf_images = []
        self.flag = 0

        self.create_menu()
        self.create_widgets()

    def resource_path(relative_path):
        try:
            # PyInstaller에 의해 임시폴더에서 실행될 경우 임시폴더로 접근하는 함수
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_menu(self):
        self.menu = tk.Menu(self.root)
        self.menu.add_command(label="개발자 정보", command=lambda: developer.developer_info(self.root))
        self.root.config(menu=self.menu)


    def create_widgets(self):
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self.root, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.bind("<Configure>", self.resize_canvas)

        merge_button = tk.Button(
            self.canvas,
            text="PDF파일을 병합하기",
            command=self.merge_pdfs,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5,
        )
        merge_button.pack(side="bottom", padx=10, pady=10)

        self.select_button = tk.Button(
            self.canvas,
            text="PDF파일을 선택하기",
            command=self.select_pdfs,
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            padx=10,
            pady=5,
        )
        self.select_button.pack(side="bottom", padx=10, pady=10)

    def restart(self):
        self.canvas.destroy()
        self.scrollbar.destroy()
        self.create_widgets()

    def clear_files(self):
        self.pdf_files = []
        self.flag=0
        self.restart()

    def remove_file(self, image_idx):
        self.pdf_images.pop(image_idx)
        self.pdf_files.pop(image_idx)
        self.pdf_labels.pop(image_idx)
        self.restart()
        self.show_pdf_files()

    def select_del_pdf(self, event, image_idx):
        if(image_idx==self.img_idx):
            self.restart()
            self.show_pdf_files()
            return
        else:
            self.restart()
            self.show_pdf_files()
            self.img_idx=image_idx
            selected_label = self.pdf_labels[image_idx]
            selected_label.config(bg="#2196F3", fg="white")

            delete_button = tk.Button(
                self.canvas,
                text="Delete",
                command=lambda: self.remove_file(image_idx),
                font=("Arial", 10),
                bg="#F44336",
                fg="white",
                padx=10,
                pady=5
            )
            delete_button.pack(side="right", padx=10, pady=5)

            up_button = tk.Button(
                self.canvas,
                text="Up",
                command=lambda: self.move_up(image_idx),
                font=("Arial", 10),
                bg="#F44336",
                fg="white",
                padx=10,
                pady=5
            )
            up_button.pack(side="right", padx=10, pady=5)

            down_button = tk.Button(
                self.canvas,
                text="Down",
                command=lambda: self.move_down(image_idx),
                font=("Arial", 10),
                bg="#F44336",
                fg="white",
                padx=10,
                pady=5
            )
            down_button.pack(side="right", padx=10, pady=5)

    def move_up(self, index):
        if index > 0:
            # Move the item at the current index up by one
            self.pdf_files.insert(index - 1, self.pdf_files.pop(index))
            # Update the UI to reflect the new order
            self.restart()
            self.show_pdf_files()
        else:
            messagebox.showwarning("현재 파일이 가장 위에 있습니다.")

    def move_down(self, index):
        if index < len(self.pdf_files) - 1:
            # Move the item at the current index down by one
            self.pdf_files.insert(index + 1, self.pdf_files.pop(index))
            # Update the UI to reflect the new order
            self.restart()
            self.show_pdf_files()
        else:
            messagebox.showwarning("현재 파일이 가장 아래에 있습니다.")

    def select_pdfs(self):
        if(self.flag==1):
            exist_pdf_files=self.pdf_files
            pdf_files = filedialog.askopenfilenames(
                initialdir=".",
                title="Select PDF files",
                filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")),
            )
            for pdf_file in pdf_files:
                exist_pdf_files.append(pdf_file)
                print(exist_pdf_files)
            self.pdf_files = list(exist_pdf_files)
            self.restart()
        else:

            pdf_files = filedialog.askopenfilenames(
                initialdir=".",
                title="Select PDF files",
                filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")),
            )
            if len(pdf_files) > 10:
                tk.messagebox.showwarning("Warning", "최대 10개까지선택 가능합니다.")
                return
            self.pdf_files = list(pdf_files)
        if(len(self.pdf_files)>0):
            self.show_pdf_files()

    def show_pdf_files(self):
        self.flag = 1
        self.canvas.delete("all")
        self.pdf_labels = []
        self.pdf_images = []
        self.img_idx=9999

        self.select_button.destroy()

        def resource_path(relative_path):
            try:
                # PyInstaller에 의해 임시폴더에서 실행될 경우 임시폴더로 접근하는 함수
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        for i, pdf_file in enumerate(self.pdf_files):
            # Create a label with the filename and icon
            png_path=resource_path("img\pdf_icon.png")
            pdf_image = Image.open(png_path).resize((32, 32), Image.Resampling.LANCZOS)

            self.pdf_images.append(ImageTk.PhotoImage(pdf_image))

            label = tk.Label(
                self.canvas,
                text=os.path.basename(pdf_file),
                image=self.pdf_images[-1],
                compound="left",
                font=("Arial", 10),
            )
            label.bind("<Button-1>", lambda event, image_idx=i: self.select_del_pdf(event, image_idx))
            label.pack(side="top", fill="x", padx=10, pady=5)
            self.pdf_labels.append(label)
        # Add button to allow users to add more pdf files
        add_button = tk.Button(
            self.canvas,
            text="Add Files",
            command=self.select_pdfs,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white",
            padx=10,
            pady=5
        )
        add_button.pack(side="bottom", padx=10, pady=5)

        # Add button to clear the pdf list
        clear_button = tk.Button(
            self.canvas,
            text="Clear",
            command=self.clear_files,
            font=("Arial", 10),
            bg="#F44336",
            fg="white",
            padx=10,
            pady=5
        )
        clear_button.pack(side="bottom", padx=10, pady=5)

    def merge_pdfs(self):
        if len(self.pdf_files) < 2:
            QtWidgets.QMessageBox.warning(self, "Warning", "파일을 최소 2개 이상 선택하세요.")
            return

        pdf_writer = QtGui.QPdfWriter()
        pdf_writer.setOutputFileName(
            QtWidgets.QFileDialog.getSaveFileName(self, "PDF파일 병합하기", ".", "PDF files (*.pdf)")[0])
        pdf_writer.setPageSize(QtCore.QSizeF(595, 842))  # A4 size

        painter = QtGui.QPainter(pdf_writer)
        font = QtGui.QFont("Arial", 10)
        painter.setFont(font)

        for pdf_file in self.pdf_files:
            pdf_reader = QtGui.QPdfDocument(pdf_file)
            for i in range(pdf_reader.pageCount()):
                pdf_reader_page = pdf_reader.page(i)
                painter.drawImage(0, 0, pdf_reader_page.renderToImage())
                if i != pdf_reader.pageCount() - 1:
                    pdf_writer.newPage()

        painter.end()

        QtWidgets.QMessageBox.information(self, "Success", "PDF 병합이 완료되었습니다.")
        self.restart()

    def resize_canvas(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    try:
        os.chdir(sys._MEIPASS)
    except:
        os.chdir(os.getcwd())
    root = tk.Tk()
    app = PDFMerger(root)
    root.mainloop()