import readline

from matcher.matcher import Matcher, NoPersonalityException
from gender.gender import UnsupportedGenderCommandException
from age.age import UnsupportedAgeCommandException

def get_help():
    mat = "/match [m|f|n] [18-100] to match with a new partner in an age range.\n"
    hlp = "/help to see this printout\n"
    sav = "/save to save your current chat partner session to ./personality.dat\n"
    lod = "/load to bring back the saved chat partner session\n"
    ext = "/exit to ghost."
    return "%s%s%s%s%s" % (mat, hlp, sav, lod, ext)

def print_welcome():
    print("Welcome to Matchbot!\n%s" % get_help())

def main():
    done = False
    print_welcome()
    matcher = Matcher()
    conseq_failed_match_attempts = 0
    while(not done):
        line = input("> ")
        if line == "/exit":
            done = True
        elif line == "/help":
            print("\n%s\n" % get_help())
        elif line == "/save":
            print("Trying to save current chat partner: %s" % matcher.personality)
            try:
                matcher.save_personality()
                print("Save successful.")
            except NoPersonalityException:
                print("Failed. No active personality to save")
        elif line == "/load":
            try:
                matcher.load_personality()
                print("\t\tHi there! This is %s. It's great to see you again!" % matcher.personality.name)
            except NoPersonalityException:
                print("Missing personality.dat file in basedir")
        elif line.startswith("/match"): # TODO abstract this away
            try:
                name, years_old, gender = matcher.match(line)
                matcher.new_personality(name, years_old, gender)
                print("\nNow talking with %s!\n" % name) 
                conseq_failed_match_attempts = 0
            except (UnsupportedGenderCommandException, UnsupportedAgeCommandException) as e:
                print(e.msg)
                conseq_failed_match_attempts += 1
                if conseq_failed_match_attempts == 6:
                    conseq_failed_match_attempts = 1
                    print("You seem to be having trouble. I'll select a partner for you at random.")
                    name, years_old, gender = matcher.match_random()
                    matcher.new_personality(name, years_old, gender)
                    print("\nNow talking with %s!\n" % matcher.personality)                
        else:
            conseq_failed_match_attempts = 0
            if matcher.personality is None:
                print("You're not matched with anyone so nobody read that. Use /match")
            else:
                bot_line = matcher.personality_response(line)
                print("\n%s" % (bot_line))

if __name__ == "__main__":
    main()