import tkinter as tk
from typing import Optional

from .image_ocr import ImageProcessor
from .config import TranslatorLang
from .frames.initialmenu import InitialMenu
from .frames.errorHandler import ErrorHandler


class AppController(tk.Tk):
    def __init__(self, tl: TranslatorLang):
        super().__init__()  #Calls the constructor of the parent class, necessary to inherit from tk.Tk.
        self.tl = tl

        self.bboxSel: Optional[tuple[int, int, int, int]] = None
        self.textProcessed: Optional[str] = None

        self.title("Screen Translator v5")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {} #Stores frames as objects to use them easily and faster

        self.create_frames()

        self.show_frame("InitialMenu")

    
    def create_frames(self) -> None:
        "Makes the sections and adds it to container"
        for F in (InitialMenu, ErrorHandler):
            frameName = F.__name__
            frame = F(self.container, self, self.tl)
            self.frames[frameName] = frame
            frame.grid(row=0, column=0, sticky="nsew")
   
    def show_frame(self, frameName):
        frame = self.frames[frameName]
        frame.tkraise()

    def trigger_error(self, error):
        error_frame = self.frames["ErrorHandler"]
        error_frame.set_error(error)
        self.show_frame("ErrorHandler")
    
    def stop_app(self):
        self.destroy()

    def img_to_text(self):
        if not self.bboxSel: 
            self.bboxSel = None
            self.trigger_error("Invalid Area selected")
        else:
            img_txt = ImageProcessor(bbox= self.bboxSel)
            self.textProcessed = img_txt.get_processed_text()
        
        if not self.textProcessed:
            self.trigger_error("Not text in the image to translate")
        else:
            pass

    def do_translation(self):
        if not self.tl.langDEST:
            self.trigger_error("Not valid language to translate")
        else:
            self.tl.translate_text(self.textProcessed)
            
            
