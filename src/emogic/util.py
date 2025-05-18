from collections.abc import Sequence
from typing import Any


def cs(emoji: Sequence[str] | Any) -> str:
    """Get the codepoint sequence from a sequence of characters.

    The codepoint sequence is a string of hexadecimal numbers separated by `-`.
    It is used to represent the codepoints of the characters in the emoji.

    For example, the codepoint for "👨‍👩‍👧" is `1f468-200d-1f469-200d-1f467`.

    :param emoji: The emoji to get the codepoint for.
    :type emoji: str

    :return: The codepoint of the emoji.
    :rtype: str
    """
    return "-".join(format(ord(c), "x") for c in emoji)


def anything(list: list) -> Any:
    """Return a list without None values.

    :param list: The list to filter.
    :type list: list

    :return: The filtered list.
    :rtype: list
    """
    return [x for x in list if x is not None]
