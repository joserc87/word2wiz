
class Step(object):
    def __init__(self, name, group_name):
        self.name = name
        self.group_name = group_name
        self.controls = []

    def add_control(self, control):
        self.controls += [control]

    def remove_duplicate_controls(self):
        """Remove duplicate controls, except line controls"""
        unique_controls = []
        for control in self.controls:
            for unique_control in unique_controls:
                if control == unique_control and \
                        (isinstance(control, ListControl) or
                         isinstance(control, StringControl)):
                    break
            else:
                unique_controls += [control]
        self.controls = unique_controls


class Control(object):
    def __init__(self, type, mark):
        self.type = type
        self.original_mark = mark
        self.metadata_name = None
        self.question = ""
        self.required = False

    def __eq__(self, other):
        return (self.original_mark, self.metadata_name, self.question) == \
            (other.original_mark, other.metadata_name, other.question)


class ListControl(Control):
    def __init__(self, mark):
        super().__init__('list', mark)
        parts = [part.strip() for part in mark.split(';')]
        self.question = parts[0]
        self.values = parts[1:]
        self.required = True

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, ListControl) and \
            self.values == other.values


class CheckboxControl(Control):
    def __init__(self, mark):
        super().__init__('checkbox', mark)
        self.type = 'checkbox'
        self.question, self.label = (part.strip() for part in mark.split(';'))

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, CheckboxControl)


class LineControl(Control):
    def __init__(self, mark):
        super().__init__('line', mark)
        self.question = ''

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, LineControl)


class StringControl(Control):
    def __init__(self, mark):
        super().__init__('string', mark)
        self.question = mark.strip()

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, StringControl)


class LabelControl(Control):
    def __init__(self, mark):
        super().__init__('label', mark)
        self.question = ''
        self.default_value = mark.strip()

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, LabelControl)


def make_control(mark):
    """
    Factory method to create different kinds of controls
    """
    words = mark.split()
    types = {
        'list': ListControl,
        'checkbox': CheckboxControl,
        'line': LineControl,
        'string': StringControl,
        'text': LabelControl
    }
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
