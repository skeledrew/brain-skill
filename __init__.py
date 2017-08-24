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


from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

from utils import *
from abilities import *


__author__ = 'skeledrew'
LOGGER = getLogger(__name__)


class BrainSkill(MycroftSkill):

    def __init__(self):
        self.h_prefix = 'Dyn'

    def initialize(self):
        say_rx = 'say (?P<Words>.*)'
        self.add_ability(say_rx, self.handle_say_intent)

    def add_ability(rx, handler):
        intents = self.make_intents(rx)

        while intents:
            intent = intents.pop()
            self.register_intent(intent, handler)

    def handle_say_intent(self, msg):
        words = msg.data.get('Words')
        self.speak(words)

    def make_intents(self, rx):
        rx_combos = expand_rx(rx.strip())
        intents = []

        for combo in rx_combos:
            self.register_regex(combo)
            parts = re.split('(\(|\))', combo)
            i_name = '{}{}Intent'.format(self.h_prefix, hash_sum(combo))
            intent_builder = IntentBuilder(i_name)
            section = ''

            for idx in range(len(parts)):
                part = parts[idx]

                if section and part == '(':
                    # got a complete keyword
                    entity = section.strip()
                    entity_type = ''.join(entity.title().split(' ')) + 'Keyword'
                    self.register_vocabulary(entity, entity_type)
                    intent_builder.require(entity_type)
                    section = part
                    continue
                section += part
                match = re.match('\(\?<.+>\)')

                if match:
                    # got a named group
                    rnge = match.span()
                    entity_type = combo[rnge[0]:rnge[1]]

                    if not idx == len(parts) - 1 and re.match('(\?|\*).*', parts[idx + 1]):
                        intent_builder.optionally(entity_type)

                    else:
                        intent_builder.require(entity_type)
                    continue
            intents.append(intent_builder.build())
        return intents

def create_skill():
    return BrainSkill()
