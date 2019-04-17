from luminoth import Detector, read_image, vis_objects
import os
import xlwt
import re
from src.fileHelper import FileHelper
from src.helper import Helper

checkpointName = 'b708db9e0818'

class Detection:

    preprocessed_images_path = ''
    output_path = ''
    output_boundaries_path = ''
    output_pdf_path = ''

    image_folder_set = set()

    def __init__(self, preprocessed_images_path, output_path, output_boundaries_path, output_pdf_path):
        self.preprocessed_images_path = preprocessed_images_path
        self.pdf_images_path = output_path
        self.output_boundaries_path = output_boundaries_path
        self.output_pdf_path = output_pdf_path
        self.fillImageFolderSet(self.preprocessed_images_path)

    def fillImageFolderSet(self, root):
        for dir_ in os.listdir(root):
            self.image_folder_set.add(dir_)

    def detectTableBoundaries(self):
        Helper.print("Before the Checkpoint")
        detector = Detector(checkpoint=checkpointName)
        for folder in self.image_folder_set:
            Helper.print("Detecting table boundaries of file: " + folder)
            book = xlwt.Workbook()
            worksheet = book.add_sheet(folder)

            base_folder_path = os.path.join(self.preprocessed_images_path, folder)
            images = FileHelper.getAllFilesInFolder(base_folder_path)
            current_row = 0
            for image in images:
                page = re.search("^.*_(\d*)\..*$", image).group(1)
                tableInfos = self.detect(os.path.join(base_folder_path, image), detector)
                for tableInfo in tableInfos:
                    worksheet.write(current_row, 0, page)
                    #left = xmin
                    worksheet.write(current_row, 1, tableInfo["bbox"][0])
                    #top = ymin
                    worksheet.write(current_row, 2, tableInfo["bbox"][1])
                    #right = xmax
                    worksheet.write(current_row, 3, tableInfo["bbox"][2])
                    #bottom = ymax
                    worksheet.write(current_row, 4, tableInfo["bbox"][3])
                    current_row += 1
                    #print(tableInfo)
            Helper.print("Create Excel of table boundaries for file: " + folder)
            book.save(os.path.join(self.output_path, self.output_boundaries_path, folder) + ".xls")

    # path is for example: './data/preprocessed_input_data/eu-009/eu-009-page-001.jpg'
    def detect(self, image_path, detector):
        image = read_image(image_path)
        #image = read_image('C:\\Users\\Klaymen-Island\\PycharmProjects\\TabExImg\\src\\data\\02_preprocessed_images\\eu-009\\eu-009_1.jpg')
        # If no checkpoint specified, will assume `accurate` by default. In this case,
        # we want to use our traffic checkpoint. The Detector can also take a config
        # object.

        # Returns a dictionary with the detections.
        objects = detector.predict(image)

        vis_objects(image, objects).save('traffic-out.png')

        return objects