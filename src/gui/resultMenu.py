import tkinter as tk
from ..config import TranslatorLang

class ResultMenu(tk.Frame):
    def __init__(self, parent, controller, tl: TranslatorLang):
        tk.Frame.__init__(self, parent)
        self.tl = tl
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        langHeaderFont = ("Cascadia code", 16, "bold")
        textFont = ("Cascadia code", 10)

        wrapLength = 1100 #Makes a maximum length to the text, necessary to not make text to long for the window.

        

        self.langSRC_label = tk.Label(self, text="None", font=langHeaderFont)
        self.textSRC_label = tk.Label(self, text=f"{self.tl.textSRC}", font=textFont, wraplength=wrapLength)

        self.langDEST_label = tk.Label(self, text=f"[{self.tl.langDEST[1] if self.tl.langDEST is not None else "None"}]", font=langHeaderFont)
        self.textDEST_label = tk.Label(self, text=f"{self.tl.textDEST}", font=textFont, wraplength=wrapLength)

        self.langSRC_label.grid(row=0, column=0,columnspan=2, padx=20, pady=10, sticky="nsew")   
        self.textSRC_label.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.langDEST_label.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        self.textDEST_label.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="nsew",ipadx=10, ipady=10)

        homeButton = tk.Button(self, text="Go home", command=self.go_back, font=("Cascadia code", 14))
        homeButton.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        exitButton = tk.Button(self, text="Continue", command=self.on_exit, font=("Cascadia code", 14))
        exitButton.grid(row=4, column=1, padx=20, pady=10, sticky="nsew")
    
    def go_back(self):
        self.tl.reset_data()
        self.controller.reset_data()
        self.controller.show_frame("InitialMenu")


    def update(self):
        self.langSRC_label.config(text=f"{self.tl.langSRC[1]}")
        self.langDEST_label.config(text=f"{self.tl.langDEST[1]}")

        self.textSRC_label.config(text=f"{self.tl.textSRC}")
        self.textDEST_label.config(text=f"{self.tl.textDEST}")
        
    def on_exit(self):
        self.controller.destroy()