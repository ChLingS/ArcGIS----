import tkinter
from tkinter import ttk
import threading
from asset.进度条GUI import ProgressWindow
from 导出作物面积.导出作物面积 import ExportFlamlandExcel


class ExportFramlandArea(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.columnconfigure(0, weight=1)
        self.add_widgets()

    def add_widgets(self):
        self.mark = tkinter.Label(self, text="选定作物矢量文件", anchor='w', font=("Helvetica", 16), fg="red")
        self.mark.grid(row=0, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.input = ttk.Entry(self)
        self.input.insert(0, "绝对路径")
        self.input.grid(row=1, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.out_mark = tkinter.Label(self, text="选择导出文件路径", anchor='w', font=("Helvetica", 16), fg="red")
        self.out_mark.grid(row=2, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.output = ttk.Entry(self)
        self.output.insert(0, "绝对路径")
        self.output.grid(row=3, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.button = ttk.Button(self, text="处理", command=self.start_work)
        self.button.grid(row=4, column=0, padx=5, pady=10, sticky="ew")


    def start_work(self):
        self.progress_window = ProgressWindow(self)
        threading.Thread(target=self.work).start()  # 创建一个新的线程来执行工作

    def work(self):
        table = ExportFlamlandExcel(self.input.get(), self.output.get())
        table.create_area_table()
        self.progress_window.stop()  # 停止动画


