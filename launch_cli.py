import readline

from matcher.matcher import Matcher, NoPersonalityFileException
from gender.gender import UnsupporteGenderCommandException

def get_help():
    mat = "/match [woman|man|nonbinary] to match with a new partner.\n"
    hlp = "/help to see more info\n"
    sav = "/save to save your current chat partner session to ./personality.dat\n"
    lod = "/load to reload the save session\n"
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
            print("persisting current chat partner: %s" % matcher.personality)
            matcher.save_personality()
            print("persistence successful.")
        elif line == "/load":
            try:
                matcher.load_personality()
                print("Hi there! This is %s. It's great to see you again!" % matcher.personality)
            except NoPersonalityFileException:
                print("Missing personality.dat file in basedir")
        elif line.startswith("/match"): # TODO abstract this away
            try:
                matcher.new_personality(matcher.match(line))
                print("\nNow talking with %s!\n" % matcher.personality) 
                conseq_failed_match_attempts = 0
            except UnsupporteGenderCommandException as e:
                print(e.msg)
                conseq_failed_match_attempts += 1
                if conseq_failed_match_attempts == 6:
                    conseq_failed_match_attempts = 1
                    print("You seem to be having trouble. I'll select a partner for you at random.")
                    matcher.new_personality(matcher.match_random())
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