"""
    CS 5001
    Spring 2021
    Fangying Li
    Project: Mastermind Game -- Game Driver
    Create the Game Driver of the Mastermind game.
"""

from mastermind_game_model import GameModel
from mastermind_game_view import Board
from mastermind_game_controller import Controller


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


def start_game():
    """
    Function: start_game
        The driver function for MasterGame model. Initializes the game model,
        game controller, and game board.
    Parameter: nothing
    Return: nothing
    """

    # initialize the GameModel        
    model = GameModel()
    model.create_code()

    # create a Board
    board = Board()

    # initialize the Controller
    controller = Controller(model, board.ask_player())
    controller.reset_guess()

    # initialize the Board
    board.add_controller(controller)
    board.initialize_board()
    board.operate_board_objects()


def main():
    """
    MasterMind Game (one-player):
    1. Selects the 4 color secret code from 6 different colors: 'red', 'blue',
    'green', 'yellow', 'purple', 'black'.
    Blank positions and duplicate colors are allowed.
    2. Game model determines how many cows and bulls generated from current guess.
    The program uses black pegs for cows and red pegs for bulls.
    3. The score is the number of guesses it takes the player to guess the code.
    Player loses if they don't guess the code in 10 tries. Lower scores are better.
    4. Allows player to play multiple rounds of the game without quitting.
    5. Player can either click the Marble to make a guess, or drag the Marble to
    the guessing position.   
    """

    start_game()


if __name__ == "__main__":
    main()
