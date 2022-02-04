"""
    CS 5001
    Spring 2021
    Fangying Li
    Project: Mastermind Game -- Game Model
    Create the game model of the Mastermind game.
"""

import random

COLORS = ["red", "blue", "green", "yellow", "purple", "black", ""]
CODE_LENGTH = 4
MAX_GUESS = 10


class GameModel:
    """
    A class that implement the Mastermind game rules.
    Attributes: name(str), code(list), code_range(list of str), guess(list of str),
                max_guess(int), score(int), bull_num(int), cow_num(int)
    Methods: __init__, create_code, update, check_status, restart, __str__, __eq__
    """

    def __init__(self, max_guess = MAX_GUESS, code_range = COLORS):
        """
        Method: __init__
            Create an instance of GameModel.
        Parameters:
            max_guess (int) -- the maximum guess allowed in the game
            code_range (list) -- the range of the code values            
        Return: nothing
        """

        if not (isinstance(max_guess, int) and isinstance(code_range, list)):
            raise TypeError("Max guess and code range arguments must be" +
                            "integer and list!")
        elif max_guess < 0:
            raise ValueError("Argument must be non-negative!")

        elif len(code_range) == 0:
            raise ValueError("Code range cannot be empty list!")

        self.name = "Mastermind Game"
        self.code = []
        self.code_range = code_range

        self.guess = []
        self.max_guess = max_guess

        self.score = 0
        self.bull_num = 0
        self.cow_num = 0

    def create_code(self, length = CODE_LENGTH):
        """
        Method: create_code
            Create an randomized code of the GameModel.
            Duplicate and blanks in the code are allowed.
        Parameter:
            length (int) -- the length of the code
        Return: nothing
        """

        if not isinstance(length, int):
            raise TypeError("The length of code must be an integer!")

        elif length <= 0:
            raise ValueError("The length of code must be positive!")

        self.code = random.choices(self.code_range, k=length)
        #print(self.code)

    def update(self, guess):
        """
        Method: update
            Update the guess with its bulls and cows, and the current score.
        Parameter:
            guess (list) -- the code-guess from the player
        Return: nothing
        """

        if not isinstance(guess, list):
            raise TypeError("Argument must be list!")

        elif len(guess) != len(self.code):
            raise ValueError("The guess argument must have" +
                             " the same length of the code!")

        elif self.score < self.max_guess:
            self.score += 1
            self.guess = guess
            self.bull_num, self.cow_num = count_bulls_and_cows(
                self.code, self.guess)

    def check_status(self):
        """
        Method: check_status
            Check the current game status: "win", "lost", or "running".
        Parameter: nothing
        Return:
            A string representing current game status
        """

        if self.score <= self.max_guess and self.bull_num == len(self.code):
            return "win"
        elif self.score == self.max_guess and self.bull_num < len(self.code):
            return "lost"
        else:
            return "running"

    def restart(self):
        """
        Method: restart
            Restart the game model, including code recreation;
            guess, score, bull_num, and cow_num reset.
        Parameter: nothing
        Return: nothing  
        """

        self.create_code()
        self.guess = []
        self.score, self.bull_num, self.cow_num = 0, 0, 0

    def __str__(self):
        """
        Method: __str__
            Get the string description of GameModel instance:
            game name, current code, current guess, current score.
        Parameter: nothing
        Return:
            An string description of GameModel
        """

        return "{}\tCode: {}\tScore: {}".format(self.name, self.code, self.score)

    def __eq__(self, other):
        """
        Method: __eq__
            Compare an instance of GameModel to another one.
            Two instances are equal if they have the same code, guess, and score.
        Parameter:
            other (GameModel) --another instance of GameModel
        Return:
            A boolean representing whether the two instances are equal
        """

        return isinstance(other, GameModel) and self.code == other.code and \
               self.guess == other.guess and self.score == other.score


def count_bulls_and_cows(secret_code, guess):
    """
    Function: count_bulls_and_cows
        Calculate the num of bulls and cows in mastermind game.
        Bulls represent the correct guess in correct positions;
        cows represent the correct guess in incorrect positions.
    Parameters:
        secret_code (list of str) -- the color code generated from GameModel
        guess (list of str) -- the color guess from the player
    Return:
        A 2-tuple containing the number of bulls and cows
    """

    # SAME as the function count_bulls_and_cows in mastermind_game.py
    # Repeat this function here to AVOID circular import

    if not (isinstance(secret_code, list) and isinstance(guess, list)):
        raise TypeError("Color code and color guess must be lists!")

    elif len(secret_code) != len(guess):
        raise ValueError("The length of color code and color guess must be equal!")

    else:
        bull_num, cow_num = 0, 0
        code_copy, guess_copy = secret_code[:], guess[:]

        # count the correct guess in correct position
        for i in range(len(guess)):
            if guess[i] == secret_code[i]:
                bull_num += 1
                # remove the bulls already counted
                guess_copy.remove(guess[i])
                code_copy.remove(secret_code[i])

        # count the correct guess in incorrect position
        for each in guess_copy:
            if each in code_copy:
                cow_num += 1
                # remove the cows already counted
                code_copy.remove(each)

    return bull_num, cow_num
