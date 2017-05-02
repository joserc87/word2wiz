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
from .spell_helper import LineControl, CheckboxControl


def get_field_txt(control):
    if isinstance(control, LineControl):
        return ''
    elif isinstance(control, CheckboxControl):
        return control.question or control.label or ''
    else:
        return control.question or control.default_value or ''


def generate_report(steps):
    report = ''
    # Lengths of the step name, field and metadata, for formatting purposes
    max_step_length = max([len(step.name) for step in steps])
    max_field_length = max([max([len(get_field_txt(control))
                                 for control in step.controls])
                            for step in steps])
    max_metadata_length = max([max([len(control.metadata_name or '')
                                    for control in step.controls])
                               for step in steps])
    max_step_length = max(max_step_length, len('STEP'))
    max_field_length = max(max_field_length, len('FIELD'))
    max_metadata_length = max(max_metadata_length, len('METADATA'))
    # Heading:
    heading = '| {0} | {1} | {2} |\n'.format(
        'STEP'.center(max_step_length),
        'FIELD'.center(max_field_length),
        'METADATA'.center(max_metadata_length))
    # Divider:
    divider = '+-{0}-+-{1}-+-{2}-+\n'.format(
        '-'*max_step_length, '-'*max_field_length, '-'*max_metadata_length)
    report = divider + heading + divider
    for step in steps:
        step_name = step.name or ''
        for control in step.controls:
            field = get_field_txt(control)
            metadata = control.metadata_name or ''

            # Add a new row
            if isinstance(control, LineControl):
                report += '| {0} +-{1}-+-{2}-+\n'.format(
                    step_name.ljust(max_step_length),
                    '-'*max_field_length,
                    '-'*max_metadata_length)
            else:
                report += '| {0} | {1} | {2} |\n'.format(
                    step_name.ljust(max_step_length),
                    field.ljust(max_field_length),
                    metadata.ljust(max_metadata_length))

            # Only show the step name on the first row
            step_name = ''
        # Add a divider between steps
        report += divider
    return report


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
