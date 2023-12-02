# we will load each jpg file from the out folder and convert it to pdf
#%pip install fpdf
#%pip install Pillow


import os
import sys
from PIL import Image
from fpdf import FPDF

# we create a pdf object
pdf = FPDF()

# we set the unit to mm
pdf.unit = 'mm'

# we select the format of the pdf page
pdf_size = 'A4'

# we set the font for the page number
pdf.set_font('Arial', 'B', 12)
pdf.set_text_color(0, 0, 0)

# we get the list of files in the out folder
files = os.listdir('out')

# we sort the files
files.sort()

# we loop through the files the first 10 page of the pdf
for file in files: # [:10]:
    # we open the image
    image = Image.open('out/' + file)
    # we get the size of the image
    width, height = image.size

    ratio = width / height

    # detect DPI of the image
    # dpi = image.info['dpi']
    # we convert the dpi to mm
    # width = width * 25.4 / dpi[0]
    # height = height * 25.4 / dpi[1]

    # we create a new pdf page
    pdf.add_page()
    # we add the image to the pdf to fit the page with 15mm margin on left, right, top
    top_offset = 15
    left_offset = 15
    page_width = 210
    page_height = 297
    width = page_width - left_offset * 2
    height = width / ratio

    pdf.image('out/' + file, 15, top_offset, width, height)

    # add page number to the middle bottom of the page
    pdf.set_xy(0, page_height - 40)
    pdf.cell(page_width, 10, str(pdf.page_no()), False, 0, 'C')


# we save the pdf
pdf.output('out.pdf', 'F')

