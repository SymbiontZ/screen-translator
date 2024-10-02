from src.translator import Translator
from src.config import Config, make_dpi_aware
from src.screentk import SnippingTool

from src.image_ocr import ImageProcessor
import tkinter as tk
import time

def main():
    config = Config()

    time.sleep(3)

    make_dpi_aware()
    root = tk.Tk()
    st = SnippingTool(root)
    root.mainloop() 

    img_ocr = ImageProcessor(st.screenshot)
    print(img_ocr)
    trans = Translator(img_ocr.text, config=config)
    print(trans)

if __name__ == "__main__":
    main()
    