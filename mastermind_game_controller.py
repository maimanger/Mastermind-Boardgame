"""
    CS 5001
    Spring 2021
    Fangying Li
    Project: Mastermind Game -- Game Controller
    Create the game controller of the Mastermind game.
"""

from mastermind_game_model import GameModel

LEADERBOARD_FILENAME = "leaderboard.txt"


class Controller:
    """
    A class that controls the Mastermind Game process:
    takes user inputs and tells the GameModel what to do;
    tells the Board what to display.
    Attributes: name(str), player(str), model(GameModel), current_guess(list of str),
                current_round(int), game_status(str)
    Methods: __init__, add_model, reset_guess, add_guess, validate_filename,
            load_leaderboard_file, save_leaderboard_file, create_top_leaders_list,
            update_round, get_bulls_and_cows, get_current_guess_index, restart, 
            __str__, __eq__
    """

    def __init__(self, model = None, player = ""):
        """
        Method: __init__
            Create an instance of Controller.
        Parameters:
            model (GameModel) -- the GameModel of MasterMind game
            player (str) -- the player's name
        Return: nothing
        """

        if (model is not None and not isinstance(model, GameModel)) or \
                (player != "" and not isinstance(player, str)):
            raise TypeError("Model and player arguments must be " +
                            "GameModel class and str type!")

        self.name = "MasterMind Game Controller"
        self.player = player
        self.model = model
        self.current_guess = []
        self.current_round = 1
        self.game_status = "running"

    def add_model(self, model):
        """
        Method: add_model
            Add a GameModel attribute to the instance of Controller.
        Parameter:
            model (GameModel) -- the GameModel of MasterMind game
        Return: nothing
        """

        if not isinstance(model, GameModel):
            raise TypeError("Model must be of GameModel class!")

        self.model = model

    def reset_guess(self):
        """
        Method: reset_guess
            Reset the current_guess to a list of empty strings, which has
            the same length with the code list.
        Parameter: nothing
        Return: nothing
        """

        try:
            self.current_guess = [""] * len(self.model.code)

        # if forget to add model to a new controller
        # self.model == None, doesn't have code attribute
        except AttributeError:
            self.current_guess = []

    def add_guess(self, color, index):
        """
        Method: add_guess
            Add a new guess in the given position of the current guess-list.
        Parameters:
            color (str) -- the new guess
            index (int) -- the position index of the current guess-list
        Return: nothing
        """

        if not (isinstance(color, str) and isinstance(index, int)):
            raise TypeError("Guess and index arguments must be str and int!")

        elif index not in range(len(self.current_guess)):
            raise IndexError("The index is out of the code length!")

        elif color not in self.model.code_range:
            raise ValueError("The guess is not contained in the code range!")

        self.current_guess[index] = color

    def validate_filename(self, filename):
        """
        Method: validate_filename
            Check whether the given filename is a string .
        Parameter:
            filename (str) -- the given filename
        Return: nothing
        """

        if not isinstance(filename, str):
            raise TypeError("Filename must be a string!")

    def load_leaderboard_file(self, filename = LEADERBOARD_FILENAME):
        """
        Method: load_leaderboard_file
            Retrieve data list from leaderboard file;
            if the file don't exist, create a new file.
        Parameter:
            filename (str) -- the leaderboard filename, storing previous records
        Return:
            A list representing the data retrieved from the leaderboard file
        """

        self.validate_filename(filename)
        leaders_list = []

        try:
            with open(filename, "r") as infile:
                name = infile.readline().strip("\n")
                score = infile.readline().strip("\n")
                while name != "":  # not reach the end of file
                    leaders_list.append([name, score])
                    name = infile.readline().strip("\n")
                    score = infile.readline().strip("\n")

        except FileNotFoundError:
            outfile = open(filename, "w")
            outfile.close()

        return leaders_list

    def create_top_leaders_list(self, previous_leaders):
        """
        Method: create_top_leaders_list
            Sort the scores of the current player and previous players,
            and create a list of top five players' records.
        Parameter:
            previous_leaders (list) -- a list of previous leaders record
        Return:
            A list representing the top five leaders' records
        """

        if not isinstance(previous_leaders, list):
            raise TypeError("Argument must be a list!")
        else:
            for name, score in previous_leaders:
                if not (isinstance(name, str) and isinstance(score, str)):
                    raise TypeError("Each element in the argument list must be str!")

        # current leaders_list = [[current_player, current_score]]
        # extend previous leaders to current leaders' list
        leaders_list = [[self.player, str(self.model.score)]]
        leaders_list.extend(previous_leaders)

        # sort the current leaders' list by ascending score
        # if there is a tie between the new player and existing leaders
        # the new player will show up ahead of old records
        # because Python uses a stable sort for ties
        # items will show up in the same order they occurred
        leaders_list.sort(key=lambda x: int(x[1]))

        # return the top five leaders
        return leaders_list[:5]

    def save_leaderboard_file(self, top_leaders, filename = LEADERBOARD_FILENAME):
        """
        Method: save_leaderboard_file
            Save the updated leaders' records to leaderboard file.
        Parameters:
            top_leaders (list) -- the list of top leader' records
            filename (str) -- the leaderboard filename storing updated records
        Return: nothing
        """

        self.validate_filename(filename)
        if not isinstance(top_leaders, list):
            raise TypeError("Top leaders argument must be a list!")
        else:
            for name, score in top_leaders:
                if not (isinstance(name, str) and isinstance(score, str)):
                    raise TypeError("Each element in the argument list must be str!")

        if self.game_status == "win":
            with open(filename, "w") as outfile:
                for each in top_leaders:
                    outfile.write(each[0] + "\n")
                    outfile.write(each[1] + "\n")

    def update_round(self, infile_name = LEADERBOARD_FILENAME,
                     outfile_name = LEADERBOARD_FILENAME):
        """
        Method: update_round
            Update current game round, including update GameModel, update game_status,
            reset guess list , save leaderboard_file, update round counter.
        Parameters:
            infile_name (str) -- the leaderboard filename storing previous records
            outfile_name (str) -- the leaderboard filename storing updated records        
        Return: nothing
        """

        self.validate_filename(infile_name)
        self.validate_filename(outfile_name)

        if self.game_status == "running":
            # update GameModel
            self.model.update(self.current_guess)
            # update Controller attributes
            self.game_status = self.model.check_status()
            self.reset_guess()
            self.current_round += 1
            # save top leaders' records
            previous_leaders = self.load_leaderboard_file(infile_name)
            top_leaders = self.create_top_leaders_list(previous_leaders)
            self.save_leaderboard_file(top_leaders, outfile_name)

    def get_bulls_and_cows(self):
        """
        Method: get_bulls_and_cows
            Get the current number of bulls and cows.
        Parameter: nothing
        Return:
            A 2-tuple of integers representing the current number of bulls and cows
        """

        return self.model.bull_num, self.model.cow_num

    def get_current_guess_index(self):
        """
        Method: get_current_guess_index
            Get the index of the last non-empty position in the current guess.
        Parameter: nothing
        Return:
            An integer representing the index of the last non-empty guess
        """

        for i in range(len(self.current_guess) - 1, -1, -1):
            if self.current_guess[i] != "":
                return i
        return -1

    def restart(self):
        """
        Method: restart
            Restart the Controller without changing the player,
            including reset current_round, reset game_status ,
            and restart GameModel .
        Parameter: nothing
        Return: nothing
        """

        self.current_round = 1
        self.game_status = "running"
        self.model.restart()

    def __str__(self):
        """
        Method: __str__
            Return a string representation of Controller instance.
        Parameter: nothing
        Return:
            A string representation
        """

        return "{}\tPlayer: {}\tGame status: {}".format(self.name, self.player,
                                                        self.game_status)

    def __eq__(self, other):
        """
        Method: __eq__
            Compare current Controller instance to another one.
        Parameter:
            other (Controller) -- another instance of Controller
        Return:
            A boolean representing whether the two instances are equal
        """

        # two Controllers are equal, only if they have the same player
        # and have exactly the same object of GameModel
        return isinstance(other, Controller) and self.player == other.player \
               and self.model is other.model
