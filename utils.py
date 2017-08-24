# This file is part of brain-skill

# brain-skill - This is a Mycroft skill that is intended to be dynamically extensible and modifiable.

# @author Andrew Phillips
# @copyright 2017 Andrew Phillips <skeledrew@gmail.com>

# brain-skill is free software; you can redistribute it and/or
# modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
# License as published by the Free Software Foundation; either
# version 3 of the License, or any later version.

# brain-skill is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU AFFERO GENERAL PUBLIC LICENSE for more details.

# You should have received a copy of the GNU Affero General Public
# License along with brain-skill.  If not, see <http://www.gnu.org/licenses/>.


import re, itertools

import pdb


def expand_rx(rx, ignore_named_groups=True):
    # 17-08-24
    poss = [0]  # initialized positions
    rxs = []
    level = 0
    named = []

    for idx in range(len(rx)):
        # mark targeted group points

        if rx[idx] == '(':
            level += 1

            if not rx[idx+1] == '?':
                # regular group
                poss.append(idx)

            else:
                # may need to avoid named groups
                named.append(idx)
            continue

        if rx[idx] == ')':

            if ignore_named_groups and named:
                if level == named[-1]: named.pop(-1)

            else:
                poss.append(idx)
            level -= 1
            continue
    poss.append(len(rx))
    start = poss.pop(0)
    parts = []

    while poss:
        end = poss.pop(0)
        parts.append(rx[start:end])
        start = end + 1
    parts = [part.split('|') for part in parts]

    for prod in itertools.product(*parts):
        rxs.append(''.join(prod))
    return rxs

def hash_sum(data):
    # 17-08-24
    return adler32(bytes(data, 'utf-8'))

