import os, deepl
from pathlib import Path
from typing import Union, Optional
import ctypes, platform, requests, pytesseract

localDir = os.getcwd()
dataPath: Path = Path(os.path.join(localDir,"data"))

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TranslatorLang:
    '''
    A class used to represent languages of translator

    Attributes
    ----------

    Methods
    -------
    '''
    def __init__(self):
        self.langSRC: tuple[str, str]= None
        self.langDEST: tuple[str, str] = None
        #self.lang is like (EN-GB, English (British))

        self.textSRC: str = None
        self.textDEST: str = None


        self.DEEPLTranslator = deepl.Translator(get_api_key())
    
    def set_lang_src(self, lang: str):
        if not lang:
            self.langSRC = (None, "Detected Language")
        elif lang and lang not in self.get_langs_deepl("source", "list"):
            raise ValueError("Not valid lang from to translate TEST")
        else:
            langsDict = self.get_langs_deepl("source", "dict")
            langCode = langsDict.get(lang)
            self.langSRC = (langCode, lang)


    def set_lang_dest(self, lang: str):
        if lang not in self.get_langs_deepl("target", "list"):
            raise ValueError("Not valid lang from to translate")
        
        langsDict = self.get_langs_deepl("target", "dict")
        langCode = langsDict[lang]
        self.langDEST = (langCode, lang)

    def translate_text(self, text: str) -> Optional[str]:
        self.srcText = text
        if self.langSRC[0]:
            result = self.DEEPLTranslator.translate_text(
                self.srcText, 
                source_lang=self.langSRC[0], 
                target_lang=self.langDEST[0])
        else:
            result = self.DEEPLTranslator.translate_text(
                self.srcText, 
                target_lang=self.langDEST[0])

        self.textDEST = result.text
    
    @staticmethod
    def get_langs_deepl(type: str, typedata: str) -> dict[str, str]:
        #REQUEST TO AVAILABLE LANGUAGES IN DEEPL
        apikey = get_api_key()
        url = "https://api-free.deepl.com/v2/languages"
        params = { "type": f"{type}" }
        headers = {
            "Authorization": f"DeepL-Auth-Key {apikey}",
            "User-Agent": "ScreenTranslator/4.1.0"
        }
        
        response = requests.get(url, headers=headers, params=params)
        #The request returns a list like: [{"RU":"Russian"}, {"FR":"French"}, ...]
        langsList = response.json()
        
        #Transform to {"Russian":"RU","French": "FR"}
        langsDict: dict[str, str] = {lang["name"]: lang["language"] for lang in langsList}
        
        langsList = [lang for lang in langsDict]
        
        if typedata == "dict":
            return langsDict
        elif typedata == "list":
            return langsList
        else:
            raise ValueError("Not valid typedata to get languages")

    
    def reset_data(self):
        self.langSRC = None
        self.langDEST = None
        self.textSRC = None
        self.textDEST = None
        
    
    @staticmethod
    def get_langs_tesseract() -> list[str]:
        langsList = pytesseract.get_languages()
        return langsList


def get_api_key() -> Union[str, ValueError]:
    '''
    This function returns the apikey attribute from .env file

    Raises
    ------
    ValueError
        If no APIKEY is defined in .env file
    '''

    apiKey = os.getenv("APIKEY")
    if not apiKey:
        raise ValueError("Apikey not defined in .env file")
    return apiKey

def make_dpi_aware() -> None:
    """Hacer que la aplicación sea DPI-aware en sistemas Windows"""
    try:
        if platform.system() == "Windows":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print("No se pudo ajustar la DPI Awareness:", e)

