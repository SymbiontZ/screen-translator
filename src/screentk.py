import tkinter as tk
from PIL import ImageGrab
from datetime import datetime

class SnippingTool:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.attributes("-topmost", True)
        self.master.attributes("-alpha", 0.025)
        self.master.attributes("-fullscreen", True)
        #self.master.overrideredirect(True)

        # SCREEN BOX SNIPPING DIMENSIONS

        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None

        self.screenshot: str = None

        #Tkinter canvas

        self.canvas = tk.Canvas(
            master=self.master,
            cursor="cross",
            height= 1080,
            width= 1920
        )

        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.master.bind("<Escape>", self.remove_snipping)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)



    def on_press(self, event):
        self.x1 = self.master.winfo_pointerx()
        self.y1 = self.master.winfo_pointery()
        self.master.attributes("-alpha", 0.5)

        # print(self.x1, self.y1)

    def on_drag(self, event):
        currX = self.master.winfo_pointerx()
        currY = self.master.winfo_pointery()

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
        self.x2 = self.master.winfo_pointerx()
        self.y2 = self.master.winfo_pointery()

        self.master.attributes("-alpha", 0)
        
        
        self.remove_snipping()
        self.do_screenshot()

    def do_screenshot(self):
        left = min(self.x1, self.x2)
        top = min(self.y1, self.y2)
        right = max(self.x1, self.x2)
        bottom = max(self.y1, self.y2)

        bbox = (left, top, right, bottom)


        timestamp = datetime.now().strftime(r"%Y-%m-%d_%H-%M-%S")

        screenshot = ImageGrab.grab(bbox= bbox)
        self.screenshot = f"screenshot_{timestamp}.png"
        screenshot.save(self.screenshot)

        # print("DIMENSIONS:", bbox)

    def remove_snipping(self, event=None):
        self.master.quit()

# root = tk.Tk()
# st = SnippingTool(root)

# root.mainloop()