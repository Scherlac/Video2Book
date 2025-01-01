# we will find the text paragraphs on the image and extract them using pytesseract
#%pip install pytesseract

import os
import PIL
import numpy as np
import pytesseract
from pytesseract import Output
import json
import re

# Add the path of Tesseract to the environment variables
os.environ['PATH'] += ';C:\\Program Files\\Tesseract-OCR'


def read_book(path, book_file, lang='eng'):
    """Reads the book from the given path and stores it in the given file name."""

    # We load the images from the out folder with the jpg extension
    files = os.listdir(path)
    files = [file for file in files if file.endswith('.jpg')]
    files.sort()

    # we create a data structure to store image_to_data output hierarchically structured as follows:
    # document -> page -> block -> paragraph -> line -> word 
    # we will use a list to store the data
    book = {
        'title': '',
        'pages': {}
    }

   
    # We loop through the images and track the index
    for page_index, file in enumerate(files):

        # load the image
        image = PIL.Image.open(os.path.join(path, file))

        # we convert the image to numpy array
        np_image = np.array(image)

        # we get the text from the image as annotation data
        data = pytesseract.image_to_data(np_image, output_type=Output.DICT)

        # we ned hungarian language for the OCR
        # we get the text from the image
        page_text = pytesseract.image_to_string(np_image, lang=lang)

        # we add the page to the book
        page = book['pages'].get(page_index, None)
        if page is None:
            page = {
                'page_index': page_index, 
                'text': page_text, 
                'lines': {},
                'image_name': file }
            book['pages'][page_index] = page


        for j in range(len(data['text'])):

            line_index = f'b{data["block_num"][j]:03d}-p{data["par_num"][j]:03d}'  
            word_index = f'l{data["line_num"][j]:03d}-w{data["word_num"][j]:03d}'
            text = data['text'][j]
            x = data['left'][j]
            y = data['top'][j]
            w = data['width'][j]
            h = data['height'][j]

            # we create a dictionary to store the text and the coordinates
            word = {
                'word_index': word_index,
                'text': text, 
                'x': x, 'y': y, 
                'w': w, 'h': h
                }

            line = page['lines'].get(line_index, None)
            if line is None:
                line = {
                    'line_index': line_index, 
                    'text': '',
                    'words': {},
                    'boundaries': {
                        'min_x': x,
                        'min_y': y,
                        'max_x': x + w,
                        'max_y': y + h,
                        'height': len(text) * h,
                        'norm': len(text)
                        },
                    }
                page['lines'][line_index] = line

            line['words'][word_index] = word
            line['text'] += text + ' '

            boundaries = line['boundaries']

            boundaries['min_x'] = min(boundaries['min_x'], x)
            boundaries['min_y'] = min(boundaries['min_y'], y)
            boundaries['max_x'] = max(boundaries['max_x'], x + w)
            boundaries['max_y'] = max(boundaries['max_y'], y + h)
            boundaries['height'] += len(text) * h
            boundaries['norm'] += len(text)


        # convert word coordinates relative to the line
        for line_index, line in page['lines'].items():

            # we need to update the line coordinates
            boundaries = line['boundaries']

            line['left'] = boundaries['min_x']
            line['top'] = boundaries['min_y']
            line['width'] = boundaries['max_x'] - boundaries['min_x']
            line['height'] = boundaries['max_y'] - boundaries['min_y']
            line['font_size'] = boundaries['height'] / boundaries['norm'] if boundaries['norm'] > 3 else 12

            # we need to update the word coordinates
            for word in line['words'].values():
                word['x'] -= line['left']
                word['y'] -= line['top']

            # normalize text
            line['text'] = line['text'].strip()

            #replace multiple spaces with single space with regex
            line['text'] = re.sub('\s+', ' ', line['text'])

    # write book to file
    with open(book_file, 'w') as f:
        # we write the book to the file indented with 4 spaces
        json.dump(book, f, indent=4)

    return book

