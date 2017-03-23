#!/usr/bin/python

import sys
from collections import OrderedDict
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


def remove_unwanted_matches(questions, file_path='data/unwanted_matches.txt'):
    """
    Loads the unwanted matches from unwanted_matches.txt (by default), and
    returns a list with the questions that do not match.
    Args:
        questions(list): A list of strings with all the matches
        file_path(str): Optional. The file that contains the unwanted matches.
    Returns:
        The input list minus the questions that are in the unwanted_matches.txt.
    """
    filtered_questions = questions
    with open(file_path) as f:
        for unwanted_match in f.read().splitlines():
            if unwanted_match in filtered_questions:
                filtered_questions.remove(unwanted_match)
    return filtered_questions


def word2wiz(path):
    # Jinja2
    env = Environment(loader=FileSystemLoader('spell'),
                      trim_blocks=True,
                      lstrip_blocks=True)
    main_template = env.get_template('main.spl')

    # Get all the <<question>>s from the word document
    questions = word.analyse_doc(path)
    # Take out the questions that are just for the configuration part
    config = Config()
    questions = config.parse_defaults(questions)
    # Filter out unwanted matches
    questions = remove_unwanted_matches(questions)
    # Remove duplicates
    questions = list(OrderedDict.fromkeys(questions))
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
