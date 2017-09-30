## Brain Skill
Basic services and automation for skills.

## Description 
Essentially [Tasker](http://tasker.dinglisch.net/) for [Mycroft AI](https://mycroft.ai/), to help automate ALL THE THINGS. 'nuff said. NB: This is an early work in progress.

## Examples 
* "announce I have so much potential"
* "brain scan"

## Installation
* Setup Mycroft on a Linux desktop, build on a Pi, or purchase a Mark 1
* Run `msm install https://github.com/skeledrew/brain-skill.git` or say "hey mycroft... install brain skill"
* Run `cd ~/skills/brain-skill && sudo bash requirements.sh`
* Run `sudo pip install -r requirements.txt` to ensure PyPI modules are installed

## Usage:
* Echo whatever you want it to
  * "announce I have so much potential"
* Test to see if anything went wrong that was caught
  * "brain scan"
* Reload abilities
  * "reload abilities"
* Eye actions
  * "reset eyes" ^
  * "look up/down/left/right/crossed" ^
  * "set brightness to N" ^ (N = 1-30)
  * "eye color ColorName" ^ (valid names: http://www.w3.org/TR/css3-color/#svg-color)
* Check core version
  * "what version are you"
  * "search skill log for SearchTerm" (not for instances with voice output)
* Create thought chains in settings.json to execute multiple abilities at a single keyword/phrase (will be voice automated soon)
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
* `[^] Mark 1 enclosure specific`

## Known Bugs, Quirks & Limits
* Can't think of any!

## To Do
* learn spelling and chain abilities by voice
* resource downloader
* web API wrapper
* autogenerate regex, vocab files
* help system
* webserver
* event triggers and state management

## Credits 
skeledrew