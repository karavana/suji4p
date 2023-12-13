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

    for index, char in enumerate(src):
        number = Char.get_number(char)
        if number is not None:
            acc.attach_number(index, number)
            continue

        cardinal = Char.get_cardinal(char)
        if cardinal is not None:
            acc.attach_cardinal(index, cardinal)
            continue

        if Char.is_decimal_point(char):
            acc.turn_to_decimal_state(index)
            continue

        if acc.inside:
            acc.inside = False
            results.append(acc.get_value())

        if Char.is_delimiter(char):
            continue

        acc.__val_cardinal = 0

    if acc.inside:
        acc.inside = False
        results.append(acc.get_value())

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