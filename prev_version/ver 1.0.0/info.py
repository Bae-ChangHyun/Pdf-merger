import os
import sys
import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import messagebox

class developer_info:
    def __init__(self,root):

        self.root = tk.Toplevel(root)
        self.root.title("개발자 정보")
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_width = self.root.winfo_width()
        root_height = root.winfo_height()
        x = root_x + root_width // 2 - self.root.winfo_width() // 2
        y = root_y + root_height // 2 - self.root.winfo_height() // 2
        self.root.geometry("+{}+{}".format(x, y))
        self.developer_infos()

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def operate(self, text):
        if (text == 'To Mail'):
            webbrowser.open('mailto:matthew624@naver.com', new=1)
        if (text == 'Github_Link'):
            webbrowser.open('https://github.com/Bae-ChangHyun', new=1)
        if (text == 'Insta'):
            webbrowser.open('https://www.instagram.com/raeps_dlog_/', new=1)
        if (text == "배창현"):
            messagebox.showinfo("VER 1.0.0", "Last Update 22.08.25")

    def click_item(self, event):
        selectedItem = self.treeview.focus()
        self.getValue = self.treeview.item(selectedItem).get('values')[1]  # 딕셔너리의 값만 가져오기
        self.showed.configure(text=self.getValue, command=partial(self.operate, self.getValue))  # 라벨 내용 바꾸기

    def developer_infos(self):
        self.developer_frame = Frame(self.root)
        self.developer_frame.pack(fill=BOTH, expand=1, padx=10, pady=10)

        self.treeview = ttk.Treeview(self.developer_frame, columns=["one", 'two'], displaycolumns=["one", 'two'],
                                     height=6)
        self.treeview.pack(fill=BOTH, expand=1)

        self.treeview.column("one", width=80, anchor="center")
        self.treeview.heading("one", text="정보")
        self.treeview.column("two", width=150, anchor="center")
        self.treeview.heading("two", text="정보")
        self.treeview['show'] = 'headings'

        treelist = [('개발자', '배창현'), ("깃허브", "Github_Link"), ("인스타그램", "Insta"), ("이메일", "To Mail")]

        for i in range(len(treelist)):
            self.treeview.insert('', 'end', text="", values=treelist[i], iid=str(i))

        self.treeview.bind('<ButtonRelease-1>', self.click_item)

        self.getValue = "선택후 클릭"
        self.showed = Button(self.developer_frame, text="VER 1.0.0", command=partial(self.operate, self.getValue))
        self.showed.pack(side=BOTTOM, padx=10, pady=10)
