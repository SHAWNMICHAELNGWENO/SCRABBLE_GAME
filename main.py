import random
import string
import word_checker


# default color code of stuff printed in console
RESET = "\033[0m"


# weight of randomly generated letters based on how many english word starts with each alphabet
# https://www.unscramblerer.com/scrabble-twl-dictionary-statistics/
weight_of_letters = {
    'A': 5.93, 'B': 5.66, 'C': 9.23, 'D': 5.84, 'E': 3.96, 'F': 3.96, 'G': 3.3,
    'H': 3.62, 'I': 3.64, 'J': 0.84, 'K': 1.08, 'L': 2.99, 'M': 5.63, 'N': 2.56,
    'O': 3.33, 'P': 8.43, 'Q': 0.47, 'R': 5.83, 'S': 11.12, 'T': 5.08, 'U': 2.92,
    'V': 1.61, 'W': 2.21, 'X': 0.08, 'Y': 0.34, 'Z': 0.34
}

# credit to GPT-4o
# strip ANSI color codes for comparison
def strip_ansi_codes(s):
    return s.replace("\033[91m", "").replace("\033[92m", "").replace("\033[93m", "").replace("\033[94m", "").replace("\033[95m", "").replace("\033[96m", "").replace(RESET, "")


# get the ANSI escape codes for different colors (print randomly generated letters using different colors)
def get_color_code(index):
    colors = [
       "\033[91m", # Red 
       "\033[92m", # Green 
       "\033[93m", # Yellow 
       "\033[94m", # Blue 
       "\033[95m", # Magenta 
       "\033[96m", # Cyan 
    ]
    return colors[index % len(colors)]


# generate the random letters initially on the board
def generate_random_letters(num_letter):
    alphabet = list(weight_of_letters.keys())
    weight = list(weight_of_letters.values())
    return [random.choices(alphabet, weight)[0] for _ in range(num_letter)]


# generate the random coordinates on the board
def generate_random_coordinates(num_coords, size_limit):
    return [(random.randint(0, size_limit - 1), random.randint(0, size_limit - 1)) for _ in range(num_coords)]


# check whether the current coordinate is in the list of randomly generated coordinates
def check_coordinate_in_list(x, y, coordinates):
    return (x, y) in coordinates


# print the grid with the blocked coordinates, the randomized letters and everything
def print_grid(size, grid):
    for i in range(size):
        print("+---" * size + "+")
        for j in range(size):
            char = grid[i][j]
            if char == ' ▩ ':
                print(f"|{char}", end="")
            elif char != ' ':
                print(f"| {char} ", end="")
            else:
                print("|   ", end="")
        print("|")
    print("+---" * size + "+")


# check whether the user's inputted word is eligible for placement on the grid
def can_place_word(grid, word, start_x, start_y, direction):
    combined_word = ""
    for index, char in enumerate(word):
        if direction == "H":
            x, y = start_x + index, start_y
        elif direction == "V":
            x, y = start_x, start_y + index
        
        # Check grid boundaries
        if x >= len(grid[0]) or y >= len(grid):
            print(f"Out of bounds: ({x}, {y})")
            return False

        grid_char = strip_ansi_codes(grid[y][x])
        if grid_char != " " and grid_char != char.upper():
            print(f"Conflict at ({y}, {x}): grid has '{grid[y][x]}', word has '{char.upper()}'")
            return False

        combined_word += grid_char if grid_char != " " else char.upper()

    # Check if the combined word is valid
    if not word_checker.is_valid_word(combined_word):
        print(f"The word '{combined_word}' is not a valid English word.")
        return False
    
    # Additional boundary checks
    if direction == "H":
        if start_x > 0 and grid[start_y][start_x - 1] != " " and strip_ansi_codes(grid[start_y][start_x - 1]) != grid[start_y][start_x]:
            print("Invalid extension at the start of the word.")
            return False
        if start_x + len(word) < len(grid[0]) and grid[start_y][start_x + len(word)] != " ":
            print("Invalid extension at the end of the word.")
            return False

    elif direction == "V":
        if start_y > 0 and grid[start_y - 1][start_x] != " " and strip_ansi_codes(grid[start_y - 1][start_x]) != grid[start_y][start_x]:
            print("Invalid extension at the start of the word.")
            return False
        if start_y + len(word) < len(grid) and grid[start_y + len(word)][start_x] != " ":
            print("Invalid extension at the end of the word.")
            return False

    return True
    

# update the grid with the user's inputted word
def update_grid_with_word(grid, word, start_x, start_y, direction):
    for index, char in enumerate(word):
        word_char = char.upper()
        if direction == "H":
            x, y = start_x + index, start_y
        elif direction == "V":
            x, y = start_x, start_y + index
        
        grid_char = grid[y][x]
        # Retain the color if it's the same letter
        if strip_ansi_codes(grid_char) == word_char:
            continue
        # Otherwise, update with the new letter
        grid[y][x] = word_char


