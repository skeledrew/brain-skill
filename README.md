# Mycroft Brain Skill


## Description
Essentially [Tasker](http://tasker.dinglisch.net/) for [Mycroft AI](https://mycroft.ai/), to help automate ALL THE THINGS. 'nuff said. NB: This is an early work in progress.

## Installation
- Setup Mycroft on a Linux desktop, build on a Pi, or purchase a Mark 1
- Run `msm install https://github.com/skeledrew/brain-skill.git` or say "hey mycroft... install brain skill"

## Usage:
- Echo whatever you want it to
  - "hey mycroft... say I have so much potential"
- Quick test
  - "hey mycroft... holla back"
- Reload abilities
  - "hey mycroft... reload abilities"
- Another test
  - "hey mycroft... ping"
- Eye actions
  - "hey mycroft... reset eyes" *
  - "hey mycroft... look up/down/left/right/crossed" *
  - "hey mycroft... set brightness to N" * (N = 1-30)
  - "hey mycroft... eye color ColorName" * (valid names: http://www.w3.org/TR/css3-color/#svg-color)
- Check core version
  - "hey mycroft... what version are you"
- Create thought chains in settings.json to execute multiple abilities at a single keyword/phrase (will be voice automated soon)
``` json
{
    "thot_chains":
    {
        "play some blues on pandora":
        [
            ["shout", "play pandora"],
            ["shout", "play blues radio"]
        ],
        "chicago weather":
        [
            ["shout", "what is the weather in chicago"]
        ],
        "rainbow eyes":
        [
            ["shout", "eye color red"],
            ["shout", "eye color orange"],
            ["shout", "eye color yellow"],
            ["shout", "eye color green"],
            ["shout", "eye color blue"],
            ["shout", "eye color indigo"],
            ["shout", "eye color violet"]
        ],
    }
}
```
- `* Mark 1 enclosure specific`

## Known Bugs, Quirks & Limits
- Can't think of any!

## To Do
- learn spelling and chain abilities by voice
- resource downloader
- web API wrapper
- autogenerate regex, vocab files
- help system
- webserver
- event triggers and state management