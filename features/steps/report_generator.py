from behave import *
from hamcrest import *
from word2wiz.report import generate_report


@when('we generate a report for those steps')
def step_impl(context):
    context.report = generate_report(context.steps)

@then('the report should be')
def step_impl(context):
    report = context.report.replace('\r', '')
    assert_that(report, equal_to(context.text))
