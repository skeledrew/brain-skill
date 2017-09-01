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


import re, time

from mycroft.messagebus.message import Message


def blank(this=None, msg=None):
    if not this: return 'ability template'
    this.speak('Please copy this template to make your own abilities')

def ping(this=None, msg=None):
    if not this: return 'ping'
    this.speak('I\'m here!')

def learn(this=None, msg=None):
    if not this: return 'learn new ability'
    return

def reset_eyes(this=None, msg=None):
    if not this: return 'reset eyes'
    this.enclosure.eyes_reset()

def red_eyes(this=None, msg=None):
    # doesn't work
    if not this: return 'red eyes'
    this.enclosure.eyes_color(255, 0, 0)

def look(this=None, msg=None):
    if not this: return 'look (?P<Where>\w+)'
    where = msg.data.get('Where')
    this.enclosure.eyes_look(where[0])

def illum(this=None, msg=None):
    #return None  # don't load
    if not this: return 'set brightness to (?P<Amount>\d+)' #'(set|increase|decrease) (illumination|brightness) (to|by)? (?P<Amount>\d+)?( percent)?'
    command = msg.data.get('utterance')
    level = 0

    if re.search('set \w+ to \d+.*', command):
        # set brightness
        level = 30
        if 'Amount' in msg.data: level = int(msg.data.get('Amount'))  # TODO: handle numbers as words
        if re.search('.*percent$', command): level = int(level / 100 * 30)
        this.log.debug('brightness; data = {}; level = {}'.format(repr(msg.data), level))
        if level < 1: level = 1
        if level > 30: level = 30

    else:
        # increase/decrease
        pass
    this.enclosure.eyes_brightness(level)

def start_web_server(this=None, msg=None):
    if not this: return 'start remote interface'
    import remi
    reload(remi)

def morning_report(this=None, msg=None):
    if not this: return 'good morning' #[{'lang': 'en-us', 'utterances': ['good morning']}]
    chain = []
    chain.append({'type': 'SpeakSkill:SpeakIntent', 'data': {'Words': 'good morning'}, 'context': None})
    #this.speak('good morning!')
    #time.sleep(2)
    chain.append({'type': 'recognizer_loop:utterance', 'data': {'lang': 'en-us', 'utterances': ['what time is it']}, 'context': None})
    #shout(this, 'what time is it')
    #time.sleep(2)
    #whisper(this, {'type': 'WeatherSkill:CurrentWeatherIntent', 'data': {'utterance': 'what is the weather', 'Weather': 'weather'}})

def whisper(this=None, msg=None):
    # direct query to a particular skill/intent; should prob not register
    if not this and not msg: return 'call intent (?P<Intent>.+) in skill (?P<Skill>.+) with data (?P<Data>.+)( and context )?(?P<Context>.+)?'
    if isinstance(msg, Message) and 'Intent' in msg.data:
        skill_id = msg.data.get('Skill')
        intent_name = msg.data.get('Intent')
        data = msg.data.get('Data')  # massage string into a dict
        target = '{}:{}'.format(skill_id, intent_name)
        context = msg.data.get('Context') if 'Context' in msg.data else None
        this.emitter.emit(Message(target, data, context))
        return

    elif isinstance(msg, dict) and 'target' in msg:
        # called as a regular function
        target = msg['target']
        data = msg['data']
        context = msg['context'] if 'context' in msg else None
        this.emitter.emit(Message(target, data, context))
        return
    this.log.error('Unable to process message: {}'.format(repr(msg)))

def shout(emitter=None, utterances=None):
    # broadcast query so any skill/intent can handle
    if not utterances: return None  # prevent addition as ability
    if not type(utterances) in [str, list]: return None
    if isinstance(utterances, str): utterance = [utterances]
    emitter.emit(Message("recognizer_loop:utterance", {"lang": "en-us", "utterances": [utterances]}))
    return True

def version(this=None, msg=None):
    if not this: return 'what version are you'
    import mycroft.version
    this.speak(mycroft.version.CORE_VERSION_STR)
