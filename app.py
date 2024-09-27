from src.translator import Translator
from src.config import Config

def main():
    config = Config()
    trans = Translator("Hello!", config=config, lang="DE")
    print(trans)

if __name__ == "__main__":
    main()