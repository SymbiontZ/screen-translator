import tkinter as tk
from ..config import TranslatorLang

class InitialMenu(tk.Frame):
    def __init__(self, parent, controller, tl: TranslatorLang):
        super().__init__(parent)
        self.controller = controller
        self.tl = tl

        headerFont = ("Cascadia Code", 20, "bold")
        headerLabel = tk.Label(self, text="Screen Translator", font=headerFont)
        headerLabel.grid(row=0,column=0, columnspan=2, padx=20, pady=20)


        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #LABEL ELEMENTS

        labelFont = ("Cascadia Code", 13)

        labelSRC = tk.Label(self, text="FROM:", font=labelFont)
        labelDEST = tk.Label(self, text="TO:", font=labelFont)

        labelSRC.grid(row=1, column=0, padx=20, pady=15)
        labelDEST.grid(row=1, column=1, padx=20, pady=15)

        #OPTIONMENU ELEMENTS
        
        #Obtain list available to use in translator
        langsListSRC = self.tl.get_langs_deepl(type="source", typedata="list")
        langsListDEST = self.tl.get_langs_deepl(type="target", typedata="list")

        self.ValueLangSRC = tk.StringVar()
        self.ValueLangSRC.set("Detect language")

        self.ValueLangDEST = tk.StringVar()
        self.ValueLangDEST.set("Default (English)")

        menuSRC = tk.OptionMenu(self, self.ValueLangSRC, *langsListSRC)
        menuDEST = tk.OptionMenu(self, self.ValueLangDEST, *langsListDEST)

        menuSRC.config(font=("Cascadia Code", 10))
        menuSRC["menu"].config(font=("Cascadia Code", 10))
        menuDEST.config(font=("Cascadia Code", 10))
        menuDEST["menu"].config(font=("Cascadia Code", 10))

        menuSRC.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        menuDEST.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        #BUTTON
        buttonFont = ("Cascadia Code", 12)
        transButton = tk.Button(self, text="Translate!", command=lambda: self.press_button(), font=buttonFont)
        transButton.grid(row=3, columnspan=2, padx=20, pady=10)

    def press_button(self):
        langSRC = self.ValueLangSRC.get()
        langDEST = self.ValueLangDEST.get()
        if langDEST == "Default (English)":
            langDEST = "English (British)"
        if langSRC == "Detect language":
            langSRC = None

        self.tl.set_lang_src(langSRC) 
        self.tl.set_lang_dest(langDEST)

        print(langSRC, langDEST)
        print(self.tl.langSRC, self.tl.langDEST)