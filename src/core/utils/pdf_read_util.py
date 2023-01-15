import os
from typing import Dict
import fitz


def read_native_pdf(pdf_file_path: str, roi_dict: dict = None) -> Dict:
    # Method to read text in a pdf using the fitz module
    if os.path.exists(pdf_file_path):

        document = fitz.open(pdf_file_path)
        text_dict = {}
        # read each page of the document
        for page_index, page in enumerate(document):
            text_dict[page_index] = [block_info[4] for block_info in page.get_text("blocks") if
                                     len(block_info[4].strip()) > 0]

        return text_dict

    else:
        print("File not found - {}".format(pdf_file_path))