# update the list of letters and coordinates to choose from with the user's inputted word
def update_letters_and_coord(word, start_x, start_y, direction, letter_coordinates, letters):
    for index, char in enumerate(word):
        if direction == "H":
            x, y = start_x + index, start_y
        elif direction == "V":
            x, y = start_x, start_y + index
        
        if (x, y) not in letter_coordinates:
            letter_coordinates.append((x, y))
            letters.append(char.upper())


# check whether the word is blocked in hori direction
def check_hori_blocked(start_of_x, start_of_y, len_word, block_coordinates, size_grid):
    for i in range(len_word):
        # check if x-coord + 0, x-coord + 1, x-coord + 2... up to length of word and y-coord in block_coordinates
        if (start_of_x + i, start_of_y) in block_coordinates:
            return True

    # check if the word too long for the board horizontally
    if start_of_x + len_word > size_grid:
        return True
    return False


# check whether the word is blocked in vert direction 
def check_vert_blocked(start_of_x, start_of_y, len_word, block_coordinates, size_grid):
    for i in range(len_word):
        if (start_of_x, start_of_y + i) in block_coordinates:
            return True

    # check if the word too long for the board vertically
    if start_of_y + len_word > size_grid:
        return True
    return False


# let the user choose the direction of the word to be displayed on the board
def direction_of_word(grid, word, size_grid, start_of_x, start_of_y, len_word, block_coordinates, letter_coordinates, lett):
    direction = input("Enter the direction ('V' for vertical, 'H' for horizontal) you want the word to be on the board: ").upper()
    if direction == "H":
        if check_hori_blocked(start_of_x, start_of_y, len_word, block_coordinates, size_grid):
            print("Horizontal path is blocked.")
            return False
    elif direction == "V":
        if check_vert_blocked(start_of_x, start_of_y, len_word, block_coordinates, size_grid):
            print("Vertical path is blocked.")
            return False
    else:
        print("Invalid input. Enter 'V' for vertical, or 'H' for horizontal.")
        return False
    
    if can_place_word(grid, word, start_of_x, start_of_y, direction):
        update_grid_with_word(grid, word, start_of_x, start_of_y, direction)
        update_letters_and_coord(word, start_of_x, start_of_y, direction, letter_coordinates, lett)
        print_grid(size_grid, grid)
        print("Successfully placed the word on the board!")
        return True
    else:
        print("The word cannot be placed due to conflict with existing letters.")
        return False


# credit to GPT-4o
# check if the initially generated letters are connected via words
def is_connected(letter_coordinates, grid):
    visited = set()
    
    def dfs(x, y):
        if (x, y) in visited or grid[y][x] == ' ':
            return
        visited.add((x, y))
        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx, ny) in letter_coordinates:
                dfs(nx, ny)

    # Start DFS from the first letter
    start_x, start_y = letter_coordinates[0]
    dfs(start_x, start_y)

    # Check if all letter coordinates are visited
    return all((x, y) in visited for x, y in letter_coordinates)

# let the user input the words
def user_input_word(letters, letter_coordinates):
    word = input("Enter a word: ")
    confirm = False

    # check if the word is valid and update if necessary
    word = word_checker.get_valid_word(word, letters)

    coord_of_first_letter = get_letter_coord_based_on_user(word[0], letters, letter_coordinates)

    while not coord_of_first_letter:
        word = input("No valid coordinates found for the first letter. Please enter another word: ")
        word = word_checker.get_valid_word(word, letters)
        coord_of_first_letter = get_letter_coord_based_on_user(word[0], letters, letter_coordinates)

    print("Choose the coordinate where you want to put the word on the board.")
    print("Choose by inputting the index of the coordinate from the list of coordinates to choose from. (0, 1, 2... and so on)")

    while not confirm:
        print("Coordinates to choose from:", coord_of_first_letter)
        choose_coord = input("Coordinate you choose: ")

        while not choose_coord.isnumeric():
            choose_coord = input("Make sure to input a number (ie. index of the coordinate): ")

        while int(choose_coord) > len(coord_of_first_letter) - 1:
            choose_coord = input("Make sure to input an index within the range: ")

        choose_coord = int(choose_coord)
        print("Coordinate chosen:", coord_of_first_letter[choose_coord]) 

        yes_no = input("Confirm the coordinate chosen by typing 'y' or 'n': ")
        if yes_no.isalpha() and yes_no.lower() == 'y':
            confirm = True

    print("Coordinate chosen:", coord_of_first_letter[choose_coord])
    return coord_of_first_letter[choose_coord][0], coord_of_first_letter[choose_coord][1], len(word), word

