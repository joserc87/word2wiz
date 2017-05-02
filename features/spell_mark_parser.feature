Feature: Parsing control marks
    In order to transform the marks in the word document to a wizard
    configuration,
    As a user of the utility methods
    I want the methods to generate controls from the content of the marks
    (strings)

    ##########
    # String #
    ##########

    Scenario: Generic string question mark
        Given a mark with content "Naam"
         When we make a control from that mark
         Then it should create a string control
          And the question should be "Naam"
          And the default value should be null
          And the question should not be hidden

    Scenario: Generic optional string question mark
        Given a mark with content "optional Dit is een unvelveld"
         When we make a control from that mark
         Then it should create a string control
          And the question should be "Dit is een unvelveld"
          And the default value should be null
          And the question should be optional

    Scenario: Generic optional string question mark
        Given a mark with content "required Dit is een unvelveld"
         When we make a control from that mark
         Then it should create a string control
          And the question should be "Dit is een unvelveld"
          And the default value should be null
          And the question should be required

    Scenario: String mark with default value
        Given a mark with content "Dit is een unvelveld=default waarde"
         When we make a control from that mark
         Then it should create a string control
          And the question should be "Dit is een unvelveld"
          And the default value should be "default waarde"
          And the question should be optional

    Scenario: String mark with empty modifier
        Given a mark with content "empty Dit is een unvelveld"
         When we make a control from that mark
         Then it should create a string control
          And the question should be "Dit is een unvelveld"
          And the question should be hidden

    ########
    # Line #
    ########

    Scenario: Line mark
        Given a mark with content "line"
         When we make a control from that mark
         Then it should create a line control
          And it should create a label control
          And the question should be empty
          And the default value should be "--------------------------------------------------"
          And the question should be hidden

    ############
    # Checkbox #
    ############

    Scenario: Checkbox mark
        Given a mark with content "checkbox  andere nota’s; Wij verwerkten andere nota’s"
         When we make a control from that mark
         Then it should create a checkbox control
          And the question should be "andere nota’s"
          And the label should be "Wij verwerkten andere nota’s"
          And the default value should be null
          And the question should not be hidden

    Scenario: Checkbox mark (selected)
        Given a mark with content "checkbox Dit is een checkbox=on"
         When we make a control from that mark
         Then it should create a checkbox control
          And the question should be empty
          And the label should be "Dit is een checkbox"
          And the default value should be true

    Scenario: Checkbox mark (unselected)
        Given a mark with content "checkbox Dit is een checkbox=off"
         When we make a control from that mark
         Then it should create a checkbox control
          And the question should be empty
          And the label should be "Dit is een checkbox"
          And the default value should be false

    Scenario: Checkbox mark with empty modifier
        Given a mark with content "checkbox empty andere nota’s; Wij verwerkten andere nota’s"
         When we make a control from that mark
         Then it should create a checkbox control
          And the question should be "andere nota’s"
          And the label should be "Wij verwerkten andere nota’s"
          And the default value should be null
          And the question should be hidden

    ########
    # List #
    ########

    Scenario: List mark
        Given a mark with content "list Gaat het om 1 of meerdere nota’s?;1 nota; meerdere nota’s"
         When we make a control from that mark
         Then it should create a list control
          And the question should be "Gaat het om 1 of meerdere nota’s?"
          And the items should be
              | item            |
              | 1 nota          |
              | meerdere nota’s |
          And the default value should be null
          And the question should not be hidden

    Scenario: List mark
        Given a mark with content "list Gaat het om 1 of meerdere nota’s?;1 nota; meerdere nota’s=1 nota"
         When we make a control from that mark
         Then it should create a list control
          And the question should be "Gaat het om 1 of meerdere nota’s?"
          And the items should be
              | item            |
              | 1 nota          |
              | meerdere nota’s |
          And the default value should be "1 nota"

    Scenario: List mark with empty modifier
        Given a mark with content "list empty Gaat het om 1 of meerdere nota’s?;1 nota; meerdere nota’s"
         When we make a control from that mark
         Then it should create a list control
          And the question should be "Gaat het om 1 of meerdere nota’s?"
          And the items should be
              | item            |
              | 1 nota          |
              | meerdere nota’s |
          And the default value should be null
          And the question should be hidden

    ########
    # Text #
    ########

    Scenario: Text mark
        Given a mark with content "text Dit is gewoon tekst"
         When we make a control from that mark
         Then it should create a label control
          And the question should be empty
          And the default value should be "Dit is gewoon tekst"
          And the question should be hidden

    Scenario: Text mark with default value
        Given a mark with content "text Dit is gewoon tekst=Dit is andere tekst"
         When we make a control from that mark
         Then it should create a label control
          And the question should be empty
          And the default value should be "Dit is andere tekst"
