# Remove Duplicate slides
This simple python program removes slides that are duplicates in a presentation pdf. It is useful for lecture presentations where content is shown sequentially (bullet points, etc.) and the presenter has to go back to a previous slide to show something again. This program removes the duplicate slides and keeps only the last instance of the slide.

## How it works
The program uses the pdf2image library to convert the pdf to images. It then uses the tesseract library to perform optical character recognition (OCR) on the images. The OCR results are then compared to determine if the slides are duplicates. The program then uses the PyPDF2 library to create a new pdf with the duplicate slides removed.

The OCR only checks the bottom right corner of the slide. This is because the slide number is usually located there. If the slide number is the same as the previous slide, then the slide is considered a duplicate. You can change the params of how much of the image the OCR looks at in the code (looking at less of the image will make the program run faster but may not work as well).

## Installation
### Python dependencies
Python requirements
```
pip install -r requirements.txt
```

### Mac OS
Libraries for pdf and ocr:
```
brew install poppler
brew install tesseract
```

### Linux
Libraries for pdf and ocr:
```
sudo apt-get install poppler-utils
sudo apt-get install tesseract-ocr
```

### Windows
Libraries for pdf and ocr:
```
choco install poppler
choco install tesseract
```

## Usage
```
python remove_duplicate_slides.py <input_pdf_file> [--include-unrecognised-pages] [--keep-first-page]
```
The program will create a new pdf file with the duplicate slides removed. The new pdf file will be named `output_<input_pdf_file>.pdf`.

Options:
* `--keep-first-page`: Keep the first page of the pdf. This is useful if the first page is a title page or something that you want to keep.
* `--include-unrecognised-pages`: Include pages that could not be recognised by OCR. This is useful if you have slides that are images or have no text.