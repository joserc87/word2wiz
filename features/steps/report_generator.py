from behave import *
from hamcrest import *
from textwrap import dedent
from word2wiz.report import generate_report


@when('we generate a report for those steps')
def step_impl(context):
    context.report = generate_report(context.steps)

@then('the report should be')
def step_impl(context):
    report = context.report.replace('\r', '')
    assert_that(report, equal_to(context.text), dedent('''
                The report shuld look like:
                {}
                But instead it is rendered like this:
                {}''').format(context.text, report))
