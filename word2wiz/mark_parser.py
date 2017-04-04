from collections import OrderedDict
import re
from .spell_helper import Step
from .util import parse_mark

DEFAULT_STEP_NAME = 'doc_name'
DEFAULT_STEP_GROUP_NAME = 'Buitenland'


def remove_unwanted_matches(marks, file_path='data/unwanted_matches.txt'):
    """
    Loads the unwanted matches from unwanted_matches.txt (by default), and
    returns a list with the marks that do not match.
    Args:
        marks(list): A list of strings with all the matches
        file_path(str): Optional. The file that contains the unwanted matches.
    Returns:
        The input list minus the marks that are in the unwanted_matches.txt.
    """
    with open(file_path) as f:
        unwanted_matches = [m for m in f.read().splitlines()]
    return [q for q in marks if q not in unwanted_matches]


def preprocess_mark(mark):
    mark = mark.strip()
    mark = re.sub('\s+', ' ', mark)
    return mark


def preprocess_marks(marks):
    # Remove duplicates
    marks = list(OrderedDict.fromkeys(marks))
    # Trim spaces
    marks = [preprocess_mark(q) for q in marks]
    marks = remove_unwanted_matches(marks)
    return marks


def get_steps(marks):
    """
    Parses a list of marks and extracts the step-control hierarchy. It also
    links the metadatas to the controls.
    """
    steps = [Step(DEFAULT_STEP_NAME, DEFAULT_STEP_GROUP_NAME)]

    for mark in marks:
        # If it's a step mark:
        step_name = parse_mark(mark, 'step')
        if step_name is not None:
            steps += [Step(step_name, DEFAULT_STEP_GROUP_NAME)]
        else:
            # If it's not a step mark,it must be a control
            steps[-1].add_control(mark)
    return steps
