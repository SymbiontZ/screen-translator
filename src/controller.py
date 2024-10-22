import tkinter as tk
from typing import Optional
from time import sleep

from .image_ocr import ImageProcessor
from .config import TranslatorLang
from .gui.initialmenu import InitialMenu
from .gui.errorHandler import ErrorHandler
from .gui.snippingTool import SnippingTool
from .gui.resultMenu import ResultMenu


class AppController(tk.Tk):
    def __init__(self, tl: TranslatorLang):
        super().__init__()  #Calls the constructor of the parent class, necessary to inherit from tk.Tk.
        self.tl = tl

        self.bboxSel: Optional[tuple[int, int, int, int]] = None
        self.textProcessed: Optional[str] = None

        self.title("SYMBZ Tools")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)


        self.frames = {} #Stores frames as objects to use them easily and faster
        self.actualFrame = None

        for F in (InitialMenu, SnippingTool, ErrorHandler, ResultMenu):
            frameName = F.__name__
            frame = F(self.container, self, self.tl)
            self.frames[frameName] = frame

            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("InitialMenu")
        
   
    def show_frame(self, frameName):
        for f in self.frames.values():
            f.forget()
        self.actualFrame = self.frames[frameName]
        self.actualFrame.tkraise()

        if frameName == "InitialMenu":
            self.set_resolution(800, 400)
        
        elif frameName == "SnippingTool":
            self.activate_snippingtool_mode()

        elif frameName == "ResultMenu":
            self.set_resolution(1200, 800)
            self.actualFrame.update()
        
        elif frameName == "ErrorHandler":
            self.set_resolution(600, 200)
        


    def set_resolution(self, width, height):
        self.geometry(f"{width}x{height}")

    def activate_snippingtool_mode(self):
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.025)
        self.attributes("-fullscreen", True)
    def deactivate_snippingtool_mode(self):
        self.attributes("-topmost", False)
        self.attributes("-alpha", 1)
        self.attributes("-fullscreen", False)
    
    def middle_transparency(self):
        self.attributes("-alpha", 0.5)
    def full_transparency(self):
        self.attributes("-alpha", 0)

    def reset_data(self):
        self.bboxSel = None
        self.textProcessed = None

    def trigger_error(self, error):
        error_frame = self.frames["ErrorHandler"]
        error_frame.set_error(error)
        self.show_frame("ErrorHandler")
    
    def stop_app(self):
        self.destroy()

    def img_to_txt(self):
        if self.bboxSel[0] == self.bboxSel[2] or self.bboxSel[1] == self.bboxSel[3]:
            print("TEST INVALID AREA")
            self.bboxSel = None
            self.trigger_error("Invalid Area selected")
        else:
            img_txt = ImageProcessor(bbox= self.bboxSel)
            self.textProcessed = img_txt.get_processed_text()
            self.tl.textSRC = self.textProcessed
        
            if not self.textProcessed:
                self.trigger_error("Not text in the image to translate")
            else:
                self.do_translation()
                print("TEST TRANSLATION")

    def do_translation(self):
        if not self.tl.langDEST:
            self.trigger_error("Not valid language to translate")
        else:
            self.tl.translate_text(self.textProcessed)
            self.show_frame("ResultMenu")
            
            
