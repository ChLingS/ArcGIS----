import tkinter
from tkinter import ttk


class CheckBoxDemo(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="选择处理作物", padding=15)

        self.var = tkinter.StringVar(self)

        self.add_widgets()

    def add_widgets(self):
        self.radiobutton_1 = ttk.Radiobutton(self, text="油菜", variable=self.var, value="油菜", state="disabled")
        self.radiobutton_1.grid(row=1, column=0, padx=(30, 0), pady=(5, 10), sticky="w")

        self.radiobutton_2 = ttk.Radiobutton(self, text="早稻", variable=self.var, value="早稻")
        self.radiobutton_2.grid(row=2, column=0, padx=(30, 0), pady=10, sticky="w")

        self.radiobutton_3 = ttk.Radiobutton(self, text="其他", variable=self.var, value="长势", state="disabled")
        self.radiobutton_3.grid(row=3, column=0, padx=(30, 0), pady=(10, 0), sticky="w")


class CitySelection(ttk.LabelFrame):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, text="选择城市", padding=15, **kwargs)
        self.options = ["南昌市", "九江市", "上饶市", "抚州市", "宜春市", "吉安市", "赣州市", "景德镇市", "萍乡市", "新余市", "鹰潭市"]
        self.var = [tkinter.IntVar() for _ in self.options]
        self.checkboxes = [ttk.Checkbutton(self, text=option, variable=var) for option, var in zip(self.options, self.var)]

        for cb in self.checkboxes:
            cb.pack(side="top", anchor="w")

        self.btn = ttk.Button(self, text="全选/全取消", command=self.select_deselect_all)
        self.btn.pack(side="top")

    def select_deselect_all(self):
        if all(var.get() == 0 for var in self.var):
            for var in self.var:
                var.set(1)
        else:
            for var in self.var:
                var.set(0)

    def get_selected_options(self):
        return [option for option, var in zip(self.options, self.var) if var.get() == 1]