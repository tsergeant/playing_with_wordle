"""
Computer calculates fitness for each word as a starting word.

:author:  Terry Sergeant
:version: 1

NOTE: A single pass through the 13000 words takes about 5 minutes which
makes it infeasible to get stats for all words so we'll randomly choose
some and hope it is a reasonable estimate.

After playing around with 5 randomly selected words is looks like sampling 50
words will give an estimate of fitness to within about 20% of the actual.

pass1.txt -> fitness value for all words in wordlist when calculated
    using 50 randomly selected guesses.
pass1.top2500.txt -> top 2500 words from pass1


pass2.txt -> fitness value for the top 2500 words from pass1 when calculated
    using 250 randomly selected guesses.
pass2.top500.txt -> top 500 words from pass2

pass3.txt -> fitness value for the top 500 words from pass2 when calculated
    using 1000 randomly selected guesses.
pass3.top100.txt -> top 100 words from pass3

pass4.txt -> fitness value for the top 100 words from pass3 when calculated
    using 2500 randomly selected guesses. NOTE: 2500 guesses takes about 30
    seconds. (About 50 minutes to go through 100 words.)
pass4.top20.txt -> top 20 words from pass4

pass5.txt -> fitness value for the top 20 words from pass4 when calculated
    using the entire dictionary
pass5.top20.txt -> top 20 words from pass5
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
    #print("My mega-intelligence has reduced the options to " + str(len(newwordlist)) + " words.")



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

    print("Dictionary contains "+str(len(wordlist))+" words.")
    return wordlist, wordhash


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
            print(Back.YELLOW+ result['guess'][i], end='')
        else:
            print(Back.BLACK + result['guess'][i], end='')
    print(Style.RESET_ALL)



def get_next_guess(wordlist):
    """
    Randomly select a word from the list of words.

    :param wordlist: The list of words currently being considered.
    :returns: A randomly selected word from the list.
    """
    return wordlist[random.randint(0,len(wordlist)-1)]

#-------------------------------------------------------------------------------------

random.seed()
wordlist, wordhash = load_dictionary("dictionary.txt")
samplelist,samplehash = load_dictionary("pass4.top20.txt")
#sample = ['stulm']
num_trials = len(samplelist)
num_trials = len(wordlist)
for guess in samplelist:
    total = 0
    #for i in range(num_trials):
    for answer in wordlist:
        #answer = get_next_guess(wordlist)
        result = grade_word(answer, guess, wordhash)
        lst = reduce_word_list(wordlist, result)
        total += len(lst)
        #print("   " + guess + " " + answer + " " + str(len(lst)))

    print(guess + " " + str(total) + " " + str(total / num_trials))

