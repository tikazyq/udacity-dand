# -*- coding: utf-8 -*-

"""
UK Postcode manipulation

Port of https://github.com/threedaymonk/uk_postcode

See http://www.freemaptools.com/download-uk-postcode-lat-lng.htm
"""

import re
from collections import namedtuple


PATTERN = r'''(?:
    ( G[I1]R \s* [0O]AA )           # special postcode
  |
    ( [A-PR-UWYZ01][A-Z01]? )       # area
    ( [0-9IO][0-9A-HJKMNPR-YIO]? )  # district
    (?: \s*
      ( [0-9IO] )                   # sector
      ( [ABD-HJLNPQ-Z10]{2} )       # unit
    )?
)$'''


postcode_tuple = namedtuple('Postcode', 'raw,area,district,sector,unit')


class Postcode(postcode_tuple):
    __slots__ = ()

    @property
    def outcode(self):
        return self.area + self.district

    @property
    def incode(self):
        if self.sector is not None and self.unit is not None:
            return self.sector + self.unit

    @property
    def full(self):
        return bool(self.outcode and self.incode)

    @property
    def normalised(self):
        return ' '.join(p for p in (self.outcode, self.incode) if p).upper()


def _letters(s):
    """Replace common digit-instead-of-alpha mistakes"""
    if s:
        return s.replace('10', 'IO')


def _digits(s):
    """Replace common alpha-instead-of-digit mistakes"""
    if s:
        return s.replace('IO', '10')


def validate(raw_postcode, incode_required=False):
    r = raw_postcode.strip().upper()
    match = re.match(PATTERN, r, re.VERBOSE | re.IGNORECASE)
    if not match:
        return None

    matches = match.groups()

    if matches[0]:
        parts = ['G', 'IR', '0', 'AA']

    else:
        parts = matches[1:]

        if incode_required:
            if not parts[2] and not parts[3]:
                return None

        if re.match('^[A-Z][1I]$', parts[0]):
            parts[0] = parts[0][0]
            parts[1] = '1' + parts[1]

        parts = [_letters(parts[0]), _digits(parts[1]), _digits(parts[2]), _letters(parts[3])]

    return Postcode(raw_postcode, *parts)
