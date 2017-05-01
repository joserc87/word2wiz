Feature: Extracting marks from a MS Word document
    As a user
    I need to extract the marks from the Word document
    So that I can generate a wizard configuration with them

    Scenario: Marks with strange characters
        Given a word document
          And a paragraph
          """
          «Lorem ipsum» dolor sit amet, consectetur adipiscing elit. «Morbi»
          ultricies eleifend velit eget aliquam. Orci varius natoque penatibus
          et magnis dis parturient montes, nascetur ridiculus mus.
          «Curabitur ipsum» elit, vestibulum in posuere dictum, convallis ut
          enim. Donec ut ipsum eros. Duis et nibh mauris. Donec vel elementum
          risus, vulputate sagittis tellus. Sed ullamcorper metus in viverra
          suscipit. Mauris posuere tristique quam, sagittis hendrerit lectus
          aliquam eget. Praesent in augue magna.
          """
          And a paragraph
          """
          Aliquam erat volutpat. Integer ac sodales tellus. Aliquam volutpat
          luctus ante. Vivamus sit amet risus ac magna tempus eleifend id non
          ante. Nulla velit libero, viverra eget nulla non, tincidunt euismod
          lectus. Aenean iaculis velit a neque convallis dignissim. Sed
          tincidunt, sem sed luctus semper, turpis mi dapibus sem, at
          vestibulum justo ex sit amet velit. Maecenas dignissim viverra
          feugiat. Vivamus iaculis dui in pretium mollis. Nulla massa diam,
          sagittis et est quis, aliquam interdum lorem. Curabitur finibus massa
          ac purus congue, a gravida tellus ultrices. Nullam eu dolor odio.
          Etiam iaculis odio lectus, at facilisis «sapien posuere» a.
          Suspendisse accumsan justo eu elit suscipit, dignissim viverra leo
          sagittis. Aliquam porttitor est in cursus sodales.
          """
          When we analyse the document
          Then the returned questions should be
              | question        |
              | Lorem ipsum     |
              | Morbi           |
              | Curabitur ipsum |
              | sapien posuere  |

    Scenario: Marks with simple angle characters
        Given a word document
          And a paragraph
          """
          Lorem ipsum dolor sit amet, <<consectetur adipiscing elit>>. Morbi
          ultricies eleifend velit eget aliquam. Orci varius natoque penatibus
          et magnis dis parturient montes, nascetur <<ridiculus mus>>.
          Curabitur ipsum elit, vestibulum in posuere dictum, convallis ut
          enim. Donec ut ipsum eros. Duis et nibh mauris. Donec vel elementum
          risus, vulputate sagittis tellus. Sed ullamcorper metus in viverra
          suscipit. Mauris posuere tristique quam, sagittis hendrerit lectus
          aliquam eget. <<Praesent>> in augue magna.
          """
          And a paragraph
          """
          Aliquam erat volutpat. Integer ac sodales tellus. Aliquam volutpat
          luctus ante. Vivamus sit amet risus ac magna tempus eleifend id non
          ante. Nulla velit libero, viverra eget nulla non, tincidunt euismod
          lectus. Aenean iaculis velit a neque convallis dignissim. Sed
          tincidunt, sem sed luctus semper, turpis mi dapibus sem, at
          vestibulum justo ex sit amet velit. Maecenas dignissim viverra
          feugiat. Vivamus iaculis dui in pretium mollis. Nulla massa diam,
          sagittis et est quis, aliquam interdum lorem. Curabitur finibus massa
          ac purus congue, a gravida tellus ultrices. Nullam eu dolor odio.
          Etiam iaculis odio lectus, at facilisis <<sapien posuere>> a.
          Suspendisse accumsan justo eu elit suscipit, dignissim viverra leo
          sagittis. Aliquam porttitor est in cursus sodales.
          """
          When we analyse the document
          Then the returned questions should be
              | question                    |
              | consectetur adipiscing elit |
              | ridiculus mus               |
              | Praesent                    |
              | sapien posuere              |
