Feature: Parsing default values
    As a program
    I want that the default marks are parsed
    So that the special marks are removed and the values can be used

    Scenario: Getting default values
        Given a list of marks
            | mark |
        When we parse the defaults
        Then config.defaultonderwerptekst should be empty
         And config.defaultondertekenaar should be empty
         And config.defaultfunctieondertekenaar should be empty
         And config.defaultbijlageuploaden should be false
         And config.defaultmedischecategorie should be "Medisch Declaratie"

    Scenario: Setting regular string defaults
        Given a list of marks
            | mark |
            | defaultonderwerptekst my onderwerp tekst             |
            | defaultondertekenaar my ondertekenaar                |
        When we parse the defaults
        Then config.defaultonderwerptekst should be "my onderwerp tekst"
         And config.defaultondertekenaar should be "my ondertekenaar"

    Scenario: Functieondertekenaar and medischcategorie are capitalized
        Given a list of marks
            | mark |
            | defaultfunctieondertekenaar my functie ondertekenaar |
            | defaultmedischecategorie my medische categorie       |
        When we parse the defaults
        Then config.defaultfunctieondertekenaar should be "My functie ondertekenaar"
         And config.defaultmedischecategorie should be "My medische categorie"

    Scenario: Bijlageuploaden is True
        Given a list of marks
            | mark |
            | defaultbijlageuploaden ja |
        When we parse the defaults
        Then config.defaultbijlageuploaden should be true

    Scenario: Bijlageuploaden is False
        Given a list of marks
            | mark |
            | defaultbijlageuploaden nee |
        When we parse the defaults
        Then config.defaultbijlageuploaden should be false
