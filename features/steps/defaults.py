from behave import when, then
from hamcrest import assert_that, equal_to
from word2wiz.config import Config


@when('we parse the defaults')
def step_impl(context):
    context.conf = Config()
    context.conf.parse_defaults(context.marks)

def _get_value(context, default):
    config = context.conf
    if default == 'defaultonderwerptekst':
        value = config.defaultonderwerptekst
    if default == 'defaultondertekenaar':
        value = config.defaultondertekenaar
    if default == 'defaultfunctieondertekenaar':
        value = config.defaultfunctieondertekenaar
    if default == 'defaultbijlageuploaden':
        value = config.defaultbijlageuploaden
    if default == 'defaultmedischecategorie':
        value = config.defaultmedischecategorie
    return value

@then('config.{default} should be "{expected_value}"')
@then('config.{default} should be empty')
def step_impl(context, default, expected_value=''):
    value = _get_value(context, default)
    assert_that(value, equal_to(expected_value))


@then('config.{default} should be true')
def step_impl(context, default):
    value = _get_value(context, default)
    assert_that(value, equal_to(True))


@then('config.{default} should be false')
def step_impl(context, default):
    value = _get_value(context, default)

@then('config.{default} should be [{values}]')
def step_impl(context, default, values):
    listValue = _get_value(context, default)
    for i, sValue in enumerate([s.strip() for s in values.split(',')]):
        value = None
        if sValue == 'true':
            value = True
        elif sValue == 'false':
            value = False
        elif sValue[0] == sValue[-1] and sValue[0] in ['"', "'"]:
            value = sValue[1:-1]
        assert_that(listValue[i], equal_to(value), 'Error in value {}'.format(i))
