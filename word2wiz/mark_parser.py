import re
from os.path import dirname, realpath, join
from .spell_helper import Step, DynamicStep, LabelControl, make_control
from .util import parse_mark


def remove_unwanted_matches(marks, file_path=None):
    """
    Loads the unwanted matches from unwanted_matches.txt (by default), and
    returns a list with the marks that do not match.
    Args:
        marks(list): A list of strings with all the matches
        file_path(str): Optional. The file that contains the unwanted matches.
    Returns:
        The input list minus the marks that are in the unwanted_matches.txt.
    """
    if file_path is None:
        current_dir = dirname(realpath(__file__))
        file_path = join(current_dir, 'unwanted_matches.txt')
    with open(file_path) as f:
        unwanted_matches = [m for m in f.read().splitlines()]
    return [q for q in marks if q not in unwanted_matches]


def trim_mark(mark):
    mark = mark.strip()
    mark = re.sub('\s+', ' ', mark)
    return mark


def get_metadata(metadata_num):
    return 'txt_{:03d}'.format(metadata_num + 1)


def assign_metadatas(steps):
    i = 0
    for step in steps:
        for control in step.controls:
            # <<line>> and <<text>> do not consume metadata
            if not isinstance(control, LabelControl):
                control.metadata_name = get_metadata(i)
                i += 1


def get_steps(config, marks):
    """
    Parses a list of marks and extracts the step-control hierarchy. It also
    links the metadatas to the controls.
    """
    # Trim spaces
    marks = [trim_mark(q) for q in marks]
    marks = remove_unwanted_matches(marks)

    steps = [
        Step('static1'),
        DynamicStep(config.defaultstepname, config.defaultstepgroupname)
    ]

    # Number of the letter we are processing right now
    letter = 1
    for mark in marks:
        # If it's a step mark:
        step_name = parse_mark(mark, 'step')
        new_brief = mark == 'gekoppeldebrief'
        if step_name is not None:
            steps += [DynamicStep(step_name, config.defaultstepgroupname,
                                  letter_num=letter)]
        elif new_brief:
            # Add an upload step to finish the letter and add the new steps
            steps += [Step('upload', letter_num=letter)]
            letter += 1
            steps += [Step('static{}'.format(letter), letter_num=letter)]
            steps += [DynamicStep(config.defaultstepname, config.defaultstepgroupname,
                                  letter_num=letter)]
        else:
            # If it's not a step mark,it must be a control
            steps[-1].add_control(make_control(mark))

    # Remove duplicate controls
    for step in [s for s in steps if type(s) is DynamicStep]:
        step.remove_duplicate_controls()

    # Always add the upload and final step at the end
    steps += [
        Step('upload', letter_num=letter),
        Step('end', letter_num=letter)
    ]

    # Link step.next_step
    for i, step in enumerate(steps):
        step.next_step = steps[i + 1] if i + 1 < len(steps) else None


    # Assign metadatas
    assign_metadatas([s for s in steps if type(s) is DynamicStep])

    return steps
