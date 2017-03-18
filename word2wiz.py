#!/usr/bin/python

import sys
from os.path import basename, splitext
import word
from config import Config
from jinja2 import Environment, FileSystemLoader

class Control:
    def __init__(self, string):
        # Get the desired control type from the string
        if string.startswith('list '):
            self.type = 'list'
            parts = string.split(';')
            self.question = parts[0][len('list '):]
            self.values = parts[1:]
        elif string.startswith('checkbox '):
            self.type = 'checkbox'
            parts = string.split(';')
            self.question = parts[0][len('checkbox '):]
            self.label = parts[-1]
        elif string.startswith('line'):
            # used to output a line between questions (it's just a label)
            self.type = 'line'
        else:
            # Otherwise it's a string control
            self.type = 'string'
            self.question = string

def word2wiz(path):
    # Jinja2
    env = Environment(loader=FileSystemLoader('templates'),
                      trim_blocks=True,
                      lstrip_blocks=True)
    main_template = env.get_template('main.spl')

    # Get all the <<question>>s from the word document
    questions = word.analyse_doc(path)
    # Take the questions that are just for the configuration part
    config = Config()
    questions = config.parse_defaults(questions)
    # Transform the rest of the questions in controls
    controls = [Control(q) for q in questions]
    # Medewerkers for step 1 (name, last name, function)
    medewerkers = [
        ('Margot',    'Smits',       'Senior medisch adviseur'),
        ('Wendy',     'Haanschoten', 'Adviserend apotheker'),
        ('Marjolein', 'Rijkeboer',   'Adviserend psycholoog'),
        ('Herman',    'Flens',       'Medisch adviseur'),
        ('Job',       'van Huizen',  'Medisch adviseur')]
    medischecategorie = [
        'Medisch Polis',
        'Medisch Machtiging',
        'Medisch Declaratie',
        'Medisch Declaratie Dossier',
        'Medisch Zorgbemiddel',
        'Medisch Verhaal',
        'Medisch AWBZ',
        'Medisch Arbo',
        'Polis',
        'Standaard',
        'Marketing',
        'Financieel']
    return main_template.render(doc_name=splitext(basename(path))[0],
                                config=config,
                                medewerkers=medewerkers,
                                medischecategorie=medischecategorie,
                                controls=controls)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Wrong number of arguments.')
        print('Usage: python main.py INPUT_FILE.docx')
    else:
        print(word2wiz(sys.argv[1]))
