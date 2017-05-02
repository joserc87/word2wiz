import os
import argparse
from word2wiz import word2wiz
from .version import __version__


def isdoc(filepath):
    f = filepath.lower()
    return f.endswith('.docx') or f.endswith('.doc')


def get_files(args):
    files = []
    for input_file in args.input_files:
        if os.path.isfile(input_file):
            files += [input_file]
        elif os.path.isdir(input_file):
            root, dirs, dir_files = next(os.walk(input_file))
            files += [os.path.join(root, f) for f in dir_files if isdoc(f)]
    return files


def convert_single(path, args):
    """
    Run the tool for one single file
    """
    spell, report = word2wiz.word2wiz(path)

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


def convert_batch(paths, args):
    """
    Run the tool for multiple files
    """
    for path in paths:
        print('Converting {0}'.format(path))
        spell, report = word2wiz.word2wiz(path)

        path_base, _ = os.path.splitext(path)
        filename = os.path.basename(path_base)
        if args.output:
            spell_path = os.path.join(args.output, filename + '.spl')
        else:
            spell_path = path_base + '.spl'

        if args.report:
            report_path = os.path.join(args.report, filename + '.txt')
        else:
            report_path = path_base + '.txt'

        # Write the spell
        with open(spell_path, 'w') as output_file:
            output_file.write(spell)

        # Write the report
        with open(report_path, 'w') as report_file:
            report_file.write(report)


def main():
    description = 'Create a spell configuration from a Microsoft Word document'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('input_files',
                        metavar='FILES',
                        nargs='+',
                        help='the input word document')

    parser.add_argument('-o', '--output',
                        help='the file for the output spell (stdout by default)'
                        )

    parser.add_argument('--report',
                        help='the ouput report file containing the fields and' +
                        'the metadatas they are linked to')

    parser.add_argument('-v', '--version',
                        help='prints the version',
                        action='version',
                        version='%(prog)s ' + __version__)

    # Parse
    args = parser.parse_args()

    # Files to convert
    files = get_files(args)

    # Run
    if len(files) == 1:
        convert_single(files[0], args)
    else:
        convert_batch(files, args)
