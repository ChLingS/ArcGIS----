import tkinter
from tkinter import ttk
from 作物与城市选取.作物与城市选取GUI import CitySelection, CheckBoxDemo
from 作物提取.作物提取GUI import InputsAndButtonsDemo
from 合并数据.合并矢量或栅格GUI import MergeFiles
from 导出作物面积.导出作物面积GUI import ExportFramlandArea
from 查看数据.查看矢量详情GUI import ShowDetail
from 作物长势.长势数据GUI import CropGrowth
import sv_ttk


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        for index in range(2):
            self.columnconfigure(index, weight=1)
            self.rowconfigure(index, weight=1)

        CheckBoxDemo(self).grid(row=0, column=0, padx=(0, 5), pady=(0, 10), sticky="nsew")

        city_selection = CitySelection(self)
        city_selection.grid(row=1, column=0, padx=(0, 5), pady=(0, 10), sticky="nsew")

        self.inputs_and_buttons_demo = InputsAndButtonsDemo(self, city_selection)
        self.inputs_and_buttons_demo.grid(row=0, column=1, rowspan=2, padx=10, pady=(1, 0), sticky="nsew")

        self.crop_growth = CropGrowth(self, city_selection)
        self.crop_growth.grid(row=0, column=1, rowspan=2, padx=10, pady=(1, 0), sticky="nsew")
        self.crop_growth.grid_remove()


        self.area_demo = MergeFiles(self)
        self.area_demo.grid(row=0, column=1, rowspan=2, padx=10, pady=(1, 0), sticky="nsew")
        self.area_demo.grid_remove()  # 默认隐藏MergeFiles

        self.export_framland_area = ExportFramlandArea(self)
        self.export_framland_area.grid(row=0, column=1, rowspan=2, padx=10, pady=(1, 0), sticky="nsew")
        self.export_framland_area.grid_remove()  # 默认隐藏ExportFramlandArea

        self.show_shp_detail = ShowDetail(self)
        self.show_shp_detail.grid(row=0, column=1, rowspan=2, padx=10, pady=(1, 0), sticky="nsew")
        self.show_shp_detail.grid_remove()

        # 创建一个菜单
        menubar = tkinter.Menu(parent)
        parent.config(menu=menubar)
        menubar.add_separator()
        # 在菜单中添加两个命令，用来切换InputsAndButtonsDemo和MergeFiles的显示状态
        menubar.add_command(label="作物提取", command=self.show_inputs_and_buttons_demo)
        menubar.add_command(label="长势提取", command=self.show_crop_growth)
        menubar.add_command(label="数据编辑", command=self.show_area_demo)
        menubar.add_command(label="导出田块面积", command=self.show_export_framland_area)
        menubar.add_command(label="查看矢量", command=self.show_shp)

    def show_inputs_and_buttons_demo(self):
        self.inputs_and_buttons_demo.grid()
        self.area_demo.grid_remove()
        self.export_framland_area.grid_remove()
        self.show_shp_detail.grid_remove()
        self.crop_growth.grid_remove()

    def show_crop_growth(self):
        self.crop_growth.grid()
        self.inputs_and_buttons_demo.grid_remove()
        self.export_framland_area.grid_remove()
        self.show_shp_detail.grid_remove()
        self.area_demo.grid_remove()

    def show_area_demo(self):
        self.area_demo.grid()
        self.inputs_and_buttons_demo.grid_remove()
        self.export_framland_area.grid_remove()
        self.show_shp_detail.grid_remove()
        self.crop_growth.grid_remove()

    def show_export_framland_area(self):
        self.export_framland_area.grid()
        self.area_demo.grid_remove()
        self.inputs_and_buttons_demo.grid_remove()
        self.show_shp_detail.grid_remove()
        self.crop_growth.grid_remove()

    def show_shp(self):
        self.show_shp_detail.grid()
        self.area_demo.grid_remove()
        self.inputs_and_buttons_demo.grid_remove()
        self.export_framland_area.grid_remove()
        self.crop_growth.grid_remove()


def main():
    root = tkinter.Tk()
    root.title("提取田块")
    root.iconbitmap(r'icon.ico')
    sv_ttk.set_theme("light")

    App(root).pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    main()
