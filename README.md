# Screen Translator

This program will extract text from images and translate it into a selected language using the DeepL API.


## Installation

### Obtaining API key from DEEPL

In order to get your API key, you need to go [Deepl Api Pricing Website](https://www.deepl.com/en/pro/change-plan#developer) and chose your plan by creating an account. Then copy your API key.

Then you make a `.env` file and introduce your api like:
```shell
APIKEY = "9f43f-38...59rj"
```

### Setting up project

This are the commands you need to execute in shell on the directory you want to have the program.
```shell
git clone https://github.com/SymbiontZ/screen-translator.git
cd screen-translator/
python -m venv env
.\/.env/Scripts/activate
pip install -r requirements.txt
```

### Downloading Tesseract
Additionally, you need to install Tesseract OCR, which is necessary for converting images to text.
Installation guide [here](https://tesseract-ocr.github.io/tessdoc/Installation.html#:~:text=Tesseract%20is%20available%20directly%20from,directly%20from%20the%20Linux%20distributions.)



Then you just need to execute `app.py` :)

## Using Screen Translator

After executing `python app.py`, a window will open:

![language selector](/docs/images/lang_select_menu.png)

1. Choose the language to translate from and the language to translate to.

2. Press the **Translate!** button.

Once you press the button, a snipping tool window will appear, similar to the one in Windows. Select the section of the screen you want to translate. 

![snipping tool box](/docs/images/snipping_tool_box.png)

Finally, when you release the mouse button, another window will appear with the translation.

![translation window](/docs/images/translation_window.png)

Please note that the translation may not be perfect, but it works for the majority of cases.