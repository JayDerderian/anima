'''
module for dealing with meters'''


valid_beats = [1, 2, 4, 8, 16, 32, 64]


def is_valid(meter):
    '''returns True if meter is valid (rational)'''
    return meter[0] > 0 and valid_beat_duration(meter)


def valid_beat_duration(meter):
    '''returns True if meter denominator is a valid beat duration'''
    return True if meter[1] in valid_beats else False


def is_simple(meter):
    '''returns True if meter is a simple meter'''
    return is_valid(meter)


def is_compound(meter):
    '''returns True if meter is a compound meter'''
    return is_valid(meter) and meter[0] % 3 == 0 and 6 <= meter[0]