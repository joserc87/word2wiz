
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
        self.default_value = None
        self.question_hidden = False

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
        stripped = [part.strip() for part in mark.split(';')]
        self.question, self.label = stripped if len(stripped) == 2 \
            else ('', stripped[0])
        self._default_value = None

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, CheckboxControl)

    @property
    def default_value(self):
        """Wrapper to make sure that the default_value is a boolean"""
        return self._default_value

    @default_value.setter
    def default_value(self, value):
        if value is None:
            self._default_value = None
        elif type(value) is bool:
            self._default_value = value
        else:
            value = value.lower()
            if value in ['on', 'true', 'ja', 'yes', 'selected']:
                self._default_value = True
            elif value in ['off', 'false', 'nee', 'no', 'unselected',
                           'not selected']:
                self._default_value = False
            else:
                # TODO: Throw an exception?
                pass


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
        self.question_hidden = True

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, LabelControl)


class LineControl(LabelControl):
    def __init__(self, mark):
        super().__init__(mark)
        # Override type
        self.type = 'line'
        self.question = ''
        self.default_value = '-'*50

    def __eq__(self, other):
        return super().__eq__(other) and \
            isinstance(other, LineControl)


def make_control(mark):
    """
    Factory method to create different kinds of controls
    """
    # Exctract default value from the mark:
    eq = mark.find('=')
    default_value = None
    if eq >= 0:
        default_value = mark[eq+1:].strip()
        mark = mark[:eq]

    # Divide the mark in words
    words = mark.split()
    types = {
        'list': ListControl,
        'checkbox': CheckboxControl,
        'line': LineControl,
        'string': StringControl,
        'text': LabelControl
    }
    modifiers = ['required',
                 'optional',
                 'empty'
                 ]
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
    elif 'empty' in found_modifiers:
        control.question_hidden = True

    # Set default value (if specified)
    if default_value is not None:
        control.default_value = default_value

    return control
