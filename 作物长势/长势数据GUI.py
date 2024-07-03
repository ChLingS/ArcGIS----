import tkinter
from tkinter import ttk
import tkinter.messagebox as messagebox
import threading
import 作物长势.作物长势 as tools
from asset.进度条GUI import ProgressWindow


class CropGrowth(ttk.Frame):
    def __init__(self, parent, city_selection):
        super().__init__(parent, style="Card.TFrame", padding=15)
        self.city_selection = city_selection
        self.columnconfigure(0, weight=1)
        self.add_widgets()  # 添加控件

    def add_widgets(self):
        self.mark = tkinter.Label(self, text="选定长势矢量文件", anchor='w', font=("Helvetica", 16))
        self.mark.grid(row=0, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.input = ttk.Entry(self)
        self.input.insert(0, "F:\企业实习\早稻地块数据")
        self.input.grid(row=1, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.date_mark = ttk.Label(self, text="选定长势日期", anchor='w', font=("Helvetica", 16))
        self.date_mark.grid(row=2, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.date = ttk.Entry(self)
        self.date.insert(0, "202405")
        self.date.grid(row=3, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.tif_file_note = ttk.Label(self, text="选定长势栅格文件", anchor='w', font=("Helvetica", 16))
        self.tif_file_note.grid(row=4, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.tif_file = ttk.Entry(self)
        self.tif_file.insert(0, r"F:\企业实习\早稻\PtythonProject\NDVI长势监测\JX_NDVI_05_reclass.tif")
        self.tif_file.grid(row=5, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.excel_area_note = ttk.Label(self, text="选定县级面积文件夹", anchor='w', font=("Helvetica", 16))
        self.excel_area_note.grid(row=6, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.excel_area = ttk.Entry(self)
        self.excel_area.insert(0, r"F:\企业实习\地块面积excel数据\水稻Excel")
        self.excel_area.grid(row=7, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.out_mark = tkinter.Label(self, text="选择导出文件路径", anchor='w', font=("Helvetica", 16), fg="red")
        self.out_mark.grid(row=8, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.output = ttk.Entry(self)
        self.output.insert(0, "F:\企业实习\长势数据")
        self.output.grid(row=9, column=0, padx=5, pady=(0, 1), sticky="ew")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=10, column=0, pady=10, sticky="ew")

        self.button = ttk.Button(self, text="处理", command=self.start_work)
        self.button.grid(row=11, column=0, padx=5, pady=10, sticky="ew")

    def start_work(self):
        self.progress_window = ProgressWindow(self)
        threading.Thread(target=self.work).start()  # 创建一个新的线程来执行工作

    def work(self):
        try:
            date: str = self.date.get()
            frame: str = self.input.get()
            out_path: str = self.output.get()
            tif_file: str = self.tif_file.get()
            frame_area: str = self.excel_area.get()
            # 获取城市
            selected_cities = self.city_selection.get_selected_options()

            # 检查参数是否为空
            parameters = {"date": date, "frame": frame, "out_path": out_path, "tif_file": tif_file,
                          "frame_area": frame_area, "selected_cities": selected_cities}
            for param_name, param_value in parameters.items():
                if not param_value:
                    raise ValueError(f"参数 '{param_name}' 为空")

            for city in selected_cities:
                res = tools.Crop_Growth(
                    date=date, city=city, frame_path=frame, out_path=out_path, tif_file=tif_file
                )
                res.tif_to_shp()
                res2 = tools.ExportToExcel(date=date, city=city, out_path=out_path)
                res3 = tools.TranslateExcel(res2, area_exels_path=frame_area)
                res3.Xlprocess()
                res3.write()
            self.progress_window.stop()  # 停止动画
        except Exception as e:
            self.progress_window.stop()  # 停止动画
            messagebox.showerror("错误", f"{e}")
