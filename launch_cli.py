import readline

from matcher.matcher import Matcher, NoPersonalityException, UnmatchedException, UnableToFindMatchException
from gender.gender import UnsupportedGenderCommandException
from age.age import UnsupportedAgeCommandException

def get_help():
    mat = "/match [m|f|n] [18-100] to match with a new partner in an age range.\n"
    hlp = "/help to see this printout\n"
    sav = "/save to save your current chat partner session to ./personality.dat\n"
    lod = "/load to bring back the saved chat partner session\n"
    deb = "/debug to see details about the current personality you're talking to.\n"
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
                print("Reconnecting with " + matcher.personality.name)
                print(matcher.welcome_back())
            except NoPersonalityException:
                print("Missing personality.dat file in basedir")
        elif line.startswith("/match"):
            try:
                print("\nLooking for a match....")
                matcher.new_personality(line)
                print("\nNow talking with %s!\n" % matcher.personality.name) 
                conseq_failed_match_attempts = 0
            except (UnsupportedGenderCommandException, UnsupportedAgeCommandException) as e:
                print(e.msg)
                conseq_failed_match_attempts += 1
                if conseq_failed_match_attempts == 6:
                    conseq_failed_match_attempts = 1
                    print("You seem to be having trouble. I'll select a partner for you at random.")
                    matcher.new_random_personality()
                    print("\nNow talking with %s!\n" % matcher.personality.name)
            except (UnableToFindMatchException):
                print("So sorry but we couldn't find a match. Try again.")

        
        elif line.startswith("/debug"):
            if matcher.personality is None:
                print("You're not matched with anyone yet so nothing to debug. Use /match")
            else:
                bot_line = matcher.debug_personality_response(matcher.personality, line)
                print("\n%s" % (bot_line))
        else:
            conseq_failed_match_attempts = 0
            if matcher.personality is None:
                print("You're not matched with anyone so nobody read that. Use /match")
            else:
                try:
                    bot_line = matcher.personality_response(line)
                    print("\n%s" % (bot_line))
                except UnmatchedException:
                    print(f"You've been unmatched by {matcher.personality.name}. I guess you weren't very smooth")
                    matcher.personality = None

if __name__ == "__main__":
    main()