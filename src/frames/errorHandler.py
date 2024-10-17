import tkinter as tk

class ErrorHandler(tk.Frame):
    def __init__(self, parent, controller, lang):
        super().__init__(parent)
        self.controller = controller
        