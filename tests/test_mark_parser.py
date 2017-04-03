import unittest
import word2wiz.mark_parser


class test_remove_unwanted_matches(unittest.TestCase):

    def setUp(self):
        self.marks = ['verwijderen',
                      'altijd',
                      'mark1',
                      'voorletters',
                      'mw_initialen',
                      'lb _tekst',
                      'lb_naam',
                      'lb_naam',
                      'mark2',
                      'mark2'
                      ]

    def test_remove_unwanted_matches(self):
        marks = word2wiz.mark_parser.remove_unwanted_matches(self.marks)
        self.assertEquals(marks, ['mark1', 'mark2', 'mark2'])


class test_preprocess_mark(unittest.TestCase):
    def test_preprocess_mark(self):
        mark = ' \t my mark  with\tmultiple \t inner spaces'
        self.assertEquals(
            word2wiz.mark_parser.preprocess_mark(mark),
            'my mark with multiple inner spaces'
        )


class test_preprocess_marks(unittest.TestCase):
    def test_preprocess_marks_removes_duplicates(self):
        marks = ['q1', 'q1', 'q2']
        pq = word2wiz.mark_parser.preprocess_marks(marks)
        self.assertEquals(pq, ['q1', 'q2'])

    def test_preprocess_marks_trims_spaces(self):
        marks = [' mark  with  \t spaces \t', 'q2']
        pq = word2wiz.mark_parser.preprocess_marks(marks)
        self.assertEquals(pq, ['mark with spaces', 'q2'])

    def test_preprocess_marks_removes_unwanted_matches(self):
        marks = ['lb_naam', 'lb_naam ', 'q1', ' verwijderen ', 'q2']
        pq = word2wiz.mark_parser.preprocess_marks(marks)
        self.assertEquals(pq, ['q1', 'q2'])


class test_get_steps(unittest.TestCase):
    def test_get_steps(self):
        # Given a list of marks
        marks = ['mark1',
                 'mark2',
                 'mw_initialen',  # Ignore
                 'step Algemeen',
                 'list a;b;c'
                 ]
        # When we get the controls:
        steps = word2wiz.mark_parser.get_steps(marks)
        self.assertEquals(2, len(steps))
        self.assertEquals(steps[1].name, 'Algemeen')
        self.assertEquals(steps[1].group_name, 'Buitenland')