# get the coordinates of places where the user's word's first character lies on the board
def get_letter_coord_based_on_user(char, letters, letter_coordinates):
    lett_coord_of_user = [letter_coordinates[index] for index, lett in enumerate(letters) if lett == char.upper()]
    return lett_coord_of_user

# main
def main():

    # title card
    scrabble_ascii = r'''
        _____  _____ _____            ____  ____  _      ______ 
       / ____|/ ____|  __ \     /\   |  _ \|  _ \| |    |  ____|
      | (___ | |    | |__) |   /  \  | |_) | |_) | |    | |__   
       \___ \| |    |  _  /   / /\ \ |  _ <|  _ <| |    |  __|  
       ____) | |____| | \ \  / ____ \| |_) | |_) | |____| |____ 
      |_____/ \_____|_|  \_\/_/    \_\____/|____/|______|______|
    '''
    print(scrabble_ascii)

    head1 = input("Enter 'start' to play: ")

    while head1 != "start":
        head1 = input("Enter 'start' to play: ")
    
    # print rules of the game
    print("*****RULES*****")
    print("1. Randomly selected letters and blocked squares will show up on the board")
    print("2. The number of letters and blocked squares will be different based on the difficulty (Easy, Medium, Hard)")
    print("3. Type in a word that start with one of the letters on the board")
    print("4. Set the direction of the word displayed on the board (vertical or horizontal)")
    print("5. You can now use the letters of the word inputted as the starting point")
    print("6. The objective of the game is to connect all of the first batch of letters using the words the player typed in")
    print("***************")
    print()
    print("**RESTRICTION**")
    print("1. You cannot form a new word by merging 2 words")
    print("Eg. Merge 'LOLIPOP' and 'POP' to form a long horizonal 'LOLIPOPOP'.")
    print("***************")

    # set size of grid
    size_grid = input("Size of grid (from 10x10 to 15x15): ")
    while not (size_grid.isdigit() and 10 <= int(size_grid) <= 15):
        size_grid = input("Size of grid (from 10x10 to 15x15): ")
    
    # make sure the inputted size grid is converted to int
    size_grid = int(size_grid)

    # set number of blocked squares and letters
    difficulty = input("Select level of difficulty ('E'/'M'/'H'): ").upper()
    num_square = 5
    num_letter = 5

    # Easy: 5 letters, 5 blocks
    # Medium: 5 letters, 10 blocks
    # Hard: 7 letters, 15 blocks

    while difficulty not in ("E", "M", "H"):
        difficulty = input("Select level of difficulty ('E'/'M'/'H'): ").upper()

    if difficulty == "E":
        num_square = 5
        num_letter = 5
    elif difficulty == "M":
        num_square = 10
        num_letter = 5
    elif difficulty == "H":
        num_square = 15
        num_letter = 7

    grid = [[' ' for _ in range(size_grid)] for _ in range(size_grid)]
    block_coordinates = generate_random_coordinates(num_square, size_grid)
    letter_coordinates = generate_random_coordinates(num_letter, size_grid)
    letters = generate_random_letters(num_letter)

    while any(coord in block_coordinates for coord in letter_coordinates):
        letter_coordinates = generate_random_coordinates(num_letter, size_grid) 

    for index, (x, y) in enumerate(letter_coordinates):
        # set color, print lett, turn the color back to default
        grid[y][x] = get_color_code(index) + letters[index] + RESET

    for (x, y) in block_coordinates:
        grid[y][x] = ' ▩ '

    # print actual grid
    print_grid(size_grid, grid)

    # let user input word
    while not is_connected(letter_coordinates, grid):
        start_of_x, start_of_y, len_word, word = user_input_word(letters, letter_coordinates)

        # check if the selected direction is blocked according to the word inputted and the coordinate chosen
        # while direction_of_word == False
        while not direction_of_word(grid, word, size_grid, start_of_x, start_of_y, len_word, block_coordinates, letter_coordinates, letters):
            print("Please enter a new word or input the word again and change the direction.")
            start_of_x, start_of_y, len_word, word = user_input_word(letters, letter_coordinates)

    if is_connected(letter_coordinates, grid):
        import win_animation
        win_animation.play_animation(duration=10)
        replay = input("Enter 'R' to replay, 'Q' to quit: ").upper()
        while (replay != "R" and replay != "Q") or not replay.isalpha:
            replay = input("Enter 'R' to replay, 'Q' to quit: ").upper()
    
        if replay == "R":
            print("Restarting the game...")
            main()
        elif replay == "Q":
            print("Thank you for playing!")
            exit()

if __name__ == "__main__":
    main()
