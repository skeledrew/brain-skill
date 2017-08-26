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


interact = False


import sys
from os.path import dirname, abspath

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

sys.path.append(abspath(dirname(__file__)))  # local imports hack

import utils
reload(utils)  # py2 method

for name in dir(utils):
    # unpack
    if not '__' in name: exec('{0} = getattr(utils, "{0}")'.format(name))
import abilities
reload(abilities)


__author__ = 'skeledrew'
__version__ = '0.2.1'
LOGGER = getLogger(__name__)


class BrainSkill(MycroftSkill):

    def __init__(self):
        super(BrainSkill, self).__init__(name='BrainSkill')
        self.h_prefix = 'Dyn'
        self.bridged_funcs = {}

    def initialize(self):
        say_rx = 'say (?P<Words>.*)'
        self.add_ability(say_rx, self.handle_say_intent)
        self.add_ability('holla back', self.handle_holler_intent)
        self.add_ability('reload abilities', self.reload_abilities)
        self.load_abilities()

    def add_ability(self, rx, handler):
        self.log.info('Binding "{}" to "{}"'.format(rx, repr(handler)))
        intents = self.make_intents(rx)

        while intents:
            intent = intents.pop()
            self.register_intent(intent, handler)

    def reload_abilities(self, msg):
        reload(abilities)
        self.load_abilities()
        self.speak('abilities reloaded!')

    def load_abilities(self):
        # load core and pipes

        for abl in dir(abilities):
            # core abilities
            if '__' in abl: continue
            abl = getattr(abilities, abl)
            rx = abl()
            self.bridged_funcs[rx] = abl
            self.add_ability(rx, self.handle_external_intent)

    def handle_external_intent(self, msg):
        # bridge to function
        self.log.debug('bridging; m_data = {}'.format(repr(msg.data)))
        ext_func = None
        utt = msg.data['utterance']

        for rx in self.bridged_funcs:
            self.log.debug('searching for correct bridge; rx = {}; utt = {}'.format(rx, utt))
            if not re.match(rx, utt): continue
            ext_func = self.bridged_funcs[rx]
            break
        ext_func(self, msg)

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
                intent = IntentBuilder(re.sub('Keywords?', 'Intent', entity_type)).require(entity_type).build()
                intents.append(intent)
                continue
            self.register_regex(combo)
            parts = re.split('(\(|\))', combo)
            intent_builder = IntentBuilder(i_name)
            section = ''

            for idx in range(len(parts)):
                # separate keywords from names
                part = parts[idx]

                if section and part == '(':
                    # got a complete keyword
                    entity_type = self.make_entity_type(section)
                    intent_builder.require(entity_type)
                    section = '('
                    continue
                section += part
                match = re.match('\(\?P<\w+>.+\)', section)

                if match:
                    # got a named group
                    span = re.search('<\w+>', section).span()
                    entity_type = section[span[0]+1:span[1]-1]

                    if not idx == len(parts) - 1 and re.match('(\?|\*).*', parts[idx + 1]):
                        intent_builder.optionally(entity_type)

                    else:
                        intent_builder.require(entity_type)
                    section = ''
                    continue
            intents.append(intent_builder.build())
            self.log.info('Created intent: {}'.format(str(intents[-1].__dict__)))
        return intents

    def make_entity_type(self, entity):
        entity = entity.strip()
        entity_type = ''.join(entity.title().split(' ')) + 'Keyword' + ('s' if ' ' in entity else '')
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
    return BrainSkill()


if sys.argv[0] == '' and not __name__ == '__main__':
    interact = True # for pdb trace activation
