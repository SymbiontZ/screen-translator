from src.config import make_dpi_aware, TranslatorLang
from src.controller import AppController

import tkinter as tk

def main():
    make_dpi_aware()
    tl = TranslatorLang()
    app = AppController(tl=tl)
    app.mainloop()

    
    
if __name__ == "__main__":
    main()
