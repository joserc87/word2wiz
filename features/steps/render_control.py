from jinja2 import Environment, FileSystemLoader
from behave import *
from hamcrest import *
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


@given('the control metadata is {metadata}')
def step_impl(context, metadata):
    context.control.metadata_name = metadata


@given('the control label is "{label}"')
def step_impl(context, label):
    context.control.label = label


@given('the control is optional')
def step_impl(context):
    context.control.required = False


@given('the control is required')
def step_impl(context):
    context.control.required = True


@when('we render the control')
def step_impl(context):
    env = Environment(loader=FileSystemLoader('spell'),
                      trim_blocks=True,
                      lstrip_blocks=True)
    control_template = env.from_string(
        "{% from 'control.spl' import render_control %}" +
        "{{ render_control(control) }}")
    context.result = control_template.render(control=context.control)


@then('the result should be')
def step_impl(context):
    assert_that(context.result, equal_to(context.text))
