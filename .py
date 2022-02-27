import time, pathlib, random, glob

def check_win(secret_word):
    """Tells if player guessed the secret word.
    :param secret_word: the secret word of the game
    :param old_letters_guessed: list of letters that the player already guessed
    :type secret_word: str
    :type old_letters_guessed: list
    :return: True if all letters of the secret word are in the list of letters that the player already guessed, False otherwise.
    :rtype: boolean
    """
    global old_letters_guessed
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


def show_hidden_word(secret_word):
    """Shows player guess condition graphically to user.
    :param secret_word: the secret word of the game
    :param old_letters_guessed: list of letters that the player already guessed
    :type secret_word: str
    :type old_letters_guessed: list
    :return: String that made of bottom lines (letters that player has not yet guessed) and letters that player guessed right.
    :rtype: str
    """
    global old_letters_guessed
    result = ''
    for letter in secret_word:
        if letter not in old_letters_guessed:
            result = result + '_ '
        else:
            result = result + letter + ' '
    return result


def check_valid_input(letter_guessed):
    """Tells if user's input is valid or not.
    :param letter_guessed: user's guess (input)
    :param old_letters_guessed: user's old guesses (valid letters) list
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: True if user's input valid (1 length and in english alphabet) and never used before, False otherwise.
    :rtype: boolean
    """
    global old_letters_guessed
    if (len(letter_guessed) == 1) and (letter_guessed.isalpha()) and (letter_guessed not in old_letters_guessed):
        return True
    else:
        return False


def try_update_letter_guessed(letter_guessed):
    """Adds user's input to guesses list if valid or prints message if not.
    :param letter_guessed: user's input
    :param old_letters_guessed: user's old guesses (valid letters) list
    :type letter_guessed: str
    :type old_letters_guessed: list
    :return: True if user's input added to guesses list and False if not.
    :rtype: boolean
    """
    global old_letters_guessed
    if check_valid_input(letter_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    else:
        print('X')
        if old_letters_guessed:
            print(' -> '.join(sorted(old_letters_guessed)))
        return False


def choose_word(file_path, index):
    """Gets path of a text file with words separated with spaces in it and an index.
    :param file_path: path of a text file with words in it
    :param index: index represents location of a word from the file
    :type file_path: str
    :type index: int
    :return: The word at the specific index
    :rtype: str
    """
    with open(file_path, 'r') as f:
        words_list = f.read().split(' ')  # turning the text in the file into a list of words
        fixed_index = index
        if index > len(words_list):
            fixed_index = index % len(words_list)  # in case that "index" is larger than number of the words on the file
        return words_list[fixed_index - 1].lower()


def opening_print():
    '''Prints opening when game starts using ASCII art.'''
    HANGMAN_ASCII_ART = """ _    _                                         \n\
| |  | |                                        \n\
| |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  \n\
|  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \  \n\
| |  | | (_| | | | | (_| | | | | | | (_| | | | |\n\
|_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|\n\
                     __/ |                      \n\
                    |___/\n"""
    MAX_TRIES = 6
    print('%s\nYou have %d attempts to guess the word, good luck!\n' % (HANGMAN_ASCII_ART, MAX_TRIES))


def print_hangman(num_of_tries):
    '''Prints game condition of player using ASCII art.'''
    HANGMAN_PHOTOS = {
    0:"""x-------x""",
    1:"""x-------x\n|\n|\n|\n|\n|""",
    2:"""x-------x\n|       |\n|       0\n|\n|\n|""",
    3:"""x-------x\n|       |\n|       0\n|       |\n|\n|""",
    4:"""x-------x\n|       |\n|       0\n|      /|\ \n|\n|""",
    5:"""x-------x\n|       |\n|       0\n|      /|\ \n|      /  \n|""",
    6:"""x-------x\n|       |\n|       0\n|      /|\ \n|      / \ \n|"""}
    if num_of_tries == 0:
        print('\n%s' % HANGMAN_PHOTOS[num_of_tries])
    elif num_of_tries == 1:
        print('%s\n' % HANGMAN_PHOTOS[num_of_tries])
    else:
        print('\n%s\n' % HANGMAN_PHOTOS[num_of_tries])


def create_secret_word():
    '''Receives arguments from user in order to choose a secret word.
    :return: secret word (returned from "choose_word" function.
    :rtype: str
    '''
    groups = []  # list of all names of text files that are in the same directory as the PY file.
    pathes = glob.glob(str(pathlib.Path(__file__).parent.absolute()) + "/*.txt")
    for path in pathes:
        groups.append(path.split('\\')[-1].split('.')[0])
    if not groups:  # in case that there are not text files in directory (there are no words to choose from)
        return 'None'
    group = input(f"Enter group of words ({'/'.join(groups)}): ")
    path = str(pathlib.Path(__file__).parent.absolute()) + '\\' + group + '.txt'
    location_of_word = random.randint(1,100)
    return choose_word(path, location_of_word)


def main():
    opening_print()
    secret_word = create_secret_word()
    if secret_word == 'None':
        print('There are no text files in the directory to choose words from!\n')
        print('Closing in ', end='', flush=True)
        for i in range(6, 0, -1):
            print(str(i) + ', ', end='', flush=True)
            time.sleep(1)
        quit()
    global old_letters_guessed
    old_letters_guessed = []
    MAX_TRIES = 6
    num_of_tries = 0
    print('\nLet’s start!')
    print_hangman(num_of_tries)
    print('%s\n' % show_hidden_word(secret_word))
    while(True):
        if num_of_tries == MAX_TRIES:
            print('\nYOU LOST...\n')
            print('Closing in ', end='', flush=True)
            for i in range(6, 0, -1):
                print(str(i) + ', ', end='', flush=True)
                time.sleep(1)
            break
        letter_guessed = input("Guess a letter: ").lower()
        while (not try_update_letter_guessed(letter_guessed)):
            letter_guessed = input("Guess a letter: ").lower()
        if check_win(secret_word):
            print(show_hidden_word(secret_word))
            print('\nYOU WON!\n')
            print('Closing in ', end='', flush=True)
            for i in range(6, 0, -1):
                print(str(i) + ', ', end='', flush=True)
                time.sleep(1)
            break
        if (letter_guessed not in secret_word):
            print(':(')
            num_of_tries += 1
            print_hangman(num_of_tries)
        print(show_hidden_word(secret_word))


if __name__ == "__main__":
    main()
