# ajfuto
# Recursive WordHunt Solver

import time
import sys

BOARD_SIZE = 4
MIN_LENGTH = 3
MAX_LENGTH = BOARD_SIZE**2

moves = [ [-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1] ]

# Trie implementation to store dictionary of words
class TrieNode():
    def __init__(self):
        self.children = {}
        self.is_word = False

# loads dictionary from text file, represents it as Trie
def load_dictionary():
    t1 = time.time()
    dictionary = TrieNode()

    # iterate through every word in our list
    with open('./words.txt', 'r') as ifp:
        for line in ifp:
            curr_node = dictionary
            word = line.strip().lower()

            if not word.isalpha():
                continue

            if len(word) < MIN_LENGTH:
                continue

            if len(word) > MAX_LENGTH:
                continue

            # break our word into letters
            for i in range(len(word)):
                curr_char = word[i]

                # if this character isn't already logged, log it
                if curr_char not in curr_node.children:
                    curr_node.children[curr_char] = TrieNode()

                # if this makes the word complete, mark it as such    
                curr_node = curr_node.children[curr_char]
                if i == len(word) - 1:
                    curr_node.is_word = True

    t2 = time.time()
    print(f'dictionary loaded in {(t2-t1):.3f}s')
    return dictionary

# gets the letters of the board from the user
def get_letters():
    ret_lets = []

    letters_str = sys.argv[1][0:MAX_LENGTH] if len(sys.argv) > 1 and len(sys.argv[1]) >= MAX_LENGTH else input('please enter the available letters: ')
    letters_str.replace(' ', '').lower().strip()
    
    if len(letters_str) != MAX_LENGTH:
        print('invalid number of letters')
        exit(1)

    for i in range(BOARD_SIZE):
        ret_lets.append([])
        for j in range(BOARD_SIZE):
            ret_lets[i].append(letters_str[BOARD_SIZE*i+j])

    return ret_lets

# finds the solutions
# wrapper for recursive function
def solve(dictionary, board):

    visited = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    found_words = []

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            recurse_solve(i, j, '', visited, dictionary, board, found_words)

    return list(set(found_words))

def is_safe(x, y, max_x, max_y):
    return x >= 0 and x < max_x and y >= 0 and y < max_y

# recursive function that finds solutions given a board state
def recurse_solve(row, col, word, visited, curr, board, found):

    # base cases, out of bounds or visited
    if not is_safe(row, col, BOARD_SIZE, BOARD_SIZE):
        return
    if visited[row][col]:
        return

    curr_let = board[row][col]

    if curr_let not in curr.children:
        return

    visited[row][col] = True
    word += curr_let

    if len(word) > MIN_LENGTH and curr.children[curr_let].is_word:
        found.append(word)

    for move in moves:
        x = move[0]
        y = move[1]
        if is_safe(row+x, col+y, BOARD_SIZE, BOARD_SIZE):
            if not visited[row+x][col+y]:
                recurse_solve(row+x, col+y, word, visited, curr.children[curr_let], board, found)

    visited[row][col] = False

# sorts the solutions by descending lengths
def sort_sols(sols):
    return sorted(sols, key=len)[::-1]

def main(): 
    words = load_dictionary()
    letters = get_letters()
    found_sols = solve(words, letters)
    print(sort_sols(found_sols))

if __name__ == '__main__':
    main()

