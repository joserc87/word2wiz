#!/usr/bin/python
"""
Reads a word document (docx format) and generates a spell based on the markers
found in the document. The spell is printed on the standard output by default
"""

import argparse
from os.path import basename, splitext

from jinja2 import Environment, FileSystemLoader

from config import Config
import word
import mark_parser


class Control:
    def __init__(self, string):
        self.original_string = string
        self.metadata_name = None
        # Get the desired control type from the string
        if string.startswith('list '):
            self.type = 'list'
            parts = string.split(';')
            self.question = parts[0][len('list'):].strip()
            self.values = [val.strip() for val in parts[1:]]
        elif string.startswith('checkbox '):
            self.type = 'checkbox'
            parts = string.split(';')
            self.question = parts[0][len('checkbox'):].strip()
            self.label = parts[-1].strip()
        elif string.startswith('line'):
            # used to output a line between questions (it's just a label)
            self.type = 'line'
        else:
            # Otherwise it's a string control
            self.type = 'string'
            self.question = string.strip()


def create_controls(questions):
    # Transform the rest of the questions in controls
    controls = [Control(q) for q in questions]
    # Assign metadatas to controls
    for i, control in enumerate(controls):
        control.metadata_name = 'txt_{:03d}'.format(i + 1)
    return controls


def word2wiz(path):
    # Jinja2
    env = Environment(loader=FileSystemLoader('spell'),
                      trim_blocks=True,
                      lstrip_blocks=True)
    main_template = env.get_template('main.spl')

    # Get all the <<mark>>s from the word document
    marks = word.analyse_doc(path)
    # Take out the marks that are just for the configuration part
    config = Config()
    marks = config.parse_defaults(marks)
    # Remove unwanted matches, duplicates, spaces, etc
    marks = mark_parser.preprocess_marks(marks)
    controls = create_controls(marks)
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
    spell = main_template.render(doc_name=splitext(basename(path))[0],
                                 config=config,
                                 medewerkers=medewerkers,
                                 medischecategorie=medischecategorie,
                                 controls=controls)
    report = '\n'.join(['VELD: {0} >> METADATANAAM: {1}'.format(
        control.original_string,
        control.metadata_name) for control in controls])

    return (spell, report)


def main():
    description = 'Create a spell configuration from a Microsoft Word document'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('input_file',
                        nargs=1,
                        metavar='FILE',
                        help='the input word document')

    parser.add_argument('-o', '--output',
                        help='the file for the output spell (stdout by default)'
                        )

    parser.add_argument('--report',
                        help='the ouput report file containing the fields and' +
                        'the metadatas they are linked to')
    # Parse
    args = parser.parse_args()

    # Run
    spell, report = word2wiz(args.input_file[0])

    if args.output:
        # Write the spell
        with open(args.output, 'w') as output_file:
            output_file.write(spell)
    else:
        # By default, print the spell on the stdout
        print(spell)

    if args.report:
        # Write the report
        with open(args.report, 'w') as report_file:
            report_file.write(report)
    elif args.output:
        # Only print the report if the spell hasn't been printed
        print(report)


if __name__ == "__main__":
    main()
