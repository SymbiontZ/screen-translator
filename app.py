from src.translator import Translator
from src.config import Config
from src.screentk import SnippingTool
import tkinter as tk

import time
def main():
    # config = Config()
    # trans = Translator('', config=config, lang="EN-GB")
    # print(trans)
    root = tk.Tk()
    st = SnippingTool(root)

    root.mainloop()


if __name__ == "__main__":
    main()
    