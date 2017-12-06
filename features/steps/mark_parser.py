from behave import *
from hamcrest import *
from word2wiz.mark_parser import *
from word2wiz.spell_helper import *
from word2wiz.config import Config


@given('a configuration')
def step_impl(context):
    context.conf = Config()
    context.conf.defaultstepname = 'doc_name'

@given('a list of marks')
def step_impl(context):
    context.marks = [row['mark'] for row in context.table]

@when('we get the steps for those marks')
def step_impl(context):
    context.steps = get_steps(context.conf, context.marks)

@then('there should be {num_steps:d} step')
@then('there should be {num_steps:d} steps')
def step_impl(context, num_steps):
    assert_that(len(context.steps), equal_to(num_steps))

@then('step {num_step:d} should have template "{template}"')
def step_impl(context, num_step, template):
    assert_that(context.steps[num_step].template, equal_to(template))

@then('step {num_step:d} should have letter_num {letter_num:d}')
def step_impl(context, num_step, letter_num):
    assert_that(context.steps[num_step].letter_num, equal_to(letter_num))

@then('step {num_step:d} should not have next step')
@then('next step of step {num_step:d} should be {num_next_step:d}')
def step_impl(context, num_step, num_next_step=None):
    assert_that(context.steps[num_step].next_step,
                equal_to(None if num_next_step is None
                         else context.steps[num_next_step]))


@then('step {step_num:d} should have {num_controls:d} control')
@then('step {step_num:d} should have {num_controls:d} controls')
def step_impl(context, step_num, num_controls):
    assert_that(len(context.steps[step_num].controls),
                equal_to(num_controls))

@then('control {control_num:d} in step {step_num:d} should be a' +
      ' {type_control} control')
def step_impl(context, control_num, step_num, type_control):
    control = context.steps[step_num].controls[control_num]
    control_types = {
        'list': ListControl,
        'checkbox': CheckboxControl,
        'string': StringControl,
        'line': LineControl,
        'label': LabelControl
    }
    assert_that(type_control, is_in(control_types.keys()))
    assert_that(control, instance_of(control_types[type_control]))

@then('the question for control {control_num:d} in step {step_num:d}' +
      ' should be "{question}"')
def step_impl(context, control_num, step_num, question):
    control = context.steps[step_num].controls[control_num]
    assert_that(control.question, equal_to(question))

@then('name of step {step_num:d} should be "{step_name}"')
def step_impl(context, step_num, step_name):
    assert_that(context.steps[step_num].name,
                equal_to(step_name))

@then('group name of step {step_num:d} should be "{step_group_name}"')
def step_impl(context, step_num, step_group_name):
    assert_that(context.steps[step_num].group_name,
                equal_to(step_group_name))

@then('the items for control {control_num:d} in step {step_num:d} should be')
def step_impl(context, control_num, step_num):
    items = [row['item'] for row in context.table]
    assert_that(context.steps[step_num].controls[control_num].values,
                equal_to(items))

@then('control {control_num:d} in step {step_num:d} should have no metadata')
@then('control {control_num:d} in step {step_num:d} should have metadata ' +
      '"{metadata}"')
def step_impl(context, control_num, step_num, metadata=None):
    control = context.steps[step_num].controls[control_num]
    assert_that(control.metadata_name, equal_to(metadata))

@then('control {control_num:d} in step {step_num:d} should be required')
def step_impl(context, control_num, step_num):
    control = context.steps[step_num].controls[control_num]
    assert_that(control.required, equal_to(True))

@then('control {control_num:d} in step {step_num:d} should not be required')
def step_impl(context, control_num, step_num):
    control = context.steps[step_num].controls[control_num]
    assert_that(control.required, equal_to(False))
