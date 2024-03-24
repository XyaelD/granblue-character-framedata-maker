from logger import get_logger
from granblue_data_gatherer import GranblueDataGatherer

# get the logger
logger = get_logger()

valid_characters = ['zeta', 'vaseraga', 'eustace', 'anre', 'seox', 'lancelot', 'percival', 'siegfried',
                    'zooey', 'ladiva', 'narmaya', 'gran', 'djeeta', 'charlotta', 'ferry', 'anila',
                    'grimnir', 'metera', 'lowain', 'katalina', 'vira', 'yuel', 'soriz', 'cagliostro',
                    'nier', 'belial', 'beelzebub', 'lucilius', 'avatar_belial', '2b']

sections = [2,3,4,5,6,7,8]
#2 Section ID for normals
#3 Section ID for unique moves
#4 Section ID for universals
#5 Section ID for specials
#6 Section ID for ultimates
#7 Section ID for skybounds artes
#8 Section ID for super skybound artes

def choose_character():
    valid = False
    while not valid:
        choice = input("Which character do you want to create a .csv for?").lower().replace(" ", "_")
        if choice in valid_characters:
            logger.info(f"Creating a csv file for {choice}")
            valid = True
            return choice
        else:
            logger.warning("That is not a character in the game. Please enter another.")
            logger.info("The valid characters are: " + ', '.join(valid_characters))

if __name__ == "__main__":
    user_choice = choose_character()
    gbg = GranblueDataGatherer(user_choice)
    gbg.go_to_character_page()
    for section in sections:
        gbg.handle_section(section)
    gbg.create_csv()
    