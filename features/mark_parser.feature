Feature: Getting steps from marks
    As a user
    I want to transform the marks in the word document and get the steps with
    controls
    So that I can generate a wizard configuration with the result

    Scenario: One simple control
        Given a list of marks
            | mark         |
            | one question |
         When we get the steps for those marks
         Then there should be 1 step
          And step 0 should have 1 control
          And control 0 in step 0 should be a string control

    Scenario: Two empty steps
        Given a list of marks
            | mark |
            | step Algemeen |
        When we get the steps for those marks
        Then there should be 2 steps
         And name of step 0 should be "doc_name"
         And name of step 1 should be "Algemeen"
         And group name of step 0 should be "Buitenland"
         And group name of step 1 should be "Buitenland"

    Scenario: 2 steps with unwanted matches
        Given a list of marks
            | mark                      |
            | verwijderen               |
            | altijd                    |
            | question 1                |
            | voorletters               |
            | mw_initialen              |
            | step Second step          |
            | lb_tekst                  |
            | lb_naam                   |
            | lb_naam                   |
            | list question 2;val1;val2 |
            | org_adres                 |
         When we get the steps for those marks
         Then there should be 2 steps
          And step 0 should have 1 control
          And step 1 should have 1 control
          And the question for control 0 in step 0 should be "question 1"
          And the question for control 0 in step 1 should be "question 2"

    Scenario: Marks with inner spaces
        Given a list of marks
            | mark                                                |
            |  	 my mark  with	multiple 	 inner spaces         |
            | list Question  with   spaces 	; item 1	; item  2 |
         When we get the steps for those marks
         Then there should be 1 step
          And step 0 should have 2 control
          And the question for control 0 in step 0 should be "my mark with multiple inner spaces"
          And the question for control 1 in step 0 should be "Question with spaces"
          And the items for control 1 in step 0 should be
              | item   |
              | item 1 |
              | item 2 |

    # Scenario: Remove duplicates
    # TODO
