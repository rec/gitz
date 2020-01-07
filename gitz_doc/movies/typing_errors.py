from . import constants
import random


def with_errors(line, error_rate=constants.TYPING_ERROR_RATE):
    random.seed(hash(line))

    for k in line:
        if random.random() < error_rate:
            errors = ERRORS.get(k)
            if errors:
                yield random.choice(errors)
                yield constants.BACKSPACE
        yield k


ERRORS = {
    'a': 'qzs',
    'b': ' vfghn',
    'c': ' xsdfv',
    'd': 'werfvcxs',
    'e': 'rfdsw',
    'f': 'ertgbvcd',
    'g': 'frtyhnbv',
    'h': 'gtyujmnb',
    'i': 'uolkj',
    'j': 'hyuikmnh',
    'k': 'juiol,mj',
    'l': 'kiop;.,',
    'm': 'nhjk, ',
    'n': 'bghjm ',
    'o': 'oikl;p',
    'p': 'ol;\'[-',
    'q': 'wa',
    'r': 'edfgt',
    's': 'aqwedcxz',
    't': 'rfghy',
    'u': 'yhjki',
    'v': 'cdfgb ',
    'w': 'qasde',
    'x': 'zasdc ',
    'y': 'tghju',
    'z': 'asx',
    '0': '9-',
    '1': '`2',
    '2': '13',
    '3': '24',
    '4': '35',
    '5': '46',
    '6': '57',
    '7': '68',
    '8': '79',
    '9': '80',
}
