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
    assert_that(value, equal_to(False))
