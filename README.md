# Video2Book

This is a simple tool to convert a video to a book. It uses the opencv library to extract frames from the video and the pytesseract library to extract text from the frames. The extracted images are then combined into a pdf file. The extracted text is then saved to a html file.

## Installation

1. Ensure you have Python 3.10+ installed.

2. Activate the virtual environment:
```bash
source ~/code/.venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR (required for text extraction):
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng
```

5. (Optional) If using conda instead of venv, you can create the environment with:
```bash
conda env create -f env.yml
conda activate video2book
```

## Usage

```bash
python -m bookutils.py --file <video_file> [--crop-x crop_x1 crop_x2] [--crop-y crop_y1 crop_y2] [--lang <language>]
```

## TODO

- [ ] Add support for multi threading on the text extraction
- [ ] Add progress bar for the processing steps (image extraction, image cropping, pdf creation, text extraction)
- [ ] Improve the html reader to better align the text on the image
- [ ] Extract diagams from the images
- [ ] Skip diagrams when extracting text
- [ ] Create html with formated text and diagrams instead of just images with aligned texts
- [ ] Fix crop auto detection 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

