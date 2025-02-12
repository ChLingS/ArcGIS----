import tkinter
from tkinter import ttk
import threading
from asset.进度条GUI import ProgressWindow
from 查看数据.查看矢量详情 import ShowShapefile


class ShowDetail(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.columnconfigure(0, weight=1)
        self.add_widgets()  # 添加控件

    def add_widgets(self):
        self.mark = tkinter.Label(self, text="选定矢量文件", anchor='w', font=("Helvetica", 16), fg="red")
        self.mark.grid(row=0, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.input = ttk.Entry(self)
        self.input.insert(0, "绝对路径")
        self.input.grid(row=1, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.button = ttk.Button(self, text="处理", command=self.start_work)
        self.button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

    # def show_table(self, df):
    #     frame = tkinter.Frame(self)
    #     frame.grid(sticky='nsew')  # 使用 grid 布局
    #     # 创建Treeview控件
    #     tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    #     # 定义表头
    #     for column in df.columns:
    #         tree.heading(column, text=column)
    #     # 插入数据
    #     for index, row in df.iterrows():
    #         tree.insert('', 'end', values=list(row))
    #
    #     tree.grid(sticky='nsew')  # 使用 grid 布局

    def start_work(self):
        self.progress_window = ProgressWindow(self)
        threading.Thread(target=self.work).start()  # 创建一个新的线程来执行工作

    def work(self):
        try:
            table = ShowShapefile(self.input.get())
            self.progress_window.stop()
            table.show()
        except Exception as e:
            print(e)
        self.progress_window.stop()
