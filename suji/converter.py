""" The entry point to the converter methods.

This provides a method to convert from japanese number notation to numerical value,
and a method to convert from a string with Japanese number notations to the numerical string.
"""
from suji.accumulator import Acc
from suji.char import Char

def values(src):
    """ Convert from Japanese number notation to numerical value.
    The return value is a list of result objects.
    If the input string has no number notation, `values` returns a empty list.
    The result object has three keys: `val`, `beg`, and `end`:

    :val: the numerical value of the number notation.
    :beg: the start postion of the found number notation at the input string.
    :end: the end postion of the found number notation.

    :param src: a input string.
    :return: a list of the numerical value objects.
    """
    acc = Acc()
    results = []

    for idx, char in enumerate(src):
        num = Char.get_number(char)
        cardinal = Char.get_cardinal(char)

        if num is not None:
            acc.attach_number(idx, num)
            continue

        if cardinal is not None:
            acc.attach_cardinal(idx, cardinal)
            continue

        if Char.is_delimiter(char) or Char.is_decimal_point(char):
            continue

        # If the current character is not related to a number and there was a accumulating
        # process happening before, it should be processed.
        if acc.inside:
            result = acc.get_value()
            if result['val'] is not None:
                results.append(result)

            acc = Acc()  # Initialize a new accumulator for any future sequences.

    # After finishing the loop, check one last time for any numbers that might not have been added.
    if acc.inside:
        result = acc.get_value()
        if result['val'] is not None:
            results.append(result)

    return results

def value(src):
    """ Convert from a string with Japanese number notations to the numerical string.
    The return value is a converted str.
    If the input string has no number notation, `value` returns the input string.

    :param src: a input string.
    :return: a converted str.
    """
    vals = values(src)
    if 0 == len(vals):
        return src
    start = 0
    s = ''
    for v in vals:
        s += src[start:v['beg']]
        s += str(v['val'])
        start = v['end']
    s += src[start:len(src)]
    return s
__all__ = ['values', 'value']