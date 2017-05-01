#!/usr/bin/python

import re
from docx import Document


def analyse_doc(docx_file):
    document = Document(docx_file)

    marks = [
        ('«', '»'),
        ('<<', '>>')
    ]

    # Regex parts for the delimiters
    start_dels, end_dels = ('|'.join(m[i] for m in marks)
                            for i in [0, 1])
    # Regex to find the questions
    regex = '(?:{0})([^({1})]*)(?:{1})'.format(start_dels, end_dels)

    questions = []
    for p in document.paragraphs:
        questions += re.findall(regex, p.text)
    return questions
