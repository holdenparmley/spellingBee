#!/usr/bin/env python
'''
A robot to solve the NYT's 'Spelling Bee' game.
Call the program, then provide the 7 letters to be used, then a list of words (as a txt file)
'''

import sys

if len(sys.argv) == 3:  # Arguments should include a 7-letter string and a dictionary file
    if len(hive := sys.argv[1].upper()) != 7:  # If the string is not exactly 7 letters long...
        sys.exit('Your hive is not big enough!')  # Print this, and exit
    dictionary = sys.argv[2]  # Save the dictionary file as dictionary
else:  # If there are not enough arguments, print the following line and exit
    sys.exit(f'Usage: {sys.argv[0]}, 7-letter hive, list of valid words')

solutions = set()  # Create an empty set, to be filled with valid solutions
dictionary_words = set()  # Create an empty set to be filled with words from a given language

with open(dictionary) as dict_file:
    for line in dict_file:
        if line[0].islower():  # If the line is not a proper noun...
            dictionary_words.add(line.rstrip().upper())  # Add it to a set of dictionary words

for word in dictionary_words:  # Go through the set of words
    # For each word, if the word has more than 4 letters, and contains the hive's center letter...
    if len(word) >= 4 and hive[3] in word.upper():
        solutions.add(word)  # Add the word to the set of solutions (it is only a candidate here)
        for letter in word:  # For each letter in the word...
            if letter not in hive:  # If the letter is not part of the hive...
                solutions.remove(word.upper())  # Remove the word from the set of solutions
                break  # Break out after the first occurrence, to avoid trying to remove twice

word_sylls = {}  # Create an empty dictionary, to fill with words and their syllable counts

with open('/srv/datasets/syllables.txt') as syllable_file:
    for line in syllable_file:  # For each line in this file...
        orig_word = line.strip().replace(';', '')  # Save a non-syllable-split version
        # This section was added to deal with the case where a word has conflicting syllable counts
        # If the non-syllable-split word is already in the set of keys...
        # And the existing syllable count is greater than the new potential syllable count...
        if orig_word in word_sylls and word_sylls[orig_word] > len(line.split(';')):
            continue  # Keep the larger syllable count, and continue to the next line in the file
        # This next line will run if the last 'if' statement was not met (this is most likely)
        word_sylls[orig_word] = len(line.split(';'))  # Add a word/syllable pair to word_sylls

solutions_pts = {}  # Create an empty dictionary, to fill with solutions and their point counts

for solution in solutions:  # For each solution to the spelling bee...
    if len(solution) == 4:  # If the solution is exactly 4 letters...
        solutions_pts[solution] = 1  # Award 1 point
    elif len(solution) > 4:  # If the solution has more than 4 letters...
        solutions_pts[solution] = len(solution)  # Award 1 point for every letter
    if len(solution) >= 7:  # If the solution has 7 or more letters, a pangram is possible
        if any(letter not in solution for letter in hive):
            pass  # If any hive letters are not included, move on without awarding extra points
        else:  # Otherwise...
            solutions_pts[solution] = len(solution) + 7  # Award 7 extra points
    if solution.lower() in word_sylls:  # If the solution is in the syllable count file...
        solutions_pts[solution] += word_sylls[solution.lower()]  # Award 1 extra point per syllable

final_answers = []  # Create an empty list, to help get our solutions in order

for pair in solutions_pts.items():  # For every solution and points pair...
    final_answers.append((pair[1], pair[0]))  # Add the pair, with points first

final_sort = sorted(final_answers)  # Sort solutions by points, and alphabetically within points

for pair in final_sort:  # For every solution/point pair in our final sorted list...
    print(f'{pair[1]} {pair[0]}')  # Print the solution, then the point value
