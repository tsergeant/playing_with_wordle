"""
Computer plays wordle (targeted strategic guessing).

:author:  Terry Sergeant
:version: 4

In this version the computer picks its first word: "lares" based on
pre-processing.  This will typically leave less than 300 possible words
remaining. Words having the form: _a_es are especially troublesome and
tend to result in lots of guesses when guesses are selected randomly.
So, the pre-computed word "compt" was found to be an optimal second
guess for these difficult words.

For other situations if the number of remaining words is more than 100 then we
make a random selection. Otherwise we perform an optimal calculation.
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
    newwordlist = [w for w in wordlist if is_possible(w, result)]
    #print("My mega-intelligence has reduced the options to " + str(len(newwordlist)) + " words.")
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

    #print("Dictionary contains "+str(len(wordlist))+" words.")
    return wordlist, wordhash




def get_random_guess(wordlist):
    """
    Randomly select a word from the list of words.

    :param wordlist: The list of words currently being considered.
    :returns: A randomly selected word from the list.
    """
    return wordlist[random.randint(0,len(wordlist)-1)]


def grade_word(answer, guess, wordhash, possible_letters):
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

    for i in range(len(guess)):
        if guesslist[j] > '2':
            possible_letters[ord(guesslist[j])-97] = False

    return {
        "guess": guess,
        "grade": "".join(guesslist),
        "possible" : possible_letters
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



def get_best_guess(allwords, possiblewords, wordhash, orig_possible_letters, is_hard_word):
    """
    Select a word from allwords that will on average reduce the number of
    possiblewords the most. We don't allow repeated letters to improve a score.

    :param allwords: The complete list of dictionary words.
    :param possiblewords: The words that have not yet been eliminated based
        one previous guesses.
    :param wordhash: A hash of possible words.
    :orig_possible_letters: A list of letters that are possible based on previous guesses.
    :is_hard_word: This value is true if the guess count is 1 and the grade was: .2.22

    :returns: The "best" next guess.
    """
    if len(possiblewords) < 3:
        return possiblewords[0]
    if is_hard_word:
        return "compt"
    if len(possiblewords) > 100:
        return get_random_guess(possiblewords)
    bestword = "false"
    bestscore = 20000000

    for guess in allwords:
        total = 0
        for answer in possiblewords:
            possible_letters = orig_possible_letters.copy()
            result = grade_word(answer, guess, wordhash, possible_letters)
            lst = reduce_word_list(wordlist, result)
            total += len(lst)

        if total < bestscore:
            bestword = guess
            bestscore = total

    #print(bestword + " is best word to guess with score of " +
    #        str(bestscore / len(possiblewords)))

    return bestword




#-------------------------------------------------------------------------------------

random.seed()
origlist, wordhash = load_dictionary("dictionary.txt")

f = open("wordle4commentary.txt", "w")

# We use the precalculated "optimal" guess lares as first guess
for answer in origlist:
    possible_letters = [True] * 26
    f.write(answer + ": ")
    wordlist, wordhash = load_dictionary("dictionary.txt")
    possible_letters = [True] * 26
    guess = "lares"
    result = grade_word(answer, guess, wordhash, possible_letters)
    f.write(guess + ",")
    possible_letters = result["possible"]
    count = 1

    while result['grade'] != '22222':
        wordlist = reduce_word_list(wordlist, result)
        is_hard_word = count == 1 and ((result["grade"][1]=='2' and result["grade"][4]=='2') or (result["grade"][3] == '2' and result["grade"][4] == '2'))
        guess = get_best_guess(origlist, wordlist, wordhash, possible_letters, is_hard_word)
        f.write(guess + ",")
        result = grade_word(answer, guess, wordhash, possible_letters)
        possible_letters = result["possible"]
        count += 1

    f.write("\n")
    print(answer + " " + str(count))

f.close()
