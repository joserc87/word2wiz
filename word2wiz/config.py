class Config:
    """
    Contains the configuration values parsed from the word document
    """
    def __init__(self):
        # Transformations:
        def none(s): return s

        def capitalize(s): return s[0].upper() + s[1:]

        def parsebool(s): return s.lower() == 'ja'

        self.attributes = {
            'defaultonderwerptekst': none,
            'defaultondertekenaar': none,
            'defaultfunctieondertekenaar': capitalize,
            'defaultbijlageuploaden': parsebool,
            'defaultmedischecategorie': capitalize
        }

        # Default values
        self.defaultonderwerptekst = ""
        self.defaultondertekenaar = ""
        self.defaultfunctieondertekenaar = ""
        self.defaultbijlageuploaden = False
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
            return string[len(key) + 1:]
        return None

    def parse_defaults(self, attributes):
        parsed_attributes = []
        updates = {}
        for attr in attributes:
            for key, transformation in self.attributes.items():
                if attr.startswith(key):
                    value = self.get_value(key, attr)
                    value = transformation(value)
                    updates[key] = value
                    parsed_attributes += [attr]
        self.__dict__.update(updates)

        return [attr for attr in attributes if attr not in parsed_attributes]
