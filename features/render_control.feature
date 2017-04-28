Feature: Rentering spell controls
    As a user
    I want the internal controls to be rendered
    So that I can generate a spell file with them

    ##########
    # String #
    ##########

    Scenario: A simple string control
        Given a string control from mark "Naam"
          And the control question is "Naam"
          And the control metadata is txt_123
          And the control is optional
         When we render the control
         Then the result should be
             """
             'Naam' -> $txt_123

             """

    Scenario: A required string control
        Given a string control from mark "Naam"
          And the control question is "Naam"
          And the control metadata is txt_321
          And the control is required
         When we render the control
         Then the result should be
             """
             required 'Naam' -> $txt_321

             """

    Scenario: A string control with default value
        Given a string control from mark "Naam"
          And the control question is "Naam"
          And the control metadata is txt_321
          And the control is required
          And the control default value is "defaultwaarde"
         When we render the control
         Then the result should be
             """
             required 'Naam' = 'defaultwaarde' -> $txt_321

             """

    ########
    # List #
    ########

    Scenario: A simple list control with items
        Given a list control from mark "Dit is de vraagtekst;nota;nota’s"
          And the control question is "Dit is de vraagtekst"
          And the control metadata is txt_list
          And the control is required
         When we render the control
         Then the result should be
             """
             required list 'Dit is de vraagtekst' -> $txt_list:
                 'nota'
                 'nota’s'

             """

    Scenario: An optional list control with items
        Given a list control from mark "Dit is de vraagtekst;nota;nota’s"
          And the control question is "Dit is de vraagtekst"
          And the control metadata is txt_list
          And the control is optional
         When we render the control
         Then the result should be
             """
             list 'Dit is de vraagtekst' -> $txt_list:
                 'nota'
                 'nota’s'

             """

    Scenario: An list control with default value
        Given a list control from mark "Dit is de vraagtekst;nota;nota’s"
          And the control question is "Dit is de vraagtekst"
          And the control metadata is txt_list
          And the control is optional
          And the control default value is "nota’s"
         When we render the control
         Then the result should be
             """
             list 'Dit is de vraagtekst' = 'nota’s' -> $txt_list:
                 'nota'
                 'nota’s'

             """

    ############
    # Checkbox #
    ############

    Scenario: A simple checkbox
        Given a checkbox control from mark "Dit is een checkbox"
          And the control question is empty
          And the control metadata is txt_checkbox
          And the control label is "Dit is een checkbox"
          And the control is optional
         When we render the control
         Then the result should be
             """
             checkbox(@label='Dit is een checkbox') '' -> $txt_checkbox

             """

    Scenario: A required checkbox
        Given a checkbox control from mark "Dit is een checkbox"
          And the control question is empty
          And the control metadata is txt_checkbox
          And the control label is "Dit is een checkbox"
          And the control is required
         When we render the control
         Then the result should be
             """
             required checkbox(@label='Dit is een checkbox') '' -> $txt_checkbox

             """

    Scenario: A checkbox with selected default value
        Given a checkbox control from mark "Dit is een checkbox"
          And the control question is empty
          And the control metadata is txt_checkbox
          And the control label is "Dit is een checkbox"
          And the control is optional
          And the control default value is true
         When we render the control
         Then the result should be
             """
             checkbox(@label='Dit is een checkbox') '' = selected -> $txt_checkbox

             """

    Scenario: A checkbox with unselected default value
        Given a checkbox control from mark "Dit is een checkbox"
          And the control question is empty
          And the control metadata is txt_checkbox
          And the control label is "Dit is een checkbox"
          And the control is optional
          And the control default value is false
         When we render the control
         Then the result should be
             """
             checkbox(@label='Dit is een checkbox') '' = not selected -> $txt_checkbox

             """

    ########
    # Text #
    ########

    Scenario: A simple text
        Given a label control from mark "Dit is gewoon tekst"
         And the control question is empty
         And the control metadata is null
         And the control default value is "Dit is gewoon tekst"
         And the control is optional
        When we render the control
        Then the result should be
            """
            label '' = 'Dit is gewoon tekst'

            """

    ########
    # Line #
    ########

    Scenario: A line
        Given a line control from mark "line"
         And the control question is empty
         And the control metadata is null
        When we render the control
        Then the result should be
            """
            label '' = '--------------------------------------------------'

            """
