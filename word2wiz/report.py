from .spell_helper import DynamicStep, LineControl, ListControl, CheckboxControl


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

    for step in [s for s in steps if type(s) is DynamicStep]:
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
