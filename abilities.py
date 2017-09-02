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
import subprocess as sp

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
    this.speak('Starting web interface')
    this.log.debug('Interface started')
    sp.check_output(['python3', 'remiface.py'], shell-True)
    this.speak('Web interface closed')

def morning_report(this=None, msg=None):
    # mainly test and demo purposes
    if not this: return 'good morning' #[{'lang': 'en-us', 'utterances': ['good morning']}]
    chain = []
    chain.append({'target': 'SpeakSkill:SpeakIntent', 'data': {'Words': 'good morning'}, 'context': None})
    chain.append(['shout', 'what time is it'])
    chain.append(['shout', 'what is the weather'])
    this.exec_chain(chain)

def whisper(this=None, msg=None):
    # direct query to a particular skill/intent; should prob not register
    pattern = 'call intent (?P<Intent>.+) in skill (?P<Skill>.+) with data (?P<Data>.+)( and context )?(?P<Context>.+)?'
    if not this and not msg: return None #pattern
    data = {}

    if isinstance(msg, str) and re.search(pattern, msg):
        match = re.match(pattern, msg)
        skill_id = match.group('Skill')
        skill_id = ''.join(skill_id.title().split(' '))
        intent_name = match.group('Intent')
        intent_name = ''.join(intent_name.title().split(' '))
        target = '{}:{}'.format(skill_id, intent_name)
        data = match.group('Data')  # massage string into a dict
        data = re.sub(' *and *', '&', re.sub(' *equal *', '=', data))
        data = {key: value for key, value in [[d.split('=')[0], d.split('=')[1]] for d in data.split('&')]}
        context = match.group('Context') #if 'Context' in msg.data else None
        this.log.info('Generated message params: target = {}, data = {}, context = {}'.format(target, data, context))
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

def shout(this=None, utterances=None):
    # broadcast query so any skill/intent can handle
    if not this: return None  # prevent addition as ability

    if not type(utterances) in [str, list]:
        this.log.error('Expected string or list, got: {} which is {}'.format(repr(utterances), str(type(utterances))[1:-1]))
        return None
    if isinstance(utterances, str): utterances = [utterances.strip()]
    this.emitter.emit(Message("recognizer_loop:utterance", {"lang": "en-us", "utterances": utterances}))
    return True

def core_version(this=None, msg=None):
    if not this: return 'what version are you'
    import mycroft.version
    this.speak(mycroft.version.CORE_VERSION_STR)

def core_update(this=None, msg=None):
    # TODO: needs sudo workaround
    return None  # disable
    if not this: return 'upgrade yourself'
    this.speak('I will now attempt to upgrade to the latest version')
    out = ''
    try:
        out = sp.check_output(['sudo', 'apt-get', 'update'], shell=True)
    except Exception as e:
        this.log.debug('Update failed: {}'.format(repr(e)))
        this.speak('Update failed. Please see log for details.')
        return
    this.log.info('Update tail = {}'.format('\n\t\t'.join(out.split('\n')[-5:])))
    out = sp.check_output('sudo apt-get install --only-upgrade mycroft-core mimic -y'.split(' '))
    this.log.info('Upgrade tail = {}'.format(out))
