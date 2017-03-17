class Config:
    def __init__(self):
        self.defaultonderwerptekst = ""
        self.defaultondertekenaar = ""
        self.defaultfunctieondertekenaar = ""
        self.defaultbijlageuploaden = ""
        self.defaultmedischecategorie = "Medisch Declaratie"

    def get_value(self, key, string):
        """
        Gets the values for a key (if the strings contains that key at all)
        Args:
            key(str): The string for the key. E.g. 'defaultonderwerptekst'
            string(str): The string. E.g. 'defaultbijlageuploaden ja'
        Returns:
            The value (E.g. 'ja') if the string contains the key, or None
            otherwise
        """
        if string.startswith(key):
            if len(string) > len(key):
                return string[len(key) + 1:]
            else:
                return ''
        return None

    def parse_defaults(self, attributes):
        parsed_attributes = []
        for attr in attributes:
            onderwerptekst = self.get_value('defaultonderwerptekst', attr)
            ondertekenaar = self.get_value('defaultondertekenaar', attr)
            functieondertekenaar = self.get_value('defaultfunctieondertekenaar',
                                                  attr)
            bijlageuploaden = self.get_value('defaultbijlageuploaden', attr)
            medischecategorie = self.get_value('defaultmedischecategorie', attr)

            if onderwerptekst is not None:
                self.defaultonderwerptekst = onderwerptekst
                parsed_attributes += [attr]

            if ondertekenaar is not None:
                self.defaultondertekenaar = ondertekenaar
                parsed_attributes += [attr]

            if functieondertekenaar is not None:
                fo = functieondertekenaar
                self.defaultfunctieondertekenaar = fo[0].upper() + fo
                parsed_attributes += [attr]

            if bijlageuploaden is not None:
                self.defaultbijlageuploaden = bijlageuploaden.lower() == 'ja'
                parsed_attributes += [attr]

            if medischecategorie is not None:
                mc = medischecategorie
                self.defaultmedischecategorie = mc[0].upper() + mc
                parsed_attributes += [attr]

        return [attr for attr in attributes if attr not in parsed_attributes]
