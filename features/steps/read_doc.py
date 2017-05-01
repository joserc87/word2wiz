from behave import given, when, then
from hamcrest import *
import word2wiz.word


class Paragraph:
    def __init__(self, text):
        self.text = text


class DocumentMock:
    def __init__(self, path):
        self.path = path
        self.paragraphs = []


@given('a word document')
def step_impl(context):
    context.document = DocumentMock('some path')
    word2wiz.word.Document = lambda path: context.document


@given('a paragraph')
def step_impl(context):
    context.document.paragraphs += [Paragraph(context.text)]


@when('we analyse the document')
def step_impl(context):
    context.questions = word2wiz.word.analyse_doc('some path')


@then('the returned questions should be')
def step_impl(context):
    assert_that(context.questions, equal_to(
        [row['question'] for row in context.table]))
