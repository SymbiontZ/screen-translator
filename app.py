from src.config import make_dpi_aware, Language
from src.translator import Translator
from src.screentk import AppController

import tkinter as tk

def main():
    make_dpi_aware()
    lang = Language()
    translator = Translator()
    app = AppController(lang, translator)
    app.run()
    

    
    
if __name__ == "__main__":
    main()
