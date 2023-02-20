# matchbot
A command line chatbot where you can have a conversation, get to know each other, and see you can setup a date (or get rejected)

Requires Python 3+

## Steps to start matchin':

1. Git clone this repo. CD to basedir location. 
2. `pip install -r requirements.txt`
3. `python bootstrap.py` One time setup of nltk per local machine.
4. Add matchbot git clone basedir to PATH `export PATH=$PATH:/path/to/matchbot`
5. Add OpenAI API key to env `export OPEN_API_KEY=${API_KEY>}`
6. Run `matchbot` to start the cli.

## Tests

`pytest tests`

## Design

TODO

## Data Sources

### Personality traits

https://argoprep.com/blog/206-personality-adjectives-to-describe-anybody/

### Nonbinary gender mames

https://nameberry.com/list/851/nonbinary-names/all

### Interests

https://en.wikipedia.org/wiki/List_of_hobbies