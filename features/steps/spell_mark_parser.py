from behave import *
from hamcrest import *
from word2wiz.spell_helper import *


@given('a mark with content "{mark}"')
def step_impl(context, mark):
    context.mark = mark

@when('we make a control from that mark')
def step_impl(context):
    context.result = make_control(context.mark)

@then('it should create a {type_control} control')
def step_impl(context, type_control):
    control_types = {
        'list': ListControl,
        'checkbox': CheckboxControl,
        'string': StringControl,
        'line': LineControl,
        'label': LabelControl,
    }
    assert_that(type_control, is_in(control_types.keys()))
    assert_that(context.result, instance_of(control_types[type_control]))

@then('the question should be "{question}"')
@then('the question should be empty')
def step_impl(context, question=""):
    assert_that(context.result.question, equal_to(question))

@then('the question should be required')
def step_impl(context):
    assert_that(context.result.required, is_(True))

@then('the question should be optional')
def step_impl(context):
    assert_that(context.result.required, is_(False))

@then('the question should be hidden')
def step_impl(context):
    assert_that(context.result.question_hidden, is_(True))

@then('the question should not be hidden')
def step_impl(context):
    assert_that(context.result.question_hidden, is_(False))

# Checkbox:
@then('the label should be "{label}"')
def step_impl(context, label):
    assert_that(context.result.label, equal_to(label))

# List:
@then('the items should be')
def step_impl(context):
    items = [row['item'] for row in context.table]
    assert_that(context.result.values, equal_to(items))

# Default values:
@then('the default value should be "{default_value}"')
@then('the default value should be empty')
def step_impl(context, default_value=''):
    assert_that(context.result.default_value, equal_to(default_value))

@then('the default value should be true')
def step_impl(context):
    assert_that(context.result.default_value, is_(True))

@then('the default value should be false')
def step_impl(context):
    assert_that(context.result.default_value, is_(False))

@then('the default value should be null')
def step_impl(context):
    assert_that(context.result.default_value, is_(none()))
