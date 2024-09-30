from src.config import Config, translationsPath
from typing import Optional, Union
import deepl, json
from deepl import TextResult, DeepLException

class Translator:
    '''
    A class used to represent a translator

    Attributes
    ----------
    config: Config
        An object from Config class that contains apikey and lang

    transCache: dict[ str, str or dict[ str, str ] ]
        Translations storage in JSON file serialized to dictionary 
        (The purpose is to not overuse API)

    srcText: str
        The text will be translated
    
    srcLang: str
        The language from srcText
    
    transLang: str
        The text already translated in language indicated

    transLang: str
        The language will be translated srcText

    '''

    def __init__(self, srcText: str,config: Config, lang: Optional[str] = None):
        self.config: Config = config
        self.transCache: dict[str, Union[str, dict[str, str]]] = self.load_cache_translations()

        self.srcText: str = srcText
        self.srcLang: str = self.get_src_lang()

        self.transLang: str = lang if lang is not None else config.lang
        self.transText: str = self.translate_text()
    
    def __str__(self) -> str:
        return f"[ {self.srcLang} ] {self.srcText} -> [ {self.transLang} ] {self.transText}"

    def translate_text(self) -> Optional[str]:
        transText = self.get_translation()
        if not transText:
            print("Translating from Deepl...")
            translator = deepl.Translator(self.config.apiKey)
            transResult: TextResult = translator.translate_text(self.srcText, target_lang=self.transLang)

            transText = transResult.text
            srcLang = transResult.detected_source_lang
            print(srcLang)
            self.save_translation(transText, srcLang)
                
        return transText

    @staticmethod
    def load_cache_translations() -> dict[dict[str, str], dict[str, str]]:
        '''
        Sets transCache from translations.json

        If raises FileNotFoundError returns an empty dict meaning
        it will be create a new translations.json file
        '''
        try:

            with open(translationsPath, "r", encoding="utf-8") as tf:
                return json.load(tf)
            
        except FileNotFoundError:
            return {}
        
        except json.JSONDecodeError:
            return {}
    
    def get_src_lang(self) -> str:
        return self.transCache.get(self.srcText, {}).get("srcLang")
    
    def get_translation(self) -> str:
        return self.transCache.get(self.srcText, {}).get(self.transLang)

    def save_translations(self):
        with open(translationsPath, "w", encoding="utf-8") as tf:
            json.dump(self.transCache, tf, ensure_ascii=False, indent=4)

    def save_translation(self, transText: str, srcLang: str):
        if not self.srcText in self.transCache:
            self.transCache[self.srcText] = {}
        
        self.srcLang = srcLang
        self.transCache[self.srcText]["srcLang"] = srcLang
        self.transCache[self.srcText][self.transLang] = transText
        self.save_translations()

