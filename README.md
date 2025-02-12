1. Project Introduction

Title:
Scrabble Word Game

Objective:
Connect randomly placed letters on the grid by forming valid English words while dodging the blocked squares

Rules:
a) Randomly selected letters and blocked squares will show up on the board
b) The number of letters and blocked squares will be different based on the difficulty (Easy, Medium, Hard)
c) Type in a word that start with one of the letters on the board
d) Set the direction of the word displayed on the board (vertical or horizontal)
e) You can now use the letters of the word inputted as the starting point as well
f) The objective of the game is to connect all of the first batch of letters using the words the player typed in

Restrictions:
a) You cannot form a new word by merging 2 words")
Eg. Merge 'LOLIPOP' and 'POP' to form a long horizonal 'LOLIPOPOP'

2. The code
Libraries:
- random
- string

Functions:
strip_ansi_codes(s)
Strip ANSI color codes for comparison

get_color_code(index)
Get the ANSI escape codes for different colors (print randomly generated letters using different colors)

generate_random_letters(num_letter):
Generate the random letters initially on the board

generate_random_coordinates(num_coords, size_limit):
Generate the random coordinates on the board

check_coordinate_in_list(x, y, coordinates):
Check whether the current coordinate is in the list of randomly generated coordinates

print_grid(size, grid):
Print the grid with the blocked coordinates, the randomized letters and everything

can_place_word(grid, word, start_x, start_y, direction):
Check whether the user's inputted word is eligible for placement on the grid

update_grid_with_word(grid, word, start_x, start_y, direction):
Update the grid with the user's inputted word

update_letters_and_coord(word, start_x, start_y, direction, letter_coordinates, letters):
Update the list of letters and coordinates to choose from with the user's inputted word

check_hori_blocked(start_of_x, start_of_y, len_word, block_coordinates, size_grid):
Check whether the word is blocked in hori direction

check_vert_blocked(start_of_x, start_of_y, len_word, block_coordinates, size_grid):
Check whether the word is blocked in vert direction 

direction_of_word(grid, word, size_grid, start_of_x, start_of_y, len_word, block_coordinates, letter_coordinates, lett):
Let the user choose the direction of the word to be displayed on the board

is_connected(letter_coordinates, grid):
Check if the initially generated letters are connected via words

user_input_word(letters, letter_coordinates):
Let the user input the words

get_letter_coord_based_on_user(char, letters, letter_coordinates):
Get the coordinates of places where the user's word's first character lies on the board

main():
Main game logic

3. Installing and Running the Project
a) Click on the scrabble_word_game.zip and download the files:
- scrabble_main.py
- word_checker.py
- win_animation.py
- words.txt

b) If you want to quit the game midway, type "Ctrl + C".



Functions:
strip_ansi_codes(s) - GPT-4o
get_color_code(index) - Microsoft Copilot
is_connected(letter_coordinates, grid) - GPT-4o

Others:
Statistics of how many English words starts with each letter:
https://www.unscramblerer.com/scrabble-twl-dictionary-statistics/

