# Brain Skill

## Usage:
- Echo whatever you want it to
  - say I have so much potential
- Quick test
  - holla back
- reload abilities
- Another test
  - ping
- Eye actions
  - reset eyes *
  - look up/down/left/right/crossed *
  - set brightness to N * (N = 1-30)
  - eye color ColorName (valid names: http://www.w3.org/TR/css3-color/#svg-color)
- what version are you
- `* Mark 1 enclosure`
- Create chains in settings.json to execute multiple actions at a single keyword (will be automated soon)
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
        ]
    }
}
```

## Known Bugs, Quirks & Limits
- External speaking is repeated sometimes

## To Do
- learn spelling and new ability
- resource downloader
- autogenerate regex, vocab files
- help system