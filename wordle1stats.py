"""
Computer plays wordle (random guessing).

:author:  Terry Sergeant
:version: 1

In this version the computer randomly selects a word, then reduces the
list of possible solutions and randomly guesses from the remaining words.
"""

import random
import re
from colorama import Fore, Back, Style

def is_possible(word, result):
    """
    Determine whether a word is possible based on guesses made so far
    and the partial word provided by the user.

    :param word: The word we are considering as a possible match.
    :param result: A dictionary that stores the guess and the grade.
    :returns: True if the word is a possible match; False otherwise.
    """
    guesslist = list(result['guess'])
    gradelist = list(result['grade'])
    wordlist = list(word)

    # if perfect match letters don't line up then its not a match
    for i in range(len(word)):
        if gradelist[i] == '2':
            if guesslist[i] != word[i]:
                return False
            else:
                # remove letters that are a perfect match
                wordlist[i] = '!'
                guesslist[i] = '@'

    for i in range(len(word)):
        if gradelist[i] == '1':
            # right letter, wrong position -> if its there mark it out, if not
            # return False. If it is in the same spot return False.
            if guesslist[i] == wordlist[i]:
                return False
            if not (guesslist[i] in wordlist):
                return False

            for j in range(len(word)):
                if guesslist[i] == wordlist[j]:
                    guesslist[i] = '@'
                    wordlist[j] = '!'
                    break
        elif gradelist[i] != '*':
            # we guessed wrong letter completely so it shouldn't be left in the word
            if guesslist[i] in wordlist:
                return False

    return word != guess  # true unless the word matches our guessed word



def reduce_word_list(wordlist, result):
    """
    Narrow down list of possible choices.

    :param wordlist: List of words that are still considered possibilities.
    :param result: A dictionary that stores the guess and the grade.
    :returns: Modified and shortened word_list.
    """
    return [w for w in wordlist if is_possible(w, result)]



def load_dictionary(filename):
    """
    Read the dictionary from the file and return the words as a list.

    :param filename: The file containing the official dictionary.
    :returns: wordlist
    """
    wordlist = []
    with open(filename) as f:
        for word in f:
            wordlist.append(word.rstrip())

    return wordlist



def get_next_guess(wordlist):
    """
    Randomly select a word from the list of words.

    :param wordlist: The list of words currently being considered.
    :returns: A randomly selected word from the list.
    """
    return wordlist[random.randint(0,len(wordlist)-1)]


def grade_word(answer, guess):
    """
    Grades the guess by comparing it to the correct answer.

    :param answer: The answer word the computer is trying to guess.
    :param guess: The guessed word to be graded.
    :returns: Returns a dictionary containing the original guess and the grade
        string.

    NOTE: The grade string contains 5 characters as follows:
     * there is a 2 if the correct letter is used in the correct place
     * there is a 1 if the correct letter is used in the wrong place
     * the original guessed letter is used if the letter does not occur in the answer
    """
    answerlist= list(answer)
    guesslist= list(guess)

    for i in range(len(answer)):
        if answerlist[i] == guesslist[i]:
            guesslist[i] = '2'
            answerlist[i] = 0

    for i in range(len(answer)):
        for j in range(len(answer)):
            if answerlist[i] == guesslist[j]:
                guesslist[j] = '1'
                answerlist[i] = 0

    return {
        "guess": guess,
        "grade": "".join(guesslist),
    }

#-------------------------------------------------------------------------------------

random.seed()
origlist = load_dictionary("dictionary.txt")

total = 0
for answer in origlist:
    wordlist= load_dictionary("dictionary.txt")
    count = 0
    while True:
        count += 1
        guess = get_next_guess(wordlist)
        result = grade_word(answer, guess)
        if result['grade'] == '22222':
            break;
        wordlist = reduce_word_list(wordlist, result)
    total += count
    print(answer + " " + str(count))

print (total / len(origlist))
