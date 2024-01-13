# matchbot
A command line chatbot where you can have a conversation, get to know each other, and see you can setup a date (or get rejected)

Requires Python 3.7+

## Quickstart:

1. Git clone this repo. CD to basedir location. 
2. `pip install -r requirements.txt`
3. Add matchbot basedir to PATH `export PATH=$PATH:/path/to/matchbot`
4. Add OpenAI API key to env `export OPEN_API_KEY=${API_KEY>}`
5. Run `matchbot`

## Commands

`/match [m|f|n] [18-100]`

Use to start a conversation with a new personality. Matchbot will auto generate this based on the gender specified
`m` (male) `f` (female) `n` (nonbinary). 

examples:
`/match f 25` --> female personality age 25.
`/match m 25-45` --> male personality between the age 25 and 45.
`/match n` --> non-binary personality between the age 18 and 100.

Age argument is optional. 

You can specify an exact age between `18` and `100` years old, or a range if you'd like to be
surprised. Format for range is dash-separated no spaces I.E. `25-45`.

`/save` to save the personality to `./saved_personality.dat`. This will let you reload later. This will overwrite any existing file with that name, so be sure to backup to a different location if you really don't want to lose the match!

`/load` to restore a personality for conversation using the file `./saved_personality.dat`

`/debug` to see details about the personality you're talking to, including current disposition. (hint: it's more fun if you don't use this).

`/help` --> print this menu

`/exit` to leave matchbot

## How it works

When matchbot creates a personality for conversation, it autogenerates a few random interests and personality traits from the data sources below. Some language processing is done to make sure randomly assigned personality traits don't conflict. E.G. A personality will not be both happy and sad, or funny and boring.

Where the conversation goes from here is up to the user. 

Depending on how you talk with the personality it will gradually increase/decrease their opinion of you. Being overly crude, mean, and/or discussing topics that don't align with their interest will have a decreased effect. 

If their opinion of you gets low enough they'll suggest you talk with another person. There's a very low (but not zero) chance of recovering the conversation from here.

If the opinion gets really low, the personality will automatically unmatch you.

If you have a meaningful conversation and the personality's opinion of you gets high enough, they'll start suggesting you go on a date. Nice work!

You can see how the personality currently feels about you by running `/debug` and observing the disposition between 0.0 and 100. Where 0 is a very negative opinion, and 100 is perfect.

## Design

launch_cli.py is the top level module with the user input loop. All printouts to the user are done here. 
Any checked exceptions bubble up to this layer as well to printout a meaningful message to the user. This was done to prevent randomly scattered print() logs all over the codebase.

Once the user asks for a match, a random personality is generated that matches the user's preference for gender and age. The gender component takes in the raw /match command from the user and responds with the `gender, name`. Where name is randomly generated based on the gender. The age component does the same thing but responds with just `years_old`.

From here a personality construct is created using `gender`, `name`, `years_old` and some randomly selected interests and non-conflicting personality traits. Male and female names are selected from the language processing library's names module. Nonbinary names, personality traits, and interests all come from the data sources cited below.

From here forward, interaction between the user and personality involves three distinct design components. The matcher, the personality, and the responder.

### Matcher

Handles operations around generation and persistance of personalities. The matcher is where the responder is instantiated and given a reference to the current personality. It's also where user messages are forwarded to the responder to generate a response back to the user. Ghosting is not a behavior encoded into the personalities, although maybe I should?

### Personality

Contains the details of the match. Currently includes: age, gender, current opinion of you, interests, and personality traits. This will be expanded on over time (see roadmap section)

### Responder

Takes a reference to the personality. When a user sends a message to the personality, the responder's job is to take that input and generate effective generativeAI prompts, based largely on the current details and traits within that personality. Currently there are only these responder types impemented:

1. GPTResponder: OPenAI gpt 3.5 turbo model.
2. Echo responder used only to printout the personality details for debugging.

Response will include as the last sentance a score between 0.0 and 100 of how the personality felt about the message they just received. This is to help the personality track their opinion of you as the conversation progresses. The responder contains some custom language processing code to parse this out of the response before forwarding the rest of the response to the user. If for some reason the responder can't find the disposition score in the response, just send the response as-is and leave their current opinion of you unchanged.

### Conversation flow design diagram

![title](design_images/matchbot_conversion_flow.png)

## Next steps

* Advanced memory contained within personality to help dynamically generate prompt sections.
* Move disposition to memory.
* Remember your name in memory. 
* Get frustrated if the person keeps repeating themselves or asking the same questions over and over.
* If bot asks them on a date and they say yes, don't keep suggesting a date. Start talking about how they can't wait to see you.

## Run tests

`pytest tests`

## Data Sources

### Personality traits

https://argoprep.com/blog/206-personality-adjectives-to-describe-anybody/

### Nonbinary names

https://nameberry.com/list/851/nonbinary-names/all

### Interests

https://en.wikipedia.org/wiki/List_of_hobbies