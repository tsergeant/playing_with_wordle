"""
Computer plays wordle (semi-strategic guessing).

:author:  Terry Sergeant
:version: 3

In this version the computer picks its first word: "lares" based on pre-processing.
This will typically leave less than 300 possible words remaining. If remaining words
is more than 50 we use this strategy:
    1) count letter frequencies of remaining words
    2) set counts to 0 for letters we know are already in the word
    3) sort letter frequency by count
    4) find a word that uses lots of highly occurring letters not known to
        be in the word

If remaining words is 50 or less we'll exhaustively find the guess the produces
the smallest remaining number of words and use that word.
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

    return wordlist, wordhash




def get_random_guess(wordlist):
    """
    Randomly select a word from the list of words.

    :param wordlist: The list of words currently being considered.
    :returns: A randomly selected word from the list.
    """
    return wordlist[random.randint(0,len(wordlist)-1)]


def get_freq_word(allwords, possiblewords, possibleletters):
    """
    This makes a guess by getting letter frequencies or remaining words and choosing
    a word (from the possiblewords list) that maximizes frequency.
    """
    freq = {}
    for word in possiblewords:
        for let in word:
            freq[let] = freq.get(let, 0) + 1

    for i in range(26):
        if not possibleletters[i]:
            freq[chr(i+97)] = 0

    bestword = "false"
    bestscore = -1
    for word in possiblewords:
        score = 0
        pos = 0
        for let in word:
            if not (let in word[:pos]):
                score += freq[let]
            pos += 1
        if score > bestscore:
            bestword = word
            bestscore = score

    return bestword


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



def show_grade(result, f):
    """
    Displays a graded guess using traditional color coding.

    :param result: A dictionary that stores the guess and the grade.

    Colors are:
     * text is white
     * green background if the correct letter is used in the correct place
     * yellow background if the correct letter is used in the wrong place
     * black background if the letter does not occur in the answer
    """
    f.write(Fore.WHITE)
    #print(Fore.WHITE, end='')
    for i in range(len(result['guess'])):
        if result['grade'][i] == '2':
            f.write(Back.GREEN + result['guess'][i])
            #print(Back.GREEN + result['guess'][i], end='')
        elif result['grade'][i] == '1':
            f.write(Back.YELLOW+ result['guess'][i])
            #print(Back.YELLOW+ result['guess'][i], end='')
        else:
            f.write(Back.BLACK + result['guess'][i])
            #print(Back.BLACK + result['guess'][i], end='')
    f.write(Style.RESET_ALL)
    #print(Style.RESET_ALL)



def get_best_guess(allwords, possiblewords, wordhash, orig_possible_letters):
    """
    Select a word from allwords that will on average reduce the number of
    possiblewords the most. We don't allow repeated letters to improve a score.

    :param allwords: The complete list of dictionary words.
    :param possiblewords: The words that have not yet been eliminated based
        one previous guesses.
    :returns: The "best" next guess.
    """
    bestword = "false"
    bestscore = 20000000
    #print(possiblewords)
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

f = open("wordle3commentary.txt", "w")

# We use the precalculated "optimal" guess lares as first guess
for answer in origlist:
    f.write(answer + ": ")
    wordlist, wordhash = load_dictionary("dictionary.txt")
    possible_letters = [True] * 26
    guess = "lares"
    result = grade_word(answer, guess, wordhash, possible_letters)
    f.write(guess + ",")
    possible_letters = result["possible"]
    #show_grade(result, f)
    count = 1


    # Then we make guesses based on letter frequency until we get down to
    # 60 possible answers left and then we do optimal calculation on the fly.
    # If we get down to 1 or 2 guesses then we randomly choose.
    while result['grade'] != '22222':
        wordlist = reduce_word_list(wordlist, result)
        #print("List reduced to: " + str(len(wordlist)))
        if len(wordlist) > 60:
            guess = get_freq_word(origlist, wordlist, possible_letters)
        elif len(wordlist) > 2:
            guess = get_best_guess(origlist, wordlist, wordhash, possible_letters)
        else:
            guess = get_random_guess(wordlist)

        result = grade_word(answer, guess, wordhash, possible_letters)
        f.write(guess + ",")
        possible_letters = result["possible"]
        #show_grade(result, f)
        count += 1

    f.write("\n")
    print(answer + " " + str(count))

f.close()
