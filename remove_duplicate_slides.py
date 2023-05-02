import sys
import re
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_path
import pytesseract
from tqdm import tqdm
import argparse

def get_slide_number(image):
    w, h = image.size
    cropped_image = image.crop((w*0.8, h*0.9, w, h))
    text = pytesseract.image_to_string(cropped_image, lang='eng', config='--psm 6')
    slide_number = re.search(r'slide (\d+)', text, re.IGNORECASE)
    return int(slide_number.group(1)) if slide_number else None

def remove_duplicate_slides(pdf_path, keep_first_page):
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    current_slide_number = 0
    last_slide_indices = {}
    if keep_first_page:
        pdf_writer.add_page(pdf_reader.pages[0])
    for page in tqdm(range(1 if keep_first_page else 0, len(pdf_reader.pages))):
        temp_images = convert_from_path(pdf_path, first_page=page+1, last_page=page+1)
        slide_number = get_slide_number(temp_images[0])
        if slide_number is not None and slide_number > current_slide_number:
            current_slide_number = slide_number
            last_slide_indices[current_slide_number] = page
        elif slide_number is not None and slide_number == current_slide_number:
            last_slide_indices[current_slide_number] = page

    for index in sorted(last_slide_indices.values()):
        pdf_writer.add_page(pdf_reader.pages[index])

    output_pdf_path = 'output_' + pdf_path
    with open(output_pdf_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Processed PDF saved as: {output_pdf_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove duplicate slides from a PDF file.')
    parser.add_argument('pdf_path', type=str, help='Path to the input PDF file.')
    parser.add_argument('--keep_first_page', action='store_true', help='Keep the first page of the PDF.')
    args = parser.parse_args()

    remove_duplicate_slides(args.pdf_path, args.keep_first_page)
