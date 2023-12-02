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
import images2json
import json2images


# main function
def main():
    """The main function of the program."""

    # we get the mp4 file path from the command line
    path = sys.argv[1]
    
    # we get the name of the video file
    file_name = os.path.basename(path)

    # folder of teh video file
    folder = os.path.dirname(path)

    # image folder name
    image_folder = folder + '/' + 'out'

    # we create the out folder if it does not exist
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # we convert the mp4 file to images
    mp4toimages.mp4toimages(path, image_folder)

    # we read the book from the images
    book = images2json.read_book(image_folder, file_name)

    # we generate html from the book and save it to a file
    json2images.generate_html(book, image_folder)

    
