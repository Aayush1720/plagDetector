import os
import docx2txt as d2t
import PyPDF2
import re
import string


class document_parser:
    def __init__(self, document):
        ext = document.split(".")[-1]
        if ext == 'pdf':
            self.text = self.pdf2str(document)
        elif ext in ['doc', 'docx']:
            self.text = self.doc2str(document)
        elif ext == '.txt':
            self.text = self.txt2str(document)

    def pdf2str(self, document):
        pdfFileObj = open(document, 'rb')
        # Read file
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # Get total number of pages
        num_pages = pdfReader.numPages
        # Initialize a count for the number of pages
        count = 0
        # Initialize a text empty etring variable
        text = ""
        # Extract text from every page on the file
        while count < num_pages:
            pageObj = pdfReader.getPage(count)
            count += 1
            text += pageObj.extractText()

        pdfFileObj.close()
        return text

    def doc2str(self, document):
        return d2t.process(document, '/')

    def txt2str(self, document):
        return ""

    def get_content(self):
        return self.text
