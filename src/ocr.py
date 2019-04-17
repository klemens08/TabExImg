import os
import re
import PyPDF2
import cv2
import pytesseract

from src.fileHelper import FileHelper

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


class OcrConverter:

    image_folder_set = set()

    def convertAllImagesToPdfs(self, base_source_folder, output_folder):
        for dir_ in os.listdir(base_source_folder):
            self.image_folder_set.add(dir_)

        for folder in self.image_folder_set:
            self.createPdfFromImages(base_source_folder, folder, output_folder)

    def createPdfFromImages(self, base_source_folder, parent_folder, output_folder):
        absolute_parent_folder_path = os.path.join(base_source_folder, parent_folder)
        images = FileHelper.getAllFilesInFolder(absolute_parent_folder_path)
        pdf_path = os.path.join(output_folder, parent_folder)# + ".pdf"

        for image in images:
            # Read image from disk
            absolute_image_path = os.path.join(absolute_parent_folder_path, image)

            im = cv2.imread(absolute_image_path, cv2.IMREAD_COLOR)

            #define tesseract config
            config = ('-l eng --oem 1 --psm 3')

            # Run tesseract OCR on image
            #text = pytesseract.image_to_string(im, config=config)

            # create PDF from tesseract OCR results
            pdf = pytesseract.image_to_pdf_or_hocr(im, extension='pdf')
            #f = open("data\\images\\eu-009-page-001.pdf", "w+b")
            f = open(os.path.join(output_folder, os.path.splitext(image)[0]) + ".pdf", "w+b")
            f.write(bytearray(pdf))
            f.close()

            # Print recognized text
            #print(text)

    def combinePdfs(self, output_folder_pdf):

        file_set = set()

        for filename in os.listdir(output_folder_pdf):
            #print(os.path.splitext(filename)[0])
            pdf_name = (os.path.splitext(filename)[0]).rsplit('_', 1)[0]
            print(pdf_name)
            file_set.add(pdf_name)

        for pdf_name in file_set:
            # Get all the PDF filenames
            pdfs2merge_set = []
            for filename in os.listdir(output_folder_pdf):
                if (os.path.splitext(filename)[0]).rsplit('_', 1)[0] == pdf_name:
                    pdfs2merge_set.append(filename)

            pdfs2merge_list_sorted = []
            for pdf_page in pdfs2merge_set:
                 for pdf_page_sorted in pdfs2merge_list_sorted:
                     page_number = int((os.path.splitext(pdf_page)[0]).rsplit('_', 1)[1])
                     curr_sorted_page_number = int((os.path.splitext(pdf_page_sorted)[0]).rsplit('_', 1)[1])
                     if page_number < curr_sorted_page_number:
                         index_to_insert = pdfs2merge_list_sorted.index(pdf_page_sorted)
                         #pdfs2merge_list_sorted[index_to_insert] = pdf_page
                         pdfs2merge_list_sorted.insert(index_to_insert, pdf_page)
                         break
                 if not pdf_page in pdfs2merge_list_sorted:
                     pdfs2merge_list_sorted.append(pdf_page)

            #sorted(pdfs2merge_set, key=lambda a: int(re.search("^.*_(\d*)\..*$", a).group(1)))

            pdfWriter = PyPDF2.PdfFileWriter()

            # loop through all PDFs
            for filename in pdfs2merge_list_sorted:
                absolute_file_path = os.path.join(output_folder_pdf, filename)
                # rb for read binary
                pdfFileObj = open(absolute_file_path, "rb")
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                # Opening each page of the PDF
                for pageNum in range(pdfReader.numPages):
                    pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)
                # save PDF to file, wb for write binary
                pdfOutput = open(os.path.join(output_folder_pdf, pdf_name) +".pdf", "wb")
                # Outputting the PDF
                pdfWriter.write(pdfOutput)
                # Closing the PDF writer
                pdfOutput.close()
                pdfFileObj.close()
                # remove file after combined
                if os.path.exists(absolute_file_path):
                    os.remove(absolute_file_path)
                else:
                    print("The file does not exist")


        #opening or creating pdf file
        # for image in images:
        #     with open(pdf_path + str(image), "wb+") as f:
        #         absolute_image_path = os.path.join(absolute_parent_folder_path, image)
        #         # opening image
        #         image = Image.open(absolute_image_path)
        #
        #         # converting into chunks using img2pdf
        #         pdf_bytes = img2pdf.convert(image.filename)
        #
        #         # writing pdf files with chunks
        #         f.write(pdf_bytes)
        #
        #         # closing image file
        #         image.close()


# if __name__ == '__main__':
#
#     # Read image path from command line
#     #imPath = "C:\Users\Klaymen-Island\PycharmProjects\TabExImg\src\data\images\0148_271.png"
#
#     # Uncomment the line below to provide path to tesseract manually
#     # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
#
#     # Define config parameters.
#     # '-l eng'  for using the English language
#     # '--oem 1' for using LSTM OCR Engine
#     config = ('-l eng --oem 1 --psm 3')
#
#     # Read image from disk
#     root_dir = os.getcwd()
#     root = os.path.join(root_dir, 'data')
#     input_data_path = os.path.join(root, "images")
#     image_path = os.path.join(input_data_path, "eu-009-page-001.jpg")
#
#     im = cv2.imread(image_path, cv2.IMREAD_COLOR)
#
#     # Run tesseract OCR on image
#     text = pytesseract.image_to_string(im, config=config)
#
#     #create PDF from tesseract OCR results
#     pdf = pytesseract.image_to_pdf_or_hocr(im, extension='pdf')
#     f = open("data\\images\\eu-009-page-001.pdf", "w+b")
#     f.write(bytearray(pdf))
#     f.close()
#
#     # Print recognized text
#     print(text)
