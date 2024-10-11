import tkinter as tk
from PIL import ImageGrab
from datetime import datetime
from .config import Language
from .translator import Translator
from .image_ocr import ImageProcessor

color_bg = "#1e1920"

WINDOWTITLE = "Screen Translator v4.1.0"

class AppController:
    def __init__(self, lang: Language, translator: Translator):
        self.lang = lang
        self.translator = translator


    def show_language_selector(self):
        root = tk.Tk()
        root.title(WINDOWTITLE)
        root.geometry("600x300")

        LanguageSelector(root, self.lang, self)

        root.mainloop()

    def show_snipping_tool(self):
        root = tk.Tk()
        st = SnippingTool(root, self.translator, self.lang, self)
        root.mainloop()

    def show_message_box(self):
        root = tk.Tk()
        root.title(WINDOWTITLE)
        MessageBox(root, self.translator)
        
        root.mainloop()
        
    def run(self):
        self.show_language_selector()

class SnippingTool:
    def __init__(self, master: tk.Tk, translator: Translator, lang: Language, controller: AppController):
        self.translator = translator
        self.lang = lang
        self.controller = controller

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
        screenshotPath = f"./data/screenshot_{timestamp}.png"

        screenshot.save(screenshotPath)
        
        img_ocr = ImageProcessor(screenshotPath)

        self.translator.set_langSRC_code(self.lang)
        self.translator.set_langDEST_code(self.lang)

        self.translator.translate_text(img_ocr.get_processed_text())

        self.controller.show_message_box()
        # print("DIMENSIONS:", bbox)

    def remove_snipping(self, event=None):
        self.master.destroy()
        
class LanguageSelector:
    def __init__(self, master:tk.Tk, lang: Language, controller: AppController) -> None:
        self.master = master
        self.controller = controller

        #HEADER ELEMENT

        headerFont = ("Cascadia Code", 20, "bold")
        headerLabel = tk.Label(self.master, text="Screen Translator", font=headerFont)
        headerLabel.grid(row=0,column=0, columnspan=2, padx=20, pady=20)


        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        #LABEL ELEMENTS

        labelFont = ("Cascadia Code", 13)

        labelSRC = tk.Label(self.master, text="FROM:", font=labelFont)
        labelDEST = tk.Label(self.master, text="TO:", font=labelFont)

        labelSRC.grid(row=1, column=0, padx=20, pady=15)
        labelDEST.grid(row=1, column=1, padx=20, pady=15)

        #OPTIONMENU ELEMENTS
        
        #Obtain list available to use in translator
        langsListSRC = lang.get_langs_deepl(type="source", typedata="list")
        langsListDEST = lang.get_langs_deepl(type="target", typedata="list")

        self.ValueLangSRC = tk.StringVar()
        self.ValueLangSRC.set("Detect language")

        self.ValueLangDEST = tk.StringVar()
        self.ValueLangDEST.set("Default (English)")

        menuSRC = tk.OptionMenu(self.master, self.ValueLangSRC, *langsListSRC)
        menuDEST = tk.OptionMenu(self.master, self.ValueLangDEST, *langsListDEST)

        menuSRC.config(font=("Cascadia Code", 10))
        menuSRC["menu"].config(font=("Cascadia Code", 10))
        menuDEST.config(font=("Cascadia Code", 10))
        menuDEST["menu"].config(font=("Cascadia Code", 10))

        menuSRC.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        menuDEST.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        #BUTTON
        buttonFont = ("Cascadia Code", 12)
        transButton = tk.Button(self.master,text="Translate!", command=lambda: self.press_button(lang), font=buttonFont)
        transButton.grid(row=3, columnspan=2, padx=20, pady=10)

    def press_button(self, lang: Language):
        lang.langSRC = self.ValueLangSRC.get()
        lang.langDEST = self.ValueLangDEST.get()

        self.master.destroy()
        self.controller.show_snipping_tool()

class MessageBox:
    def __init__(self, master: tk.Tk, translator: Translator, error = None) -> None:
        self.master = master
        self.translator = translator

        errorFont = ("Cascadia code", 14)
        langHeaderFont = ("Cascadia code", 16, "bold")
        textFont = ("Cascadia code", 10)

        wrapLength = 1250 #Makes a maximum length to the text, necessary to not make text to long for the window.

        button = tk.Button(self.master, text="Continue.", command=self.on_exit, font=("Cascadia code", 14))

        if error:
            error_label = tk.Label(self.master, text=f"{error}", font=errorFont)
            error_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
            button.grid(row=1, column=0, padx=20, pady=10)
        elif not self.translator.transText:
            error_label = tk.Label(self.master, text="Cannot obtain translation. Try again later!", font=errorFont)
            error_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
            button.grid(row=1, column=0, padx=20, pady=10)
        else:

            langSRC_label = tk.Label(self.master, text=f"[{translator.langSRC_code if translator.langSRC_code else "Detected Language"}]", font=langHeaderFont)
            textSRC_label = tk.Label(self.master, text=f"{translator.srcText}", font=textFont, wraplength=wrapLength)

            langDEST_label = tk.Label(self.master, text=f"[{translator.langDEST_code}]", font=langHeaderFont)
            textDEST_label = tk.Label(self.master, text=f"{translator.transText}", font=textFont, wraplength=wrapLength)

            langSRC_label.grid(row=0, column=0, padx=20, pady=10)
            textSRC_label.grid(row=1, column=0, padx=20, pady=10)
            langDEST_label.grid(row=2, column=0, padx=20, pady=10)
            textDEST_label.grid(row=3, column=0, padx=20, pady=10)
            button.grid(row=4, column=0, padx=20, pady=10)
        
    def on_exit(self):
        self.master.destroy()

        
        
        
# lang = Language()
# root = tk.Tk()
# ls = LanguageSelector(root, lang)

# root.mainloop()