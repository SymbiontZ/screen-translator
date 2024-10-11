import os
from pathlib import Path
from typing import Union
import ctypes, platform, requests, pytesseract

localDir = os.getcwd()
dataPath: Path = Path(os.path.join(localDir,"data"))
translationsPath: Path = Path(dataPath, "translations.json")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Language:
    '''
    A class used to represent languages of translator

    Attributes
    ----------

    Methods
    -------

    '''
    def __init__(self, langSRC: str = None, langDEST: str = None):
        self.langSRC = langSRC
        self.langDEST = langDEST
        self.langSRC_TESSERACT = self.get_langs_tesseract()


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
        
        return None
    
    @staticmethod
    def get_langs_tesseract() -> list[str]:
        langsList = pytesseract.get_languages()
        return langsList
    
    def get_langSRC_code(self):
        langsDict = self.get_langs_deepl("source", "dict")
        return langsDict.get(self.langSRC, None)
    
    def get_langDEST_code(self):
        langsDict = self.get_langs_deepl("target", "dict")
        return langsDict.get(self.langDEST, "English (British)")
    
    

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

