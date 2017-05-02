from jinja2 import Environment, FileSystemLoader
from behave import *
from hamcrest import *
from os.path import dirname, realpath, join
from word2wiz.mark_parser import *
from word2wiz.spell_helper import *

control_types = {
    'list': ListControl,
    'checkbox': CheckboxControl,
    'string': StringControl,
    'line': LineControl,
    'label': LabelControl
}


@given('a {type} control from mark "{mark}"')
def step_impl(context, type, mark):
    context.control = control_types[type](mark)


@given('the control question is "{question}"')
@given('the control question is empty')
def step_impl(context, question=''):
    context.control.question = question


@given('the control question is hidden')
def step_impl(context, question=''):
    context.control.question_hidden = True


@given('the control question is not hidden')
def step_impl(context, question=''):
    context.control.question_hidden = False


@given('the control metadata is {metadata}')
def step_impl(context, metadata):
    context.control.metadata_name = metadata


@given('the control label is "{label}"')
def step_impl(context, label):
    context.control.label = label


@given('the control default value is "{default_value}"')
def step_impl(context, default_value):
    context.control.default_value = default_value


@given('the control default value is true')
def step_impl(context):
    context.control.default_value = True


@given('the control default value is false')
def step_impl(context):
    context.control.default_value = False


@given('the control is optional')
def step_impl(context):
    context.control.required = False


@given('the control is required')
def step_impl(context):
    context.control.required = True


@when('we render the control')
def step_impl(context):
    current_dir = dirname(realpath(__file__))
    spell_dir = join(current_dir, '..', '..', 'word2wiz', 'spell')
    env = Environment(loader=FileSystemLoader(spell_dir),
                      trim_blocks=True,
                      lstrip_blocks=True)
    control_template = env.from_string(
        "{% from 'control.spl' import render_control %}" +
        "{{ render_control(control) }}")
    context.result = control_template.render(control=context.control)


@then('the result should be')
def step_impl(context):
    assert_that(context.result, equal_to(context.text))
