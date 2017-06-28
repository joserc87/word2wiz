Feature: Generating a report
    As the person who will create the document in Composition Center
    I need the link between the marks in the document (questions) and the
    metadata linked to them
    So that I can create the content in Composition Center

    Scenario: One step with two controls
        Given a list of marks
            | mark             |
            | one question     |
            | another question |
          And a configuration
        When we get the steps for those marks
         And we generate a report for those steps
        Then the report should be
            """
            +----------+------------------+----------+---------+
            |   STEP   |      FIELD       | METADATA | OPTIONS |
            +----------+------------------+----------+---------+
            | doc_name | one question     | txt_001  |         |
            |          | another question | txt_002  |         |
            +----------+------------------+----------+---------+

            """

    Scenario: Two steps with two controls
        Given a list of marks
            | mark        |
            | question 1  |
            | question 2  |
            | step step 2 |
            | question 3  |
            | question 4  |
          And a configuration
        When we get the steps for those marks
         And we generate a report for those steps
        Then the report should be
            """
            +----------+------------+----------+---------+
            |   STEP   |   FIELD    | METADATA | OPTIONS |
            +----------+------------+----------+---------+
            | doc_name | question 1 | txt_001  |         |
            |          | question 2 | txt_002  |         |
            +----------+------------+----------+---------+
            | step 2   | question 3 | txt_003  |         |
            |          | question 4 | txt_004  |         |
            +----------+------------+----------+---------+

            """

    Scenario: Two steps with a line
        Given a list of marks
            | mark        |
            | question 1  |
            | question 2  |
            | step step 2 |
            | question 3  |
            | question 4  |
            | line        |
            | question 5  |
            | question 6  |
          And a configuration
        When we get the steps for those marks
         And we generate a report for those steps
        Then the report should be
            """
            +----------+------------+----------+---------+
            |   STEP   |   FIELD    | METADATA | OPTIONS |
            +----------+------------+----------+---------+
            | doc_name | question 1 | txt_001  |         |
            |          | question 2 | txt_002  |         |
            +----------+------------+----------+---------+
            | step 2   | question 3 | txt_003  |         |
            |          | question 4 | txt_004  |         |
            |          +------------+----------+---------+
            |          | question 5 | txt_005  |         |
            |          | question 6 | txt_006  |         |
            +----------+------------+----------+---------+

            """

    Scenario: List items
        Given a list of marks
            | mark                             |
            | list question text;item 1;item 2 |
            | question 2                       |
          And a configuration
        When we get the steps for those marks
         And we generate a report for those steps
        Then the report should be
            """
            +----------+---------------+----------+-----------------+
            |   STEP   |     FIELD     | METADATA |     OPTIONS     |
            +----------+---------------+----------+-----------------+
            | doc_name | question text | txt_001  | item 1 | item 2 |
            |          | question 2    | txt_002  |                 |
            +----------+---------------+----------+-----------------+

            """

    Scenario: Text items
        Given a list of marks
            | mark                 |
            | text my label        |
            | question             |
            | text my label        |
            | checkbox my checkbox |
          And a configuration
        When we get the steps for those marks
         And we generate a report for those steps
        Then the report should be
            """
            +----------+-------------+----------+--------------+
            |   STEP   |    FIELD    | METADATA |   OPTIONS    |
            +----------+-------------+----------+--------------+
            | doc_name | my label    |          |              |
            |          | question    | txt_001  |              |
            |          | my label    |          |              |
            |          | my checkbox | txt_002  | True | False |
            +----------+-------------+----------+--------------+

            """

    Scenario: Second envelope
        Given a list of marks
            | mark               |
            | text label l1s1    |
            | question l1s1      |
            | step step2 letter1 |
            | text label l1s2    |
            | question l1s2      |
            | gekoppeldebrief    |
            | text label l2s1    |
            | question l2s1      |
            | step step2 letter2 |
            | text label l2s2    |
            | question l2s2      |
          And a configuration
        When we get the steps for those marks
         And we generate a report for those steps
        Then the report should be
            """
            +---------------+---------------+----------+---------+
            |      STEP     |     FIELD     | METADATA | OPTIONS |
            +---------------+---------------+----------+---------+
            | doc_name      | label l1s1    |          |         |
            |               | question l1s1 | txt_001  |         |
            +---------------+---------------+----------+---------+
            | step2 letter1 | label l1s2    |          |         |
            |               | question l1s2 | txt_002  |         |
            +---------------+---------------+----------+---------+

            +---------------+---------------+----------+---------+
            | doc_name      | label l2s1    |          |         |
            |               | question l2s1 | txt_003  |         |
            +---------------+---------------+----------+---------+
            | step2 letter2 | label l2s2    |          |         |
            |               | question l2s2 | txt_004  |         |
            +---------------+---------------+----------+---------+

            """
