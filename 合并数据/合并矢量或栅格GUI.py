import tkinter
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
import threading
from asset.进度条GUI import ProgressWindow
from 合并数据.合并所有矢量 import merge_all_shp_files, merge_all_tif


class MergeFiles(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.columnconfigure(0, weight=1)
        self.add_widgets()

    def add_widgets(self):
        self.label = tkinter.Label(self, text="该工具合并文件夹及其子文件夹下所有指定文件类型", anchor='w', font=("Helvetica", 16), fg="red")
        self.label.grid(row=0, column=0, padx=5, pady=(0, 1), sticky="ew")

        # 输入数据
        self.label = tkinter.Label(self, text="选择含有数据的文件夹", anchor='w', font=("Helvetica", 12))
        self.label.grid(row=1, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.entry = ttk.Entry(self)
        # self.entry.insert(0, "绝对路径")
        self.entry.insert(0, "F:\测试\shp")
        self.entry.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        # 导出数据
        self.label1 = tkinter.Label(self, text="输出合并的文件", anchor='w', font=("Helvetica", 12))
        self.label1.grid(row=1, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.entry2 = ttk.Entry(self)
        # self.entry2.insert(0, "绝对路径")
        self.entry2.insert(0, "F:\测试\out")
        self.entry2.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=4, column=0, pady=10, sticky="ew")

        # 创建一个StringVar变量来存储选中的值
        self.selected_value = tkinter.StringVar()

        # 创建两个Radiobutton控件
        rb1 = ttk.Radiobutton(self, text="栅格", value="栅格", variable=self.selected_value)
        rb2 = ttk.Radiobutton(self, text="矢量", value="矢量", variable=self.selected_value)

        # 将Radiobutton控件添加到窗口中
        rb1.grid(row=5, column=0, pady=10, sticky="ew")
        rb2.grid(row=6, column=0, pady=10, sticky="ew")

        self.button = ttk.Button(self, text="处理", command=self.start_work)
        self.button.grid(row=7, column=0, padx=5, pady=10, sticky="ew")

    def test(self):
        stautes = self.selected_value
        print(stautes.get())

    def start_work(self):
        self.progress_window = ProgressWindow(self)
        threading.Thread(target=self.work).start()  # 创建一个新的线程来执行工作

    def work(self):
        # 获取系数
        shp_path: str = self.entry.get()
        out_path: str = self.entry2.get()
        file_type = self.selected_value.get()
        if not os.path.exists(shp_path):
            messagebox.showerror("参数错误", "输入路径不存在")
        # elif not os.path.exists(out_path):
        #     messagebox.showerror("参数错误", "输出路径不存在")
        else:
            try:
                if file_type == "矢量":
                    merge_all_shp_files(shp_path, out_path)
                if file_type == "栅格":
                    dirname = os.path.dirname(out_path)
                    print('Directory in path: ', dirname)
                    basename = os.path.basename(out_path)
                    print('File name: ', basename)
                    merge_all_tif(shp_path, dirname, basename)
                self.progress_window.stop()  # 停止动画
            except Exception as e:
                messagebox.showerror("错误", f"{e}")