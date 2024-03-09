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
    :param result: A dictionary/object that stores the guess and the grade.
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
    newwordlist = [w for w in wordlist if is_possible(w, result)]
    print("My mega-intelligence has reduced the options to " + str(len(newwordlist)) + " words.")
    return newwordlist


def load_dictionary(filename):
    """
    Read the dictionary from the file and return the words as a list and
    as a hash of boolean values.

    :param filename: The file containing the official dictionary.
    :returns: wordlist, wordhash

    NOTE: The wordhash isn't really necessary in this version of the code, but will
    be useful when dealing with a user who might guess a word not in the dictionary.
    """
    wordlist = []
    wordhash = {}
    with open(filename) as f:
        for word in f:
            wordlist.append(word.rstrip())
            wordhash[word.rstrip()] = True

    print("Dictionary contains " + str(len(wordlist)) + " words.")
    return wordlist, wordhash




def get_next_guess(wordlist):
    """
    Randomly select a word from the list of words.

    :param wordlist: The list of words currently being considered.
    :returns: A randomly selected word from the list.
    """
    return wordlist[random.randint(0,len(wordlist)-1)]


def grade_word(answer, guess, wordhash):
    """
    Grades the guess by comparing it to the correct answer.

    :param answer: The answer word the computer is trying to guess.
    :param guess: The guessed word to be graded.
    :param wordhash: A hash of the original dictionary words in order to verify
        that the guess is valid.
    :returns: False if guess is not in the dictionary; otherwise returns a dictionary
        containing the original guess and the grade string.

    NOTE: The grade string contains 5 characters as follows:
     * there is a 2 if the correct letter is used in the correct place
     * there is a 1 if the correct letter is used in the wrong place
     * the original guessed letter is used if the letter does not occur in the answer
    """
    if not (guess in wordhash):
        print("The word '" + guess + "' is not in the dictionary file")
        return false

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



def show_grade(result):
    """
    Displays a graded guess using traditional color coding.

    :param result: A dictionary that stores the guess and the grade.

    Colors are:
     * text is white
     * green background if the correct letter is used in the correct place
     * yellow background if the correct letter is used in the wrong place
     * black background if the letter does not occur in the answer
    """
    print(Fore.WHITE)
    for i in range(len(result['guess'])):
        if result['grade'][i] == '2':
            print(Back.GREEN + result['guess'][i], end='')
        elif result['grade'][i] == '1':
            print(Back.YELLOW + result['guess'][i], end='')
        else:
            print(Back.BLACK + result['guess'][i], end='')
    print(Style.RESET_ALL)


#-------------------------------------------------------------------------------------

random.seed()
wordlist, wordhash = load_dictionary("dictionary.txt")
answer = get_next_guess(wordlist)

count = 0
while True:
    count += 1
    guess = get_next_guess(wordlist)
    #print(guess + "<-- Guess #" + str(count))
    result = grade_word(answer, guess, wordhash)
    show_grade(result)
    if result['grade'] == '22222':
        break;
    wordlist = reduce_word_list(wordlist, result)

