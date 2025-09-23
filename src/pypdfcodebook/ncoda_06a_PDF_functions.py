import csv
from fpdf import FPDF, TitleStyle

"""
Help to make Codebook PDF
https://pyfpdf.github.io/fpdf2/Tutorial.html#tuto-5-creating-tables
https://github.com/bvalgard/create-pdf-with-python-fpdf2

# Code for fpdf
https://github.com/PyFPDF/fpdf2/blob/master/fpdf/fpdf.py
# Docs for fpdf
https://pyfpdf.github.io/fpdf2/index.html

RGB color codes
https://www.rapidtables.com/web/color/RGB_Color.html

Possible alternative to fpdf
https://github.com/jorisschellekens/borb
"""

class PDF(FPDF):
    def __init__(self,
            header_text: str = "Header Text",
            footer_text: str = "Footer Text",
            image_path:  str = ""):
        super().__init__(orientation = "P", unit = "mm", format = "letter")
        self.header_text = header_text
        self.footer_text = footer_text
        self.image_path = image_path
    def header(self):
        # ...existing code...
        pass
