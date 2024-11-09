# we generate html from the book and save it to a file
# we generate a single page html 
# we show images and add text annotations over the images
# we show a single page at a time
# we show controls to navigate to the next and previous page

#%pip install pytesseract
#%pip install tesseract-ocr
#%pip install opencv-python
#%pip install numpy
#%pip install Pillow

import os
import PIL
import numpy as np
# html template library
from string import Template
import json


def generate_annotation_word(word):
    """Generates the html for the annotation of a word."""
    
    word_annotation = """
        <div class="word" style="position: absolute; top: $y; left: $x; width: $w; height: $h">
            $text
        </div>
        """
    
    # we load the html template
    template = Template(word_annotation)

    # we generate the html
    html = template.substitute(
        x=str(word['x']) + 'px',
        y=str(word['y']) + 'px',
        w=str(word['w']) + 'px',
        h=str(word['h']) + 'px',
        text=word['text']
    )

    return html

def generate_annotation_line(line):
    """Generates the html for the annotation of a line."""
    # multi line html template
    line_annotation = """
        <div class="line" id="$line_index"
            style="font-size: $font_size; line-height: $line_height; opacity: 0.1; position: absolute; top: $top; left: $left; width: $width; height: $height"
            >
            $words
        </div>
        """

    # we load the html template
    template = Template(line_annotation)

    words = ''
    for word in line['words'].values():
        words += generate_annotation_word(word)

    # we generate the html
    html = template.substitute(
        line_index=line['line_index'],
        top=str(line['top']) + 'px',
        left=str(line['left']) + 'px',
        width=str(line['width']) + 'px',
        height=str(line['height']) + 'px',
        words=line['text'],
        font_size=str(1.25 * line['font_size']) + 'px',
        line_height=str(1.7 * line['font_size']) + 'px'
    )

    return html

# html fragment for a single page
def generate_page(page):
    """Generates a single page html from the given page data."""
    
    page_annotation = """
        <div class="page${active}" id="$page_index"
            style="position: relative; top: 0; left: 0; width: 100%; height: 100%"
            >
            <img src="out/$image_name" alt="$text" z-index="-1" >
            $lines
        </div>
        """

    # we load the html template
    template = Template(page_annotation)

    lines = ''
    for line in page['lines'].values():
        lines += generate_annotation_line(line)

    # we generate the html
    html = template.substitute(
        page_index=page['page_index'],
        image_name=page['image_name'],
        text=page['text'],
        lines=lines,
        active='.active' if page['page_index'] == 0 else ''
    )

    return html

def generate_book(book):
    """Generates the html for the book."""
    
    book_template = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <link rel="stylesheet" href="style.css">
            <!-- script to navigate pages -->
            <style>
                .page {
                    display: none;
                }
                .page.active {
                    display: block;
                }
            </style>
            <script>
                var currentPageIndex = '';
                function changePage(currentPage, nextPage) {
                    if (nextPage) {
                        currentPage.classList.replace('page.active', 'page');
                        nextPage.classList.replace('page', 'page.active');
                        currentPageIndex = nextPage.id;
                    }
                }

                function nextPage() {
                    var currentPage = document.getElementsByClassName('page.active')[0];
                    var nextPage = currentPage.nextElementSibling;
                    changePage(currentPage, nextPage);
                }

                function previousPage() {
                    var currentPage = document.getElementsByClassName('page.active')[0];
                    var previousPage = currentPage.previousElementSibling;
                    changePage(currentPage, previousPage);
                }

                

                function keyPress(e){
                    var x = e.keyCode;
                    if (x == 37) {
                        previousPage();
                    } else if (x == 39) {
                        nextPage();
                    }
                    // show all pages with 'p'
                    else if (x == 80) {
                        var pages = document.getElementsByClassName('page');
                        for (var i = 0; i < pages.length; i++) {
                            pages[i].classList.replace('page', 'page.active');
                        }
                    }
                    // hide all pages with 'h' except the current page
                    else if (x == 72) {
                        var pages = document.getElementsByClassName('page.active');
                        for (var i = 0; i < pages.length; i++) {
                            if (pages[i].id != currentPageIndex) {
                                pages[i].classList.replace('page.active', 'page');
                            }  
                        }
                    }


                }

                document.onkeydown = keyPress
                    
            </script>
        </head>
        <body>
            <div class="book">
                $pages
            </div>
            <div class="controls">
                <button onclick="previousPage()">Previous</button>
                <button onclick="nextPage()">Next</button>
            </div>
        </body>
    </html>
    """


    # we load the html template
    template = Template(book_template)

    pages = ''
    for page in book['pages'].values():
        pages += generate_page(page)

    # we generate the html
    html = template.substitute(
        pages=pages
    )

    return html


# load the book
book = json.load(open('out/book.json'))

# generate the html
html = generate_book(book)

# save the html to a file as utf-8
with open('out/book.html', 'w', encoding='utf-8') as f:
    f.write(html)

