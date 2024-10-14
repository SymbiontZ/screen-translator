from src.config import Language, get_api_key
from typing import Optional, Union
import deepl

class Translator:
    '''
    A class used to represent a translator

    Attributes
    ----------

    '''

    def __init__(self):
        self.langSRC_code: str = None
        self.langDEST_code: str = None

        self.srcText: str = None
        self.transText: str = None
        self.DEEPLTranslator = deepl.Translator(get_api_key())
    
    def __str__(self) -> str:
        return f"[ {self.langSRC_code} ] {self.srcText} \n[ {self.langDEST_code} ] {self.transText}"
    
    def set_langSRC_code(self, lang: Language):
        self.langSRC_code = lang.get_langSRC_code()

    def set_langDEST_code(self, lang: Language):
        self.langDEST_code = lang.get_langDEST_code()

    def translate_text(self, text: str) -> Optional[str]:
        self.srcText = text
        if self.langSRC_code:
            transResult = self.DEEPLTranslator.translate_text(
                self.srcText, 
                source_lang=self.langSRC_code, 
                target_lang=self.langDEST_code)
        else:
            transResult = self.DEEPLTranslator.translate_text(
                self.srcText, 
                target_lang=self.langDEST_code)

        self.transText = transResult.text
                
        return self.transText
