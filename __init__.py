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
import sys

import pdb


log_file = '/tmp/history.log'
interact = False


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
    # 17-08-24 - removed 2nd arg to bytes for py2 compat
    return adler32(bytes(data))

def write_log(msg, log_it=None, print_=True, log=None):
    # 17-06-11
    global log_file
    if log: log_file = log

    with open(log_file, 'a') as lf:
        lf.write(msg + '\n')
    if print_: print(msg)
    if log_it: log_it(msg)
    return


from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

#from utils import *
#from abilities import *


__author__ = 'skeledrew'
LOGGER = getLogger(__name__)


class BrainSkill(MycroftSkill):

    def __init__(self):
        super(BrainSkill, self).__init__(name='BrainSkill')
        self.h_prefix = 'Dyn'

    def initialize(self):
        say_rx = 'say (?P<Words>.*)'
        self.add_ability(say_rx, self.handle_say_intent)
        self.add_ability('holla back', self.handle_holler_intent)
        #intent = 

    def add_ability(self, rx, handler):
        write_log('Binding "{}" to "{}"'.format(rx, repr(handler)), self.log.debug)
        intents = self.make_intents(rx)

        while intents:
            intent = intents.pop()
            self.register_intent(intent, handler)

    def handle_say_intent(self, msg):
        words = msg.data.get('Words')
        self.speak(words)

    def handle_holler_intent(self, msg):
        self.speak('Woo woooo')

    def make_intents(self, rx):
        rx_combos = expand_rx(rx.strip())
        intents = []
        if interact: pdb.set_trace()

        for combo in rx_combos:
            i_name = '{}{}Intent'.format(self.h_prefix, hash_sum(combo))

            if re.match('^[a-z0-9 ]+$', combo):
                # keywords only
                entity_type = self.make_entity_type(combo)
                intent = IntentBuilder(i_name).require(entity_type).build()
                intents.append(intent)
                continue
            self.register_regex(combo)
            parts = re.split('(\(|\))', combo)
            intent_builder = IntentBuilder(i_name)
            section = ''

            for idx in range(len(parts)):
                part = parts[idx]

                if section and part == '(':
                    # got a complete keyword
                    write_log('section: {}'.format(str(section)), self.log.debug)
                    entity = section.strip()
                    entity_type = self.make_entity_type(entity)
                    intent_builder.require(entity_type)
                    section = part
                    continue
                section += part
                match = re.match('\(\?<.+>\)', section)

                if match:
                    # got a named group
                    write_log('section: {}'.format(str(section)), self.log.debug)
                    rnge = match.span()
                    entity_type = combo[rnge[0]:rnge[1]]

                    if not idx == len(parts) - 1 and re.match('(\?|\*).*', parts[idx + 1]):
                        intent_builder.optionally(entity_type)

                    else:
                        intent_builder.require(entity_type)
                    continue
            intents.append(intent_builder.build())
            write_log('Created intent: {}'.format(str(intents[-1].__dict__)), self.log.debug)
        return intents

    def make_entity_type(self, entity):
        entity = entity.strip()
        entity_type = ''.join(entity.title().split(' ')) + 'Keyword' + 's' if ' ' in entity else ''
        self.register_vocabulary(entity, entity_type)
        return entity_type

class TestSkill(MycroftSkill):

    def __init__(self):
        super(TestSkill, self).__init__(name='TestSkill')

    def initialize(self):
        self.register_vocabulary('testing', 'TestingKeyword')
        testing_intent = IntentBuilder('TestingIntent').require('TestingKeyword').build()
        self.register_intent(testing_intent, self.handle_testing_intent)

    def handle_testing_intent(self, msg):
        self.speak('testing one two three')

def create_skill():
    #return TestSkill()
    return BrainSkill()


if sys.argv[0] == '' and not __name__ == '__main__':
    interact = True
