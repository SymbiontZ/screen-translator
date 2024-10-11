import cv2 as cv
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageProcessor:
    def __init__(self, imagePath: str) -> None:
        self.imagePath = imagePath
        self.text: str = self.process_image()
    
    def __str__(self):
        return self.text
    
    def process_image(self):
        image = cv.imread(self.imagePath)

        grayImg = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        blurImg = cv.GaussianBlur(grayImg, (3,3), 0)
        bwImage = cv.threshold(blurImg, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

        resultPath = "./data/image_to_text.png"
        cv.imwrite(resultPath, bwImage)

        img = Image.open(resultPath)

        return pytesseract.image_to_string(img)
    
    def get_processed_text(self):
        return self.text


