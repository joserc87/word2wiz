
class Step:
    def __init__(self, name, group_name):
        self.name = name
        self.group_name = group_name
        self.controls = []

    def add_control(self, control):
        self.controls += [control]


class Control:
    def __init__(self, mark):
        self.original_mark = mark
        self.metadata_name = None
        # Get the desired control type from the mark
        if mark.startswith('list '):
            self.type = 'list'
            parts = mark.split(';')
            self.question = parts[0][len('list'):].strip()
            self.values = [val.strip() for val in parts[1:]]
        elif mark.startswith('checkbox '):
            self.type = 'checkbox'
            parts = mark.split(';')
            self.question = parts[0][len('checkbox'):].strip()
            self.label = parts[-1].strip()
        elif mark.startswith('line'):
            # used to output a line between questions (it's just a label)
            self.type = 'line'
        else:
            # Otherwise it's a string control
            self.type = 'string'
            self.question = mark.strip()
