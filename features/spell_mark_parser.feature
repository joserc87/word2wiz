Feature: Parsing control marks
    In order to transform the marks in the word document to a wizard
    configuration,
    As a user of the utility methods
    I want the methods to generate controls from the content of the marks
    (strings)

    Scenario: Generic string question mark
        Given a mark with content "Naam"
         When we make a control from that mark
         Then it should create a string control
          And the question should be "Naam"

    Scenario: Line mark
        Given a mark with content "line"
         When we make a control from that mark
         Then it should create a line control
          And the question should be empty

    Scenario: Checkbox mark
        Given a mark with content "checkbox  andere nota’s; Wij verwerkten andere nota’s"
         When we make a control from that mark
         Then it should create a checkbox control
          And the question should be "andere nota’s"
          And the label should be "Wij verwerkten andere nota’s"

    Scenario: List mark
        Given a mark with content "list Gaat het om 1 of meerdere nota’s?;1 nota; meerdere nota’s"
         When we make a control from that mark
         Then it should create a list control
          And the question should be "Gaat het om 1 of meerdere nota’s?"
          And the items should be
              | item            |
              | 1 nota          |
              | meerdere nota’s |
