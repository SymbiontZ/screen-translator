from src.translator import Translator
from src.config import Config

def main():
    config = Config()
    trans = Translator("Me encantan los trenes", config=config, lang="EN-GB")
    print(trans)

if __name__ == "__main__":
    main()