import os
import sys
import time
import datetime
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import PIL
from string import Template
import json
from fpdf import FPDF
from PIL import Image

import mp4toimages
import images2pdf
import images2json
import json2html


# main function
def main():
    """The main function of the program."""

    # we get the mp4 file path from the command line
    path = sys.argv[1]

    # manual crop values
    # TODO: automate the crop values and/or make them configurable
    crop_x = None # [80, 900]
    crop_y = None # [40, 1070]

    # we get the name of the video file
    file_name = os.path.basename(path)

    name = os.path.splitext(file_name)[0]

    # folder of teh video file
    folder = os.path.dirname(path)

    # output folder
    out_folder = os.path.join(folder, name)

    # ensure the output folder exists
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    # raw image folder name
    raw_image_folder =  os.path.join(folder, name, "raw")

    # ensure the raw image folder exists
    if not os.path.exists(raw_image_folder):
        os.makedirs(raw_image_folder)

    # image folder name
    image_folder =  os.path.join(folder, name, "out")

    # ensure the image folder exists
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # we convert the mp4 file to images
    mp4toimages.mp4toimages(path, raw_image_folder)

    

    # crop the images
    images2pdf.crop_images(raw_image_folder, image_folder, crop_x, crop_y)

    # the pdf file
    pdf_file = os.path.join(out_folder, f"{name}.pdf")

    # we convert the images to pdf
    images2pdf.images2pdf(image_folder, pdf_file)

    # the book json file
    book_file = os.path.join(out_folder, f"{name}.json")

    # we read the book from the images
    book = images2json.read_book(image_folder, book_file, lang='eng')

    # we generate html from the book and save it to a file
    json2html.generate_html(image_folder, book_file)

    
