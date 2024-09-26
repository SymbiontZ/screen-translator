from src.config import Config, translationsPath
import deepl, json


def translate_text(text: str) -> str:
    config = Config()
    lang = config.lang
    oldTranslations = load_old_translations()

    translatedText = get_translation(text, lang, oldTranslations)
    if not translatedText:
        print("Translating from Deepl...")
        translator = deepl.Translator(config.apiKey)
        translatedText = str(translator.translate_text(text, target_lang=lang))
    
        save_translation(text, translatedText, lang, oldTranslations)

    return translatedText

# LOAD TRANSLATIONS #

def load_old_translations():
    try:
        with open(translationsPath, "r") as tf:
            return json.load(tf)
    except FileNotFoundError:
        return {}
    
def get_translation(originalText, lang, oldTranslations: dict):
    return oldTranslations.get(originalText, {}).get(lang)
    
# SAVE TRANSLATIONS #

def save_translations(translations):
    with open(translationsPath, "w") as tf:
        json.dump(translations, tf, ensure_ascii=False, indent=4)

def save_translation(originalText, translatedText, lang, oldTranslations):
    if originalText not in oldTranslations:
        oldTranslations[originalText] = {}
    
    oldTranslations[originalText][lang] = translatedText
    save_translations(oldTranslations)
