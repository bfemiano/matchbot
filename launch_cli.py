import readline

from random import randint
from responder import GenericResponder
from time import sleep
from nltk.corpus import names 

male_names = names.words('male.txt')
female_names = names.words('female.txt')

def get_help():
    mat = "/match [woman|man|nonbinary] to match with a new partner.\n"
    hlp = "/help to see more info\n"
    ext = "/exit to ghost."
    return "%s%s%s" % (mat, hlp, ext)

def print_welcome():
    print("Welcome to Matchbot!\n%s" % get_help())

def reset_match(gender): # TODO abstract this away. 
    if gender == "r":
        gender = ["w", "m", "n"][randint(0, 2)]
    if gender == "w":
        return female_names[randint(0, len(female_names))]
    elif gender == "m":
        return male_names[randint(0, len(male_names))]
    else:
        return "pat" # TODO get a good list of nonbinary names.

def slight_delay(name): # TODO abstract this away
    delay = randint(1, 2)
    print("\t\t<%s has received your message>" % name)
    sleep(delay)
    delay = randint(5, 10)
    print("\t\t<%s is thinking of what to say>" % name)
    sleep(delay)
    delay = randint(3, 5)
    print("\t\t<%s is responding>" % name)
    sleep(delay)

def main():
    done = False
    conseq_failed_match_attempts = 0
    print_welcome()
    responder = GenericResponder(wrap_count=80)
    name = None
    while(not done):
        line = input("> ")
        if line == "/exit":
            done = True
        elif line == "/help":
            print("\n%s\n" % get_help())
        elif line.startswith("/match"): # TODO abstract this away
            parts = line.split(" ")
            if len(parts) <= 1:
                print("Must be either 'woman', 'man', or 'nonbinary'")
            else:
                gender = parts[1]
                if gender == "woman":
                    name = reset_match("w")
                    print("\nNow talking with %s!\n" % name)
                elif gender == "man":
                    name = reset_match("m")
                    print("\nNow talking with %s!\n" % name)
                elif gender == "nonbinary":
                    name = reset_match("n")
                    print("\nNow talking with %s!\n" % name)
                else:
                    conseq_failed_match_attempts += 1
                    if conseq_failed_match_attempts == 6:
                        conseq_failed_match_attempts = 0
                        print("You seem to be having trouble. I'll select a partner for you at random.")
                        name = reset_match("r")
                        print("\nNow talking with %s!\n" % name)
                    else:
                        print("Must be either 'woman', 'man', or 'nonbinary'")
                    
        else:
            conseq_failed_match_attempts = 0
            if name is None:
                print("You're not matched with anyone so nobody read that. Use /match")
            else:
                bot_line = responder.respond(line)
                slight_delay(name)
                print("\n%s" % (bot_line))

if __name__ == "__main__":
    main()