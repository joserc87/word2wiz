#!/usr/bin/python

import sys
import word
from jinja2 import Environment, FileSystemLoader


def word2wiz(path):
    # Jinja2
    env = Environment(loader=FileSystemLoader('templates'),
                      trim_blocks=True,
                      lstrip_blocks=True)
    main_template = env.get_template('main.spl')

    questions = word.analyse_doc(path)
    medewerkers = [
        ('Margot',    'Smits',       'Senior medisch adviseur'),
        ('Wendy',     'Haanschoten', 'Adviserend apotheker'),
        ('Marjolein', 'Rijkeboer',   'Adviserend psycholoog'),
        ('Herman',    'Flens',       'Medisch adviseur'),
        ('Job',       'van Huizen',  'Medisch adviseur')]
    print(main_template.render(questions=questions,
                               medewerkers=medewerkers))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Wrong number of arguments.')
        print('Usage: python main.py INPUT_FILE.docx')
    else:
        word2wiz(sys.argv[1])
