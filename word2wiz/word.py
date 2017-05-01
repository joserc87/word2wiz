#!/usr/bin/python

import re
from docx import Document


def analyse_doc(docx_file):
    document = Document(docx_file)

    questions = []
    for p in document.paragraphs:
        questions += re.findall('(?:«|<<)([^(>>|»)]*)(?:»|>>)', p.text)
    return questions
