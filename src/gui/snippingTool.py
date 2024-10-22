import tkinter as tk
from ..config import TranslatorLang

class SnippingTool(tk.Frame):
    def __init__(self, parent, controller, tl: TranslatorLang):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.tl = tl

        # SCREEN BOX SNIPPING DIMENSIONS

        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None

        self.screenshot: str = None

        #Tkinter canvas

        self.canvas = tk.Canvas(
            master=self,
            cursor="cross",
            height=1080,
            width=1920
        )

        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Make the grid cell expand with the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)


    def on_press(self, event):
        self.x1 = self.winfo_pointerx()
        self.y1 = self.winfo_pointery()
        self.controller.middle_transparency()

    def on_drag(self, event):
        currX = self.winfo_pointerx()
        currY = self.winfo_pointery()

        self.canvas.delete("rect") #Deletes old rectangle before creating new one

        self.canvas.create_rectangle(
            self.x1,
            self.y1,
            currX,
            currY,
            outline= "black",
            fill="gray",
            tag = "rect"
        )

    def on_release(self, event):
        self.canvas.delete("rect")
        self.x2 = self.winfo_pointerx()
        self.y2 = self.winfo_pointery()

        self.controller.full_transparency()
        
        left = min(self.x1, self.x2)
        top = min(self.y1, self.y2)
        right = max(self.x1, self.x2)
        bottom = max(self.y1, self.y2)



        self.controller.bboxSel = (left, top, right, bottom)
        self.controller.deactivate_snippingtool_mode()
        self.controller.img_to_txt()
