from src.convertPdf import ConvertPdf
from src.detector import Detection
from src.fileHelper import FileHelper
from src.helper import Helper
from src.ocr import OcrConverter
from src.preprocessor import Preprocessor
import sys
import re
import PyPDF2
import cv2
import pytesseract
from pdf2image import convert_from_path
import shutil
from luminoth import Detector, read_image, vis_objects
import xlwt
from src.fileHelper import FileHelper
from src.helper import Helper
import os



def main():

    if len(sys.argv) < 2:
        Helper.print("Too few arguments given. Use -help to get help.")
        return

    if len(sys.argv) > 3:
        Helper.print("Too many arguments given. Use -help to get help.")
        return

    input_path_string = sys.argv[1]

    if input_path_string == "-help":
        Helper.print("Following arguments are required:")
        Helper.print("[0] absolute path to source folder")
        Helper.print("[1] absolute path to output folder")
        Helper.print("Example: \"C:\\temp\\data\\input\" \"C:\\temp\\data\\output\"")
        return

    output_path_string = sys.argv[2]

    Helper.blockPrint()
    # declare folder paths
    root_dir = os.path.abspath(os.sep)
    root = os.path.join(root_dir, "temp", "TabExImg")
    FileHelper.createPathIfNotExisting(root)
    input_path = input_path_string  # multiple scanned PDFs
    FileHelper.createPathIfNotExisting(input_path)
    pdf_images_path = os.path.join(root, "01_pdf_images")  # multiple scanned PDFs
    FileHelper.createPathIfNotExisting(pdf_images_path)
    preprocessed_images_path = os.path.join(root, "02_preprocessed_images")  # folder per pdf | preprocessed images
    FileHelper.createPathIfNotExisting(preprocessed_images_path)
    treated_pdfs_path = os.path.join(root, "03_treated_pdfs")
    FileHelper.createPathIfNotExisting(treated_pdfs_path)
    output_path = output_path_string
    FileHelper.createPathIfNotExisting(output_path)
    output_boundaries_path = os.path.join(output_path, "excel")
    FileHelper.createPathIfNotExisting(output_boundaries_path)
    output_pdf_path = os.path.join(output_path, "pdf")
    FileHelper.createPathIfNotExisting(output_pdf_path)

    # delete eventually still existing old files (01_pdf_images, 02_preprocessed_images, 03_treated_pdfs)
    Helper.print("Precautionary delete files of previous runs...")
    FileHelper.deleteAllFilesInFolder(pdf_images_path)
    FileHelper.deleteAllFilesInFolder(preprocessed_images_path)
    FileHelper.deleteAllFilesInFolder(treated_pdfs_path)

    # convert PDFs to images
    pdfConverter = ConvertPdf(input_path, pdf_images_path)
    pdfConverter.convertPdfs()

    # preprocess image files
    preprocessor = Preprocessor(input_path, pdf_images_path, preprocessed_images_path, treated_pdfs_path)
    preprocessor.execute()

    # move original PDFs to backup folder
    FileHelper.moveFiles(input_path, treated_pdfs_path)

    # detect table boundaries
    detection = Detection(preprocessed_images_path, output_path, output_boundaries_path, output_pdf_path)
    detection.detectTableBoundaries()

    # combine files
    Helper.print("Start Opitcal Character Recognition...")
    Helper.print("This can take some time...")
    ocrConverter = OcrConverter()
    ocrConverter.convertAllImagesToPdfs(pdf_images_path, output_pdf_path)
    ocrConverter.combinePdfs(output_pdf_path)
    Helper.print("Opitcal Character Recognition done...")

    Helper.print("Start cleanup temporary files...")
    # delete old files (01_pdf_images, 02_preprocessed_images, 03_treated_pdfs)
    FileHelper.deleteAllFilesInFolder(pdf_images_path)
    FileHelper.deleteAllFilesInFolder(preprocessed_images_path)
    FileHelper.deleteAllFilesInFolder(treated_pdfs_path)
    Helper.print("Cleanup done...")
    Helper.print("Table Detection Done")
    Helper.print("Result Files in " + output_path)

if __name__ == '__main__':
    main()