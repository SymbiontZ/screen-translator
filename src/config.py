import os, json
from pathlib import Path
from typing import Union
import ctypes, platform

localDir = os.getcwd()
dataPath: Path = Path(os.path.join(localDir,"data"))
confPath: Path = Path(dataPath, "config.json")
translationsPath: Path = Path(dataPath, "translations.json")


class Config:
    '''
    A class used to represent configuration of translator

    Attributes
    ----------
    apiKey: str
        an apikey from Deepl saved on .env file
    
    lang: str
        the lang from config.json file

        Example: ES, EN, DE, etc...


    Methods
    -------
    get_api_key()
        Sets apikey attribute from .env file
    
    get_lang()
        Sets lang attribute from config.json file
    '''
    def __init__(self):
        self.apiKey = self.get_api_key()
        self.lang = self.get_lang()

    @staticmethod
    def get_api_key() -> Union[str, ValueError]:
        '''
        Sets the apikey attribute from .env file

        Raises
        ------
        ValueError
            If no APIKEY is defined in .env file
        '''

        apiKey = os.getenv("APIKEY")
        if not apiKey:
            raise ValueError("Apikey not defined in .env file")
        return apiKey

    @staticmethod
    def get_lang() -> str:
        '''
        Sets the lang attribute from config.json file

        If the config.json file not exists, it creates one
        with the default lang [EN]

        '''
        if not confPath.is_file():
            with open(confPath, "w") as confFile:
                default_conf = {"lang": "EN"}
                json.dump(default_conf, confFile, indent=4)
        
        with open(confPath, "r") as confFile:
            data = json.load(confFile)
            return data.get("lang", "EN")
        

def make_dpi_aware():
    """Hacer que la aplicación sea DPI-aware en sistemas Windows"""
    try:
        if platform.system() == "Windows":
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print("No se pudo ajustar la DPI Awareness:", e)
