import tkinter
from tkinter import ttk

class ProgressWindow(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("进度")
        self.progress = ttk.Progressbar(self, length=200, mode='indeterminate')
        self.progress.pack()
        self.progress.start()  # 开始动画

        # 更新窗口以获取准确的窗口大小
        self.update()

        # 获取父窗口的位置和大小
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # 计算窗口的左上角坐标，使其位于父窗口中央
        x = parent_x + (parent_width - self.winfo_reqwidth()) / 2
        y = parent_y + (parent_height - self.winfo_reqheight()) / 2

        # 设置窗口的位置
        self.geometry("+%d+%d" % (x, y))

    def stop(self):
        self.progress.stop()  # 停止动画
        self.destroy()  # 关闭窗口