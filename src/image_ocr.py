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
        enhancedImg = cv.convertScaleAbs(image, alpha=2.0, beta=0)
        greyImage = cv.cvtColor(enhancedImg, cv.COLOR_BGR2GRAY) 

        clahe = cv.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
        enhancedImg2 = clahe.apply(greyImage)

        gaussianBlurImg = cv.GaussianBlur(enhancedImg2, (1,1), 0)
        _, bw_image = cv.threshold(enhancedImg2, 128, 255, cv.THRESH_BINARY)

        resultPath = "image_to_text.png"
        cv.imwrite(resultPath, bw_image)

        img = Image.open(resultPath)

        return pytesseract.image_to_string(img)

