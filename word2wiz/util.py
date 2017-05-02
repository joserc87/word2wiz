

def parse_mark(mark, tag, separator=None):
    """
    Returns a Step representing the mark, or null if it's not a Step mark.
    Args:
        mark (str): The mark to parse, e.g. 'step myStep'
        tag (str): The expected begining of th emark, e.g. 'step'
        separator (str): The separator, e.g. ';', or None if there is none
    Returns:
        The rest of the mark stripped, or null if the tag didn't match
    """
    if mark.startswith(tag + ' '):
        mark = mark[len(tag):]
        if separator is None:
            return mark.strip()
        else:
            parts = mark.split(separator)
            return [part.strip() for part in parts]
    else:
        # If it does not match, return none
        return None
