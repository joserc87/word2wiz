#!/usr/bin/python
"""
Reads a word document (docx format) and generates a spell based on the markers
found in the document. The spell is printed on the standard output by default
"""

import argparse
from os.path import basename, splitext, dirname, realpath, join

from jinja2 import Environment, FileSystemLoader

from .config import Config
from . import word
from . import mark_parser
from .spell_helper import LineControl, ListControl, CheckboxControl


def get_field_txt(control):
    if isinstance(control, LineControl):
        return ''
    elif isinstance(control, CheckboxControl):
        return control.question or control.label or ''
    else:
        return control.question or control.default_value or ''

def get_field_options(control):
    if isinstance(control, ListControl):
        return ' | '.join(control.values)
    elif isinstance(control, CheckboxControl):
        return ' | '.join(['True', 'False'])
    return ''


def tabularize(columns, rows):
    """
    Formats data like a table
    """

    # Find the width of the columns
    col_lens = [l for l in map(len, columns)]
    for row in rows:
        if isinstance(row, list):
            col_lens = [max(col_lens[i], len(row[i])) for i in range(len(row))]

    # Print heading
    divider = '+-{0}-+'.format('-+-'.join(['-'*l for l in col_lens]))
    semidivider = '| {0} +-{1}-+'.format(
        ' '*col_lens[0],
        '-+-'.join(['-'*l for l in col_lens[1:]]))
    columns = [name.center(width) for name, width in zip(columns, col_lens)]
    heading = '| {0} |'.format(' | '.join(columns))

    # Print data for row in
    report = [divider] + [heading] + [divider]
    for row in rows:
        if row == 'divider':
            report += [divider]
        elif row == 'semidivider':
            report += [semidivider]
        else:
            row = [name.ljust(width) for name, width in zip(row, col_lens)]
            report += ['| {0} |'.format(' | '.join(row))]

    # Separate the lines of the report by line feeds.
    return '\r\n'.join(report) + '\r\n'


def generate_report(steps):
    data = []

    col_names = ['STEP',
                 'FIELD',
                 'METADATA',
                 'OPTIONS']

    for step in steps:
        row = []
        step_name = step.name or ''
        for control in step.controls:
            field = get_field_txt(control)
            metadata = control.metadata_name or ''
            options = get_field_options(control)

            if isinstance(control, LineControl):
                row = 'semidivider'
            else:
                row = [step_name,
                       field,
                       metadata,
                       options]

            data += [row]
            # Only show the step name on the first row
            step_name = ''
        data += ['divider']

    return tabularize(col_names, data)


def word2wiz(path):
    # Jinja2
    current_dir = dirname(realpath(__file__))
    spell_dir = join(current_dir, 'spell')
    env = Environment(loader=FileSystemLoader(spell_dir),
                      trim_blocks=True,
                      lstrip_blocks=True)
    main_template = env.get_template('main.spl')

    # Get all the <<mark>>s from the word document
    marks = word.analyse_doc(path)

    # Take out the marks that are just for the configuration part
    config = Config()
    marks = config.parse_defaults(marks)

    # The steps will have the name of the document
    mark_parser.DEFAULT_STEP_NAME = splitext(basename(path))[0]
    # Parse the marks and get the step-control hierarchy
    steps = mark_parser.get_steps(marks)

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
                                 steps=steps)
    report = generate_report(steps)

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
