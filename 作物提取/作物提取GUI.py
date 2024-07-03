import tkinter
from tkinter import ttk
import tkinter.messagebox as messagebox
import os
import threading
from asset.进度条GUI import ProgressWindow
from 作物提取.作物提取 import Zone

class InputsAndButtonsDemo(ttk.Frame):
    def __init__(self, parent, city_selection):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.city_selection = city_selection
        self.exit_mid_file = tkinter.IntVar()
        self.columnconfigure(0, weight=1)
        self.add_widgets()

    def add_widgets(self):
        # 矢量数据
        self.label = tkinter.Label(self, text="选择包含原始田块矢量数据的文件夹", anchor='w', font=("Helvetica", 12))
        self.label.grid(row=0, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.entry = ttk.Entry(self)
        # self.entry.insert(0, "绝对路径")
        self.entry.insert(0, "F:\测试\shp")
        self.entry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # 阈值
        self.label2 = tkinter.Label(self, text="输入分割阈值", anchor='w', font=("Helvetica", 12))
        self.label2.grid(row=2, column=0, padx=1, pady=1, sticky="ew")

        self.spinbox = ttk.Spinbox(self, from_=0, to=100, increment=0.01)
        self.spinbox.insert(0, "0.2")
        self.spinbox.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

        self.label3 = tkinter.Label(self, text="设置输出路径", anchor='w', font=("Helvetica", 12))
        self.label3.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.entry2 = ttk.Entry(self)
        # self.entry2.insert(0, "绝对路径")
        self.entry2.insert(0, "F:\测试\out")
        self.entry2.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

        # 栅格
        self.label4 = tkinter.Label(self, text="选择原始作物栅格数据", anchor='w', font=("Helvetica", 12))
        self.label4.grid(row=6, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.entry3 = ttk.Entry(self)
        # self.entry3.insert(0, "绝对路径")
        self.entry3.insert(0, "F:\企业实习\原始地块第二版\drive-download-20240424T140030Z-001\早稻_第二版.tif")
        self.entry3.grid(row=7, column=0, padx=5, pady=10, sticky="ew")

        # 数据库
        self.label5 = ttk.Label(self, text="选择地理数据库", anchor='w', font=("Helvetica", 12))
        self.label5.grid(row=8, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.entry4 = ttk.Entry(self)
        # self.entry4.insert(0, "绝对路径")
        self.entry4.insert(0, "F:\测试\database.gdb")
        self.entry4.grid(row=9, column=0, padx=5, pady=10, sticky="ew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=10, column=0, pady=10, sticky="ew")


        self.checkbuttion_exit_mid_file = ttk.Checkbutton(self, text="是否保存中间文件", variable=self.exit_mid_file, state='nomal')
        self.checkbuttion_exit_mid_file.grid(row=11, column=0, padx=5, pady=10, sticky="ew")

        self.button = ttk.Button(self, text="处理", command=self.start_work)
        self.button.grid(row=12, column=0, padx=5, pady=10, sticky="ew")

    # def test(self):
    #     stautes =
    #     print(stautes)

    def start_work(self):
        self.progress_window = ProgressWindow(self)
        threading.Thread(target=self.work).start()  # 创建一个新的线程来执行工作

    def work(self):
        # 获取系数
        shp_path: str = self.entry.get()
        tif_path: str = self.entry3.get()
        out_path: str = self.entry2.get()
        clip_thresholds: str = self.spinbox.get()
        database_path: str = self.entry4.get()
        # 获取城市
        selected_cities = self.city_selection.get_selected_options()
        print(selected_cities)
        if not os.path.exists(shp_path):
            messagebox.showerror("参数错误", "输入路径不存在")
        elif not os.path.exists(tif_path):
            messagebox.showerror("参数错误", "栅格路径不存在")
        elif not os.path.exists(out_path):
            messagebox.showerror("参数错误", "输出路径不存在")
        elif not selected_cities:
            messagebox.showerror("参数错误", "请选择城市")
        elif not os.path.exists(database_path):
            messagebox.showerror("参数错误", "数据库路径不存在")
        else:
            try:
                if self.exit_mid_file.get():
                    Zone(
                        city=selected_cities,
                        shp_path=shp_path,
                        tif_path=tif_path,
                        thresholds=clip_thresholds,
                        database=database_path,
                        out_folder=out_path,
                        del_mid_file=True
                    )
                else:
                    Zone(
                        city=selected_cities,
                        shp_path=shp_path,
                        tif_path=tif_path,
                        thresholds=clip_thresholds,
                        database=database_path,
                        out_folder=out_path,
                        del_mid_file=False
                    )
                self.progress_window.stop()  # 停止动画
            except Exception as e:
                self.progress_window.stop()  # 停止动画
                messagebox.showerror("错误", f"{e}")