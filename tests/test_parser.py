# -*- coding: utf-8 -*-

import pytest
from cron_parser.parser import interpret_value

__author__ = "kewei"
__copyright__ = "kewei"
__license__ = "mit"


def test_parser():
    #Test to output all the times
    assert interpret_value('*', 'min') == '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 '
    assert interpret_value('*', 'hour') == '0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 '
    assert interpret_value('*', 'day_m') == '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 '
    assert interpret_value('*', 'month') == '1 2 3 4 5 6 7 8 9 10 11 12 '
    assert interpret_value('*', 'day_w') == '1 2 3 4 5 6 7 '
    
    #Test to only show the sensible results when only Feburary or Short months appear
    assert interpret_value('*', 'day_m', 1) == '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 '
    assert interpret_value('*', 'day_m', 2) == '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 '

    #Test to cover all the complex situations that can cover all the branches
    assert interpret_value('*/15', 'min') == '0 15 30 45 '
    assert interpret_value('1-5', 'day_w') == '1 2 3 4 5 '
    assert interpret_value('1-5/2', 'day_w') == '2 4 '
    assert interpret_value('*/2', 'day_w') == '2 4 6 '
    assert interpret_value('*/2,7', 'day_w') == '2 4 6 7 '

    #Test to catch all the Errors
    with pytest.raises(ValueError):
        interpret_value('*', 'unexpected_input')
    with pytest.raises(ValueError):
        interpret_value('0-5/2', 'day_w')
    with pytest.raises(ValueError):
        interpret_value('1-9/2', 'day_w')
    with pytest.raises(ValueError):
        interpret_value('1-a', 'day_w')
    with pytest.raises(ValueError):
        interpret_value('5-1', 'day_w')
    with pytest.raises(ValueError):
        interpret_value('5/2', 'day_w')
    with pytest.raises(ValueError):
        interpret_value('a', 'day_w')
