import os, json
from pathlib import Path

localDir = os.getcwd()
dataPath: Path = Path(os.path.join(localDir,"data"))
settingsPath: Path = Path(dataPath, "settings.json")
translationsPath: Path = Path(dataPath, "translations.json")


class Config:
    '''
    Config class which contains apikey and lang used.
    '''
    def __init__(self):
        self.apiKey = self.get_api_key()
        self.lang = self.get_lang()

    @staticmethod
    def get_api_key() -> str | ValueError:
        apiKey = os.getenv("APIKEY")
        if not apiKey:
            raise ValueError("Apikey not defined in .env file")
        return apiKey

    @staticmethod
    def get_lang() -> str:
        if settingsPath.is_file():
            with open(settingsPath, "r") as settingsFile:
                data = json.load(settingsFile)
                return data.get("lang", "EN")

