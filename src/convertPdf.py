from pdf2image import convert_from_path
import os

from src.fileHelper import FileHelper
from src.helper import Helper


class ConvertPdf:
    input_path = ''
    pdf_images_path = ''

    pdf_set = set()

    def __init__(self, input_path, pdf_images_path):
        self.input_path = input_path
        self.pdf_images_path = pdf_images_path
        self.fillPdfSet()

    def fillPdfSet(self):
        Helper.print("Detect files:")
        root = self.input_path
        for dir_, _, files in os.walk(root):
            for file_name in files:
                self.pdf_set.add(file_name)
                Helper.print(file_name)

    def convertPdfs(self):
        Helper.print("Start conversion of images...")
        for pdf in self.pdf_set:
            pdf_path = os.path.join(self.input_path, pdf)
            rel_dir = os.path.splitext(pdf)[0]
            output_path = os.path.join(self.pdf_images_path, rel_dir)
            FileHelper.createSubdirectoriesIfNecessary(self.pdf_images_path, rel_dir)
            self.pdf2image(pdf_path, output_path)
        Helper.print("Conversion of images done...")

    def pdf2image(self, pdf_path, output_folder):
        pages = convert_from_path(pdf_path)

        i = 1
        for page in pages:
            base_filename = os.path.splitext(os.path.basename(pdf_path))[0] + '_' + str(i) + '.jpg'
            page.save(os.path.join(output_folder, base_filename), 'JPEG')
            i += 1


    #def imagese2pdf(self):
    # todo