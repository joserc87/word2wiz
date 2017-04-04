
class Step(object):
    def __init__(self, name, group_name):
        self.name = name
        self.group_name = group_name
        self.controls = []

    def add_control(self, control):
        self.controls += [control]


class Control(object):
    def __init__(self, mark):
        self.original_mark = mark
        self.metadata_name = None


class ListControl(Control):
    def __init__(self, mark):
        super().__init__(mark)
        parts = [part.strip() for part in mark.split(';')]
        self.question = parts[0]
        self.values = parts[1:]


class CheckboxControl(Control):
    def __init__(self, mark):
        super().__init__(mark)
        self.question, self.label = (part.strip() for part in mark.split(';'))


class LineControl(Control):
    def __init__(self, mark):
        super().__init__(mark)
        self.question = ''


class StringControl(Control):
    def __init__(self, mark):
        super().__init__(mark)
        self.question = mark.strip()


def make_control(mark):
    """
    Factory method to create different kinds of controls
    """
    words = mark.split()
    types = {'list': ListControl,
             'checkbox': CheckboxControl,
             'line': LineControl,
             'string': StringControl}
    modifiers = ['required',
                 'optional']
    found_modifiers = []

    # The first element contains the type (or if it's not the type, then it's a
    # string
    if len(words) > 0 and words[0] in types.keys():
        type, i = (words[0], 1)
    else:
        type, i = ('string', 0)

    # Parse modifiers
    while i < len(words) and words[i] in modifiers:
        found_modifiers += [words[i]]
        i += 1

    # Create the control:
    control = types[type](' '.join(words[i:]))

    # Apply modifiers to the control
    if 'required' in found_modifiers:
        control.required = True
    elif 'optional' in found_modifiers:
        control.required = False

    return control
