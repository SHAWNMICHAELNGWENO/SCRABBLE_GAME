# Load a list of words into a set
# The list of words are taken from this website: https://github.com
with open('words.txt') as f:
    valid_words = set(word.strip().lower() for word in f)

# Check if the word is valid
def is_valid_word(word):
    return word.lower() in valid_words

# Return True if the word is valid and if the word starts with the letters on the board
def get_valid_word(word, letters):
    word = word.lower()
    
    # while not valid word or the word user inputted doesn't start with any of the letters on the board
    # -any() returns True when the condition inside is fulfilled- 
    while not is_valid_word(word) or word[0].upper() not in letters:
        if not is_valid_word(word):
            # Case 1: when the word user inputted is not valid (ie. not an English word)
            word = input("Please input a valid word: ") 
        else:
            # Case 2: when the word user inputted doesn't start with any of the letters on the board
            word = input("Please input a word that starts with one of the letters on the board: ")
    return word
    
if __name__ == "__main__":
    word = input("Enter a word: ")

    import main
    get_valid_word(word, letters)
