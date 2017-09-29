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
from zlib import adler32
import pdb
import sys
import json
from os.path import exists, dirname, abspath
from threading import Timer
from copy import deepcopy
import inspect

from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)
interact = False


class SkillSettings():

    def __init__(self, path):
        self._path = dirname(path) + '/settings.json'
        self._settings = self._old_settings = {}
        if exists(self._path): self._load()
        self._interval = 5
        self.timer = Timer(self._interval, self._save)

    def read(self, key):
        return self._settings[key] if key in self._settings else None

    def write(self, key, value):
        self._settings[key] = value

    def _load(self):
        with open(self._path) as fo:
            self._settings = json.load(fo)
        self._old_settings = deepcopy(self._settings)

    def _save(self):
        if self.timer.is_alive(): self.timer.cancel()
        self.timer = Timer(self._interval, self._save)
        if self._settings == self._old_settings: return
        with open(self._path, 'w') as fo:
            json.dump(self._settings, fo)
        self._old_settings = deepcopy(self._settings)


def expand_rx(rx, ignore_named_groups=True):
    # 17-08-24
    # -26 - fixed bug and compressed
    poss = [0]  # initialized positions
    rxs = []
    level = 0
    named = []
    '''if interact: pdb.set_trace()

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
        start = end + 1'''
    ###
    parts = re.split(r'\((.*?)\)', rx)
    parts = [['(%s)' % p for p in part.split('|')] if i % 2 else [part] for i, part in enumerate(parts)]

    for prod in itertools.product(*parts):
        rxs.append(''.join(prod))
    return rxs

def hash_sum(data):
    # 17-08-24 - remove 'utf-8' arg from bytes for py2 compat
    return adler32(bytes(data))

def bind_func(func, inst, name=''):
    # bind a function to a class as a method
    if not name: name = func.__name__
    setattr(inst, name, func.__get__(inst, inst.__class__))
    return func

def str_to_dict(s, main_sep='&', map_sep='=', use_re=False):
    # 17-09-29 - from common.py
    final = {}
    items = s.split(main_sep) if not use_re else re.split(main_sep, s)

    for item in items:
        item = item.split(map_sep) if not use_re else re.split(map_sep, item)
        final[item[0]] = item[1] if len(item) == 2 else None
    return final

def get_file(obj):
    # TODO: make more robust with errorchecks
    fn = None

    try:
        fn = inspect.getsourcefile(obj)
        if not '/' in fn or len(fn) < 4: raise TypeError('bad path')

    except TypeError:
        fn = abspath(obj.__module__)
    return fn

if sys.argv[0] == '' and not __name__ == '__main__':
    # running as an import
    interact = True # for pdb trace activation
    print('pdb debugging activated')

if __name__ == '__main__':
    print('Nothing to run directly here...')
