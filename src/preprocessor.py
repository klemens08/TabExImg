import os
import cv2

from src.fileHelper import FileHelper
from src.helper import Helper


class Preprocessor:
    input_path = ''
    pdf_images_path = ''
    preprocessed_images_path = ''
    treated_pdfs_path = ''

    image_set = set()

    def __init__(self, input_path, pdf_images_path, preprocessed_images_path, treated_pdfs_path):
        self.input_path = input_path
        self.pdf_images_path = pdf_images_path
        self.preprocessed_images_path = preprocessed_images_path
        self.treated_pdfs_path = treated_pdfs_path

    def execute(self):
        self.fillImageSet(self.pdf_images_path)
        Helper.print("Start preprocessing of images...")
        for image in self.image_set:
            self.processImage(image)
        Helper.print("Preprocessing of images done...")

    def fillImageSet(self, root):
        for dir_, _, files in os.walk(root):
            for file_name in files:
                rel_dir = os.path.relpath(dir_, root)
                rel_file = os.path.join(rel_dir, file_name)
                self.image_set.add(rel_file)

    def processImage(self, image_path):

        absolute_image_path = os.path.join(self.pdf_images_path, image_path)
        transformed_image = self.transformImage(absolute_image_path)

        rel_dir = FileHelper.getRelativeDirPath(absolute_image_path, self.pdf_images_path)

        # write preprocessed file to disk
        self.writePreprocessedFileToDirectory(image_path, transformed_image, rel_dir)

    def transformImage(self, absolute_image_path):
        img = cv2.imread(absolute_image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # perform transformations on image
        b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
        g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
        r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)

        # merge the transformed channels back to an image
        transformed_image = cv2.merge((b, g, r))
        return transformed_image

    def writePreprocessedFileToDirectory(self, image_path, transformed_image, rel_dir):
        preprocessed_file_path = os.path.join(self.preprocessed_images_path, image_path)

        FileHelper.createSubdirectoriesIfNecessary(self.preprocessed_images_path, rel_dir)
        # write preprocessed file to disk
        cv2.imwrite(preprocessed_file_path, transformed_image)




