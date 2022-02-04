"""
    CS 5001
    Spring 2021
    Fangying Li
    Project: Mastermind Game -- Game View
    Create the game user-interface of the Mastermind game.
"""

import turtle
import time
import tkinter
from mastermind_game_helper import Point, validate_position
from mastermind_game_controller import Controller

WINDOW_TITLE = "CS5001 MasterMind Code Game"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 750
BACKGROUND = "background.png"

PLAY_AREA_START = (-390, -280)
PLAY_AREA_SIDES = [780, 80, 780, 80]

STATUS_AREA_START = (-390, 360)
STATUS_AREA_SIDES = [500, 620, 500, 620]

LEADERBOARD_START = (150, 360)
LEADERBOARD_SIDES = [240, 620, 240, 620]

PIT_START = (-295, 325)
ROW_SPACE, COLUMN_SPACE = 60, 80

PIT_TO_PEG_X, PIT_TO_PEG_Y = 85, 10
PEG_SPACE = 20

MARBLE_START = (-330, -320)
MARBLE_SPACE = 60
MARBLE_COLORS = ["blue", "red", "green", "yellow", "purple", "black"]

CHECK_BUTTON_START = (50, -320)
CANCEL_BUTTON_START = (130, -320)
RESTART_BUTTON_START = (230, -320)
QUIT_BUTTON_START = (330, -320)
ROW_MARKER_START = (-350, 325)

WRITTEN_START = (270, 315)
WRITTEN_LINE_SPACE = 50

PICTURES = ["file_error.gif", "leaderboard_error.gif", "winner.gif", "lose.gif",
            "you_quit.gif", "marble_blue.gif", "marble_red.gif", "marble_green.gif",
            "marble_yellow.gif", "marble_purple.gif", "marble_black.gif",
            "check_button.gif", "cancel_button.gif", "restart.gif", "quit.gif",
            "row_marker.gif"]


class BoardObject(turtle.Turtle):
    """
    A class that represents objects on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size, position, board, name
    Methods: __init__, validate, draw_self, __str__, __eq__
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of BoardObject.
        Parameters:
            color (str) -- a string represents the object color
            shape (str) -- a string represents the object shape
            size (int or float) -- an int or a float represents the object size
            position (tuple) -- a tuple of two numbers (int or float),
                                representing the BoardObject position
            board (Board) -- the Board to which the BoardObject belongs to
        Return: nothing
        """

        super().__init__()
        self.default_color = color
        self.default_shape = shape
        self.default_size = size
        self.position = position
        self.board = board
        self.name = "Board Object"
        self.validate()

    def validate(self):
        """
        Method: validate
            Check if the attributes of BoardObject are valid.
        Parameter: nothing
        Return: nothing
        """

        # check each attribute's type
        if not (isinstance(self.default_color, str) and
                isinstance(self.default_shape, str) and
                isinstance(self.position, tuple) and
                isinstance(self.board, Board)) \
                or not (isinstance(self.default_size, int) or
                        isinstance(self.default_size, float)):
            raise TypeError("Invalid BoardObject arguments: " +
                            "color must be str; shape must be str; " +
                            "position must be tuple; board must be Board; " +
                            "size must be int or float!")

        # check if the size is positive
        elif self.default_size <= 0:
            raise ValueError("Size argument must be positive!")

        # check if the position is a 2-tuple of ints or floats
        else:
            validate_position(self.position)

    def draw_self(self, shape_pic):
        """
        Method: draw_self
            Draw the BoardObject based on the given shape, color, size, position.
        Parameter:
            shape_pic (str) -- the name of the BoardObject's shape picture
        Return: nothing
        """

        try:
            self.shape(shape_pic)
        # if the shape picture is not registered
        # pop up file-error message
        # use the default shape, color, and size
        except turtle.TurtleGraphicsError:
            self.board.pop_message("file_error.gif")
            self.shape(self.default_shape)
            self.color(self.default_color)
            self.shapesize(self.default_size)

        self.speed(0)
        self.up()
        self.goto(self.position)

    def __str__(self):
        """
        Method: __str__
            Return a string representation of BoardObject instance.
        Parameter: nothing
        Return:
            A string representation
        """

        return self.name

    def __eq__(self, other):
        """
        Method: __eq__
            Compare current BoardObject instance to another one.
        Parameter:
            other (BoardObject) -- another instance of BoardObject
        Return:
            A boolean representing whether the two instances are equal
        """

        return type(self) == type(other) and self.name == other.name


class Marble(BoardObject):
    """
    A class that represents the Marble on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size,
                position, board, name, stamps
    Methods: __init__, validate, draw_self, __str__, __eq__,
             drag_guess, drag_draw, click_guess, click_draw
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of Marble.
        Parameters:
            color (str) -- a string represents the Marble color
            shape (str) -- a string represents the Marble shape
            size (int or float) -- an int or a float represents the Marble size
            position (tuple of int or float) -- (x, y) coordinate of the o
                                                 Marble position
            board (Board) -- the Board to which the Marble belongs to
        Return: nothing
        """

        super().__init__(color, shape, size, position, board)
        self.name = "marble"
        # contains the stampid integer returned from a stamp-call of the Marble
        self.stamps = []

    def drag_guess(self, x, y):
        """
        Method: drag_guess
            Complete one guess by dragging the Marble object to a certain
            position on the Board.
        Parameters:
            x (float) -- x coordinate where the mouse-click released
            y (float) -- y coordinate where the mouse-click released
        Return: nothing
        """

        current_point = Point(x, y)

        # if the Marble stamp succeeded
        # add new guess to the Controller's guess list
        new_guess_index = self.drag_draw(current_point)
        if new_guess_index >= 0:
            self.board.controller.add_guess(self.default_color, new_guess_index)

    def drag_draw(self, current_point):
        """
        Method: drag_draw
            Draw a stamp by dragging the Marble to the available pit's position
            on the Board.
        Parameters:
            current_point (Point) -- the position where the mouse-click releases
        Return:
            An integer representing the column index there the Marble stamped
        """

        # get pits positions of current row
        current_pits_row = self.board.status_area.get_current_pits_row()

        # go through each available pit 
        for column in range(len(current_pits_row)):
            stamp_point = current_pits_row[column]

            # if the current position is close enough to the pit
            # and there is no Marble stamped on this pit
            # and the game is running
            if current_point.get_distance(stamp_point) <= 20 and \
                    self.board.controller.current_guess[column] == "" and \
                    not self.board.is_end:
                # draw a Marble stamp
                # register this stamp to the Marble stamps-attribute
                self.goto(stamp_point.x, stamp_point.y)
                stampid = self.stamp()
                self.stamps.append(stampid)

                # Marble goes back to its default position
                self.goto(self.position)
                return column

        # if no stamp succeeded
        self.goto(self.position)
        return -1

    def click_guess(self, x, y):
        """
        Method: click_guess
            Complete one guess by clicking the Marble object on the Board.
        Parameters:
            x (float) -- x coordinate where the mouse-click clicked
            y (float) -- y coordinate where the mouse-click clicked
        Return: nothing
        """

        # if the Marble stamp succeeded
        # add new guess to the Controller's guess list
        new_guess_index = self.click_draw()
        if new_guess_index >= 0:
            self.board.controller.add_guess(self.default_color, new_guess_index)

    def click_draw(self):
        """
        Method: click_draw
            Draw a stamp by clicking the Marble on the Board.
        Parameter: nothing
        Return: nothing
        """

        # get pits position of current row
        # get the index of the last non-empty pit (with a Marble guess on it)
        # look at the next empty pit
        current_pits_row = self.board.status_area.get_current_pits_row()
        current_column = self.board.controller.get_current_guess_index()
        new_guess_index = current_column + 1

        # if the next empty pit is within the column range
        # and the game is running
        if new_guess_index < self.board.column_num and not self.board.is_end:

            # draw a Marble stamp on this pit
            stamp_point = current_pits_row[new_guess_index]
            self.goto(stamp_point.x, stamp_point.y)
            stampid = self.stamp()
            time.sleep(0.1)  # holds on 0.1 second for next event

            # register this stamp to the Marble stamps-attribute
            self.stamps.append(stampid)

            # Marble back to its default position
            self.goto(self.position)

            return new_guess_index

        # if no stamp succeeded
        else:
            return -1


class Check(BoardObject):
    """
    A class that represents the Check-Button on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size,
                position, board, name
    Methods: __init__, validate, draw_self, __str__, __eq__, click_check
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of Check.
        Parameters:
            color (str) -- a string represents the Check-Button color
            shape (str) -- a string represents the Check-Button shape
            size (int or float) -- an int or a float represents the
                                   Check-Button size
            position (tuple of int or float) -- (x, y) coordinate of the o
                                                 Check-Button position
            board (Board) -- the Board to which the Check-Button belongs to
        Return: nothing
        """

        super().__init__(color, shape, size, position, board)
        self.name = "check_button"

    def click_check(self, x, y):
        """
        Method: click_check
            Confirm the guess in the current round by clicking the
            Check-Button on the Board, including:
            Update the Controller;
            Update the pegs and the Row-Marker on the Board;
            Show the end message on the Board.
        Parameters:
            x (float) -- x coordinate where the mouse-click clicked
            y (float) -- y coordinate where the mouse-click clicked
        Return: nothing
        """

        # Controller update the game round
        self.board.controller.update_round()

        # new row-index on Board = Controller.current_round - 1
        # we need to update pegs generated from last round/row
        # the row-index of pegs update = Controller.current_round - 2
        self.board.status_area.draw_pegs(self.board.controller.current_round - 2)

        # show end message 
        self.board.show_end_message()

        # if game isn't end
        # update the row-marker for new round 
        self.board.buttons["row_marker"].update()

        # clean all Marble-stamps memory from last round
        # otherwise we might accidentally erase the stamps from previous rounds
        self.board.clear_marbles_stamp_memory()

        time.sleep(0.5)  # holds on 0.5 second for next event


class Cancel(BoardObject):
    """
    A class that represents the Cancel-Button on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size,
                position, board, name
    Methods: __init__, validate, draw_self, __str__, __eq__, click_cancel
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of Cancel.
        Parameters:
            color (str) -- a string represents the Cancel-Button color
            shape (str) -- a string represents the Cancel-Button shape
            size (int or float) -- an int or a float represents the
                                   Cancel-Button size
            position (tuple of int or float) -- (x, y) coordinate of the o
                                                 Cancel-Button position
            board (Board) -- the Board to which the Cancel-Button belongs to
        Return: nothing
        """

        super().__init__(color, shape, size, position, board)
        self.name = "cancel_button"

    def click_cancel(self, x, y):
        """
        Method: click_cancel
            Cancel the guess in the current round by clicking the
            Cancel-Button on the Board, including:
            Erase all stamps in the current round;
            Reset Controller's guess list.
        Parameters:
            x (float) -- x coordinate where the mouse-click clicked
            y (float) -- y coordinate where the mouse-click clicked
        Return: nothing
        """

        if not self.board.is_end:
            # erase all stamps drawing
            self.board.erase_current_stamps()
            # reset Controller's guess list
            self.board.controller.reset_guess()


class Restart(BoardObject):
    """
    A class that represents the Restart-Button on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size,
                position, board, name
    Methods: __init__, validate, draw_self, __str__, __eq__, click_restart
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of Restart.
        Parameters:
            color (str) -- a string represents the Restart-Button color
            shape (str) -- a string represents the Restart-Button shape
            size (int or float) -- an int or a float represents the
                                   Restart-Button size
            position (tuple of int or float) -- (x, y) coordinate of the o
                                                 Restart-Button position
            board (Board) -- the Board to which the Restart-Button belongs to
        Return: nothing
        """

        super().__init__(color, shape, size, position, board)
        self.name = "restart"

    def click_restart(self, x, y):
        """
        Method: click_restart
            Restart the MasterMind Game by clicking the
            Restart-Button on the Board, including restart the Controller
            and reset the Board.
        Parameters:
            x (float) -- x coordinate where the mouse-click clicked
            y (float) -- y coordinate where the mouse-click clicked
        Return: nothing
        """

        if self.board.is_end:
            self.board.controller.restart()
            self.board.reset_board()


class Quit(BoardObject):
    """
    A class that represents the Quit-Button on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size,
                position, board, name
    Methods: __init__, validate, draw_self, __str__, __eq__, click_quit
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of Quit.
        Parameters:
            color (str) -- a string represents the Quit-Button color
            shape (str) -- a string represents the Quit-Button shape
            size (int or float) -- an int or a float represents the
                                   Quit-Button size
            position (tuple of int or float) -- (x, y) coordinate of the o
                                                 Quit-Button position
            board (Board) -- the Board to which the Quit-Button belongs to
        Return: nothing
        """

        super().__init__(color, shape, size, position, board)
        self.name = "quit"

    def click_quit(self, x, y):
        """
        Method: click_quit
            Quit the MasterMind Game by clicking the Quit-Button on the Board.
        Parameters:
            x (float) -- x coordinate where the mouse-click clicked
            y (float) -- y coordinate where the mouse-click clicked
        Return: nothing
        """

        self.board.pop_message("you_quit.gif")
        turtle.bye()


class RowMarker(BoardObject):
    """
    A class that represents the Row-Marker on the Mastermind Game Board.
    Attributes: default_color, default_shape, default_size,
                position, board, name
    Methods: __init__, validate, draw_self, __str__, __eq__, update
    """

    def __init__(self, color, shape, size, position, board):
        """
        Method: __init__
            Create an instance of RowMarker.
        Parameters:
            color (str) -- a string represents the RowMarker color
            shape (str) -- a string represents the RowMarker shape
            size (int or float) -- an int or a float represents the
                                   RowMarker size
            position (tuple of int or float) -- (x, y) coordinate of the o
                                                 RowMarker position
            board (Board) -- the Board to which the RowMarker belongs to
        Return: nothing
        """

        super().__init__(color, shape, size, position, board)
        self.name = "row_marker"

    def update(self, row_space = ROW_SPACE):
        """
        Method: update
            Update the RowMarker's position for each game-round.
        Parameter:
            row_space (int or float) -- the row space of the RowMarker
        Return: nothing
        """

        if not isinstance(row_space, int):
            raise TypeError("RowMarker space argument must be integer!")
        elif row_space <= 0:
            raise ValueError("RowMarker space must be positive!")

        if not self.board.is_end:
            new_row_index = self.board.controller.current_round - 1
            new_y = self.position[1] - new_row_index * row_space
            self.goto(self.position[0], new_y)


class Board:
    """
    A class that represents the Mastermind Game Board, is in charge of the
    user interface of the game.
    Attributes: name, row_num, column_num, window, pen, leaderboard, status_area,
                marbles, buttons, controller, is_end
    Methods: __init__, new_pen, new_window, ask_player, add_controller,
             register_pictures, pop_message, initialize_board, draw_area,
             validate_area, initialize_marbles, validate_marbles, initialize_buttons,
             new_check_button, new_cancel_button, new_restart_button,
             new_quit_button, new_row_marker, erase_current_stamps, reset_board,
             show_end_message, clear_marbles_stamp_memory, operate_board_objects,
             __str__, __eq__
    """

    def __init__(self):
        """
        Method: __init__
            Create an instance of Board.
        Parameter: nothing
        Return: nothing
        """

        self.name = "MasterMind Game Board"
        self.row_num = 0
        self.column_num = 0

        self.window = self.new_window()
        self.pen = self.new_pen()

        self.controller = None
        self.leaderboard = None
        self.status_area = None

        self.marbles = []
        self.buttons = {}  # dictionary: key = button name, value = button object

        self.is_end = False

    def new_pen(self):
        """
        Method: new_pen
            Create a turtle object as a pen of the Board.
        Parameter: nothing
        Return:
            A turtle object used by the Board
        """

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        return pen

    def new_window(self, title = WINDOW_TITLE, background = BACKGROUND,
                   width = WINDOW_WIDTH, height = WINDOW_HEIGHT):
        """
        Method: new_window
            Create a screen object as the window of the Board.
        Parameters:
            title (str) -- the title of the Board window
            background (str) -- the background picture of the Board window
            width (int or float) -- the width of the Board window
            height (int or float) -- the height of the Board window
        Return:
            A screen object used by the Board
        """

        self.validate_window(title, background, width, height)

        # initialize the window's title, size, and background
        window = turtle.Screen()
        window.setup(width, height)
        window.title(title)
        try:
            window.bgpic(background)
        # if cannot find/open picture file
        # file-error message pop up
        # use default setting of the background
        except tkinter.TclError:
            self.pop_message("file_error.gif")
            window.bgcolor("wheat")

        return window

    def validate_window(self, title, background, width, height):
        """
        Method: validate_window
            Check if the Board window's arguments are valid.
        Parameters: 
            title (str) -- the title of the Board window
            background (str) -- the background picture of the Board window
            width (int or float) -- the width of the Board window
            height (int or float) -- the height of the Board window
        Return: nothing
        """

        # check each argument's type
        if not (isinstance(title, str) and isinstance(background, str)) \
                or not (isinstance(width, int) or isinstance(width, float)) \
                or not (isinstance(height, int) or isinstance(height, float)):
            raise TypeError("Window's title and background arguments must be str, "
                            + "width and height arguments must be int or float!")
        # check if width and height are positive
        elif not (width > 0 and height > 0):
            raise ValueError("Window's width and height must be positive!")

    def ask_player(self):
        """
        Method: ask_player
            Ask the player to input their name.
        Parameter: nothing
        Return:
            A string representing the player's name
        """

        prompt = "Welcome to MasterMind!\n" + \
                 "Try using the left-click to click or right-click to drag!\n" + \
                 "Please enter your Name (maximum 16 letters):"
        player_name = self.window.textinput("CS5001 MasterMind", prompt)

        while not player_name or len(player_name) > 16:
            player_name = self.window.textinput("CS5001 MasterMind", prompt)

        return player_name

    def add_controller(self, controller):
        """
        Method: add_controller
            Bind a Controller to the Board, then initialize the numbers of
            rows and columns on the Board based on the Controller.
        Parameters:
            controller (Controller) -- the Controller of the MasterMind Game
        Return: nothing
        """

        if not isinstance(controller, Controller):
            raise TypeError("Board controller must be of Controller class!")

        self.controller = controller
        self.row_num = controller.model.max_guess
        self.column_num = len(controller.model.code)

    def register_pictures(self, pictures = PICTURES):
        """
        Method: register_pictures
            Register the customized pictures on the Board.
        Parameter:
            pictures (list of str) -- list of the pictures' names
        Return: nothing
        """

        if not isinstance(pictures, list):
            raise TypeError("Pictures argument must be a list!")
        for each in pictures:
            if not isinstance(each, str):
                raise TypeError("Each picture's name must be string!")
            try:
                self.window.addshape(each)
            # if cannot register any picture file, pass
            # the file-error message will pop up when using the picture
            except tkinter.TclError:
                pass

    def pop_message(self, message_type):
        """
        Method: pop_message
            Pop up a message picture on the Board.
        Parameter:
            message_type (str) -- the name of the message picture
        Return: nothing
        """

        if not isinstance(message_type, str):
            raise TypeError("Message type must be str!")

        msg_pen = self.new_pen()
        msg_pen.up()
        # display message picture
        try:
            msg_pen.shape(message_type)
            msg_pen.showturtle()

        # if cannot find any message picture
        # write the message name on the Board 
        except turtle.TurtleGraphicsError:
            msg_pen.pencolor("red")
            msg_pen.write(message_type.replace(".gif", ""), False, "center",
                          font=("Arial", 26, "bold"))

        time.sleep(3)  # message stays for 3 seconds
        msg_pen.clear()
        msg_pen.hideturtle()

    def initialize_board(self):
        """
        Method: initialize_board
            Initialize the Board, including create and draw the board areas and
            board objects.
        Parameter: nothing
        Return: nothing
        """

        self.register_pictures()

        # initialize leaderboard area
        self.leaderboard = LeaderBoard(self)
        self.leaderboard.draw_area()
        self.leaderboard.write_leaders()

        # initialize status area
        self.status_area = BoardStatusArea(self)
        self.status_area.draw_area()
        self.status_area.locate_pits_and_pegs()
        self.status_area.initialize_pits()
        self.status_area.initialize_pegs()

        # initialize play area and create board objects
        self.draw_area(PLAY_AREA_START, PLAY_AREA_SIDES)
        self.initialize_marbles()
        self.initialize_buttons()

    def draw_area(self, start, sides):
        """
        Method: draw_area
            Draw a rectangle area on the Board, based on given start position
            and sides length.
        Parameters:
            start (tuple) -- A tuple of 2 numbers(int or float), representing
                             the left-up point of the area
            sides (list) -- A list of 4 positive integers, representing the
                            up-side, right-side, down-side, left-side of the area
        Return: nothing
        """

        self.validate_area(start, sides)
        self.pen.color("dim gray")
        self.pen.pensize(2)
        self.pen.up()
        self.pen.goto(start)
        self.pen.down()

        for each in sides:
            self.pen.forward(each)
            self.pen.right(90)

    def validate_area(self, start, sides):
        """
        Method: validate_area
            Check if the given area arguments are valid.
        Parameters:
            start (tuple) -- A tuple of 2 numbers(int or float), representing
                             the left-up point of the area
            sides (list) -- A list of 4 positive integers, representing the
                            up-side, right-side, down-side, left-side of the area
        Return: nothing
        """

        # check all arguments types
        if not (isinstance(start, tuple) and isinstance(sides, list)):
            raise TypeError("Area start and sides arguments must be tuple and list!")

        # check if the sides argument is a list of 4 positive integers
        elif len(sides) != 4:
            raise ValueError("Area sides argument must has the length of 4!")
        else:
            for each in sides:
                if not (isinstance(each, int) and each > 0):
                    raise ValueError("Area side must be a positive integer!")

        # check if the start argument is a tuple of two numbers (int or float)
        validate_position(start)

    def initialize_marbles(self, marble_start = MARBLE_START,
                           marble_space = MARBLE_SPACE,
                           marble_colors = MARBLE_COLORS):
        """
        Method: initialize_marbles
            Initialize all Marbles on the Board.
        Parameters:
            marble_start (tuple) -- the tuple of two numbers(int or float),
                                    representing the first Marble's position
            marble_space (int) -- the space between each Marble
            marble_colors (list) -- the list of strings, containing all
                                    Marble colors
        Return: nothing
        """

        self.validate_marbles(marble_start, marble_space, marble_colors)

        for i in range(len(marble_colors)):
            # create Marble object
            position = (marble_start[0] + i * marble_space, marble_start[1])
            color = marble_colors[i]
            self.marbles.append(Marble(color, "circle", 1.8, position, self))
            # draw Marble object
            self.marbles[i].draw_self(self.marbles[i].name + "_" +
                                      self.marbles[i].default_color + ".gif")

    def validate_marbles(self, marble_start, marble_space, marble_colors):
        """
        Method: validate_marbles
            Check if the Marble arguments are valid.
        Parameters:
            marble_start (tuple) -- the tuple of two numbers(int or float),
                                    representing the first Marble's position
            marble_space (int) -- the space between each Marble
            marble_colors (list) -- the list of strings, containing all
                                    Marble colors
        Return: nothing
        """

        # check the Marble arguments' types
        if not (isinstance(marble_start, tuple) and isinstance(marble_space, int)
                and isinstance(marble_colors, list)):
            raise TypeError("Invalid marble arguments: " +
                            "marble_start must be tuple; " +
                            "marble_space must be integer; " +
                            "marble_colors must be list!")

        # check if the marble_space is positive
        elif marble_space <= 0:
            raise ValueError("Marble_space argument must be positive!")

        # check if the intersection of marble_colors and the code_range
        # equals to marble_colors itself
        elif set(marble_colors).intersection(self.controller.model.code_range) != \
                set(marble_colors):
            raise ValueError("Marble_colors argument contains invalid item!")

        # check if the marble_start is a tuple of two numbers (int or float)
        else:
            validate_position(marble_start)

    def initialize_buttons(self):
        """
        Method: initialize_buttons
            Initialize all buttons on the Board, including: check_button,
            cancel_button, restart_button, quit_button, row_marker.
        Parameter: nothing
        Return: nothing
        """

        buttons = [self.new_check_button(), self.new_cancel_button(),
                   self.new_restart_button(), self.new_quit_button(),
                   self.new_row_marker()]

        for name, button in buttons:
            self.buttons[name] = button
            button.draw_self(name + ".gif")

    def new_check_button(self, button_start=CHECK_BUTTON_START,
                         color="green", shape="circle", size=2.5):
        """
        Method: new_check_button
            Create a new check_button.
        Parameters: 
            button_start (tuple) -- a tuple of two numbers (int or float),
                                    representing the button position
            color (str) -- the button's default color
            shape (str) -- the button's default shape
            size (int or float) -- the button's default size
        Return:
            A tuple containing the button's name and the button object
        """

        check_button = Check(color, shape, size, button_start, self)
        return check_button.name, check_button

    def new_cancel_button(self, button_start = CANCEL_BUTTON_START,
                          color = "red", shape = "circle", size = 2.5):
        """
        Method: new_cancel_button
            Create a new cancel_button.
        Parameters: 
            button_start (tuple) -- a tuple of two numbers (int or float),
                                    representing the button position
            color (str) -- the button's default color
            shape (str) -- the button's default shape
            size (int or float) -- the button's default size
        Return:
            A tuple containing the button's name and the button object
        """

        cancel_button = Cancel(color, shape, size, button_start, self)
        return cancel_button.name, cancel_button

    def new_restart_button(self, button_start=RESTART_BUTTON_START,
                           color = "lime green", shape = "square", size = 2.5):
        """
        Method: new_restart_button
            Create a new restart_button.
        Parameters: 
            button_start (tuple) -- a tuple of two numbers (int or float),
                                    representing the button position
            color (str) -- the button's default color
            shape (str) -- the button's default shape
            size (int or float) -- the button's default size
        Return:
            A tuple containing the button's name and the button object
        """

        restart_button = Restart(color, shape, size, button_start, self)
        return restart_button.name, restart_button

    def new_quit_button(self, button_start = QUIT_BUTTON_START,
                        color = "indian red", shape = "square", size = 2.5):
        """
        Method: new_quit_button
            Create a new quit_button.
        Parameters: 
            button_start (tuple) -- a tuple of two numbers (int or float),
                                    representing the button position
            color (str) -- the button's default color
            shape (str) -- the button's default shape
            size (int or float) -- the button's default size
        Return:
            A tuple containing the button's name and the button object
        """

        quit_button = Quit(color, shape, size, button_start, self)
        return quit_button.name, quit_button

    def new_row_marker(self, button_start = ROW_MARKER_START,
                       color = "crimson", shape = "arrow", size = 1.5):
        """
        Method: new_row_marker
            Create a new row_marker.
        Parameters: 
            button_start (tuple) -- a tuple of two numbers (int or float),
                                    representing the button position
            color (str) -- the button's default color
            shape (str) -- the button's default shape
            size (int or float) -- the button's default size
        Return:
            A tuple containing the button's name and the button object
        """

        row_marker = RowMarker(color, shape, size, button_start, self)
        return row_marker.name, row_marker

    def erase_current_stamps(self):
        """
        Method: erase_current_stamps
            Erase stamps of all Marbles in the current round.
        Parameter: nothing
        Return: nothing
        """

        # erase stamps from current game round
        # which are registered in the Marble's stamp-attribute
        for a_marble in self.marbles:
            for a_stamp in a_marble.stamps[:]:
                a_marble.clearstamp(a_stamp)
                # remove all stamp attributes of this Marble
            a_marble.stamps = []

    def erase_all_stamps(self):
        """
        Method: erase_all_stamps
            Erase all Marble stamps drawing to start new game.
        Parameter: nothing
        Return: nothing
        """

        for a_marble in self.marbles:
            a_marble.clearstamps()

    def clear_marbles_stamp_memory(self):
        """
        Method: clear_marbles_stamp_memory
            Clean all Marbles' stamps attribute generated from the last round.
        Parameter: nothing
        Return: nothing
        """

        for a_marble in self.marbles:
            a_marble.stamps = []

    def reset_board(self):
        """
        Method: reset_board
            Reset the Board, including: reset is_end attribute,
            reset the status_area and the leaderboard area.
        Parameter: nothing
        Return: nothing
        """

        self.is_end = False

        # reset the status_area on Board
        self.erase_all_stamps()
        self.status_area.initialize_pegs()
        self.buttons["row_marker"].update()

        # reset the leaderboard area
        self.leaderboard.write_leaders()

    def show_end_message(self):
        """
        Method: show_end_message
            Show the end message on Board when game ends.
        Parameter: nothing
        Return: nothing
        """

        if not self.is_end:
            if self.controller.game_status == "win":
                self.is_end = True
                self.pop_message("winner.gif")

            elif self.controller.game_status == "lost":
                self.is_end = True
                self.pop_message("lose.gif")

    def operate_board_objects(self):
        """
        Method: operate_board_objects
            Bind all event methods to the Board objects,
            including Marbles, cancel_button, check_button, restart_button, quit_button.
        Parameter: nothing
        Return: nothing
        """

        for each_marble in self.marbles:
            each_marble.ondrag(each_marble.goto, btn=3)
            each_marble.onrelease(each_marble.drag_guess, btn=3)
            each_marble.onclick(each_marble.click_guess)

        self.buttons["cancel_button"].onclick(
            self.buttons["cancel_button"].click_cancel)

        self.buttons["check_button"].onclick(
            self.buttons["check_button"].click_check)

        self.buttons["restart"].onclick(
            self.buttons["restart"].click_restart)

        self.buttons["quit"].onclick(
            self.buttons["quit"].click_quit)

    def __str__(self):
        """
        Method: __str__
            Return a string representation of Board instance.
        Parameter: nothing
        Return:
            A string representation
        """

        return self.name

    def __eq__(self, other):

        """
        Method: __eq__
            Compare current Board instance to another one.
        Parameter:
            other (Board) -- another instance of Board
        Return:
            A boolean representing whether the two instances are equal
        """

        return isinstance(other, Board) and self.controller is other.controller


class LeaderBoard(Board):
    """
    A class that represents the LeaderBoard area on the Mastermind Game Board,
    displaying the leaders records.
    Attributes: name, pen, written_pen, board
    Methods: __init__, draw_area, get_leaders_data, write_leaders, validate_writing,
             __str__, __eq__, and other methods from Board class
    """

    def __init__(self, board):
        """
        Method: __init__
            Create an instance of LeaderBoard.
        Parameter:
            board (Board) -- the Board instance to which the LeaderBoard belongs
        Return: nothing
        """

        if not isinstance(board, Board):
            raise TypeError("LeaderBoard constructor must have Board argument!")

        self.name = "Leader Board"
        self.pen = self.new_pen()
        self.written_pen = self.new_pen()
        self.board = board

    def draw_area(self, start = LEADERBOARD_START, sides = LEADERBOARD_SIDES):
        """
        Method: draw_area
            Draw a LeaderBoard area on the Board, based on given start position
            and sides length.
        Parameters:
            start (tuple) -- A tuple of 2 numbers(int or float), representing
                             the left-up point of the area
            sides (list) -- A list of 4 positive integers, representing the
                            up-side, right-side, down-side, left-side of the area
        Return: nothing
        """

        super().draw_area(start, sides)

    def get_leaders_data(self):
        """
        Method: get_leaders_data
            Retrieve the leaders data from leaderboard file.
        Parameter: nothing
        Return: nothing
        """

        try:
            leaderboard_data = self.board.controller.load_leaderboard_file()
        except IOError:
            self.board.pop_message("leaderboard_error.gif")
            leaderboard_data = []

        return leaderboard_data

    def write_leaders(self, written_start = WRITTEN_START,
                      written_line_space = WRITTEN_LINE_SPACE):
        """
        Method: write_leaders
            Write the leaders records on the LeaderBoard.
        Parameters:
            written_start (tuple) -- the tuple of two numbers(int or float),
                                    representing the starting position of writing
            written_line_space (int) -- the space between each writing line
        Return: nothing
        """

        self.validate_writing(written_start, written_line_space)

        self.written_pen.clear()
        self.written_pen.up()
        self.written_pen.pencolor("dark red")

        # write the leaderboard title
        self.written_pen.goto(written_start)
        self.written_pen.write("TOP LEADERS", False, "center",
                               font=("Comic Sans MS", 18, "bold"))

        # retrieve the leaderboard data
        # write the leader records
        leaderboard_data = self.get_leaders_data()
        for i in range(len(leaderboard_data)):
            written_x = written_start[0]
            written_y = written_start[1] - written_line_space * (i + 1)
            self.written_pen.goto(written_x, written_y)
            leaderboard_message = leaderboard_data[i][0] + ": " + \
                                  leaderboard_data[i][1]
            self.written_pen.write(leaderboard_message, False, "center",
                                   font=("Comic Sans MS", 14, "bold"))

    def validate_writing(self, written_start, written_line_space):
        """
        Method: validate_writing
            Check if the LeaderBoard writing arguments are valid.
        Parameters:
            written_start (tuple) -- the tuple of two numbers(int or float),
                                    representing the starting position of writing
            written_line_space (int) -- the space between each writing line
        Return: nothing
        """

        # check the writing arguments types
        if not (isinstance(written_start, tuple) and
                isinstance(written_line_space, int)):
            raise TypeError("Written_start argument must be tuple, " +
                            "written_line_space argument must be int!")

        # check if the written_line_space is positive
        elif written_line_space <= 0:
            raise ValueError("Written_line_space must be positive!")

        # check if the written_start is a tuple of two numbers
        else:
            validate_position(written_start)

    def __str__(self):
        """
        Method: __str__
            Return a string representation of LeaderBoard instance.
        Parameter: nothing
        Return:
            A string representation
        """

        return self.name

    def __eq__(self, other):

        """
        Method: __eq__
            Compare current LeaderBoard instance to another one.
        Parameter:
            other (LeaderBoard) -- another instance of LeaderBoard
        Return:
            A boolean representing whether the two instances are equal
        """

        return isinstance(other, LeaderBoard) and self.board is other.board


class BoardStatusArea(Board):
    """
    A class that represents the status area of the Mastermind Game Board,
    displaying pits and pegs.
    Attributes: name, pen, peg_pen, board, pits_position, pegs_position
    Methods: 
    """

    def __init__(self, board):
        """
        Method: __init__
            Create an instance of BoardStatusArea.
        Parameter:
            board (Board) -- the Board instance to which the BoardStatusArea belongs
        Return: nothing
        """

        if not isinstance(board, Board):
            raise TypeError("BoardStatusArea constructor must have Board argument!")

        self.name = "Board Status Area"
        self.pen = self.new_pen()
        self.peg_pen = self.new_pen()
        self.board = board

        self.pits_position = []  # nested list, contains all pits positions
        self.pegs_position = []  # contains the first peg's position in each row

    def draw_area(self, start = STATUS_AREA_START, sides = STATUS_AREA_SIDES):
        """
        Method: draw_area
            Draw a BoardStatusArea on the Board, based on given start position
            and sides length.
        Parameters:
            start (tuple) -- A tuple of 2 numbers(int or float), representing
                             the left-up point of the area
            sides (list) -- A list of 4 positive integers, representing the
                            up-side, right-side, down-side, left-side of the area
        Return: nothing
        """

        super().draw_area(start, sides)

    def locate_pits_and_pegs(self, pit_start = PIT_START, pit_row_space = ROW_SPACE,
                             pit_column_space = COLUMN_SPACE,
                             pit_to_peg_x = PIT_TO_PEG_X,
                             pit_to_peg_y = PIT_TO_PEG_Y):
        """
        Method: locate_pits_and_pegs
            Generate the positions of all pits and pegs on the Board.
        Parameters:
            pit_start (tuple) -- a tuple of two numbers (int or float),
                                 representing the position of first pit on Board
            pit_row_space (int) -- the space between each pit-row
            pit_column_space (int) -- the space between each pit-column
            pit_to_peg_x (int) -- the x-difference between the last pit and the first
                                  peg in the same row
            pit_to_peg_y (int) -- the y-difference between the last pit and the first
                                  peg in the same row
        Return: nothing
        """

        self.validate_pits_and_pegs_positions(pit_start,
                                              pit_row_space, pit_column_space,
                                              pit_to_peg_x, pit_to_peg_y)

        for row in range(self.board.row_num):

            # locate all pits positions in one row
            pit_row = []
            for column in range(self.board.column_num):
                pit_x = pit_start[0] + column * pit_column_space
                pit_y = pit_start[1] - row * pit_row_space
                pit_row.append(Point(pit_x, pit_y))
            self.pits_position.append(pit_row)

            # locate the first peg's position in one row
            peg_x = pit_row[-1].x + pit_to_peg_x
            peg_y = pit_row[-1].y + pit_to_peg_y
            self.pegs_position.append(Point(peg_x, peg_y))

    def validate_pits_and_pegs_positions(self, pit_start,
                                         pit_row_space, pit_column_space,
                                         pit_to_peg_x, pit_to_peg_y):
        """
        Method: validate_pits_and_pegs_positions
            Check if the pits and pegs position arguments are valid.
        Parameters:
            pit_start (tuple) -- a tuple of two numbers (int or float),
                                 representing the position of first pit on Board
            pit_row_space (int) -- the space between each pit-row
            pit_column_space (int) -- the space between each pit-column
            pit_to_peg_x (int) -- the x-difference between the last pit and the first
                                  peg in the same row
            pit_to_peg_y (int) -- the y-difference between the last pit and the first
                                  peg in the same row
        Return: nothing
        """

        # check all arguments' types
        if not (isinstance(pit_start, tuple) and isinstance(pit_row_space, int) and
                isinstance(pit_column_space, int) and isinstance(pit_to_peg_x, int)
                and isinstance(pit_to_peg_y, int)):
            raise TypeError("Invalid argument types: " +
                            "Pit_start must be tuple; " +
                            "pit_row_space, pit_column_space, pit_to_peg_x, and " +
                            "pit_to_peg_y must be integers!")

        # check if all other arguments are positive
        elif not (pit_row_space > 0 and pit_column_space > 0 and pit_to_peg_x > 0
                  and pit_to_peg_y > 0):
            raise ValueError("Pit space arguments must be positive!")

        # check if the pit_start is a tuple of two numbers
        else:
            validate_position(pit_start)

    def initialize_pits(self):
        """
        Method: initialize_pits
            Initialize all pits on the status-area of the Board.
        Parameter: nothing
        Return: nothing
        """

        self.pen.up()
        self.pen.shape("circle")
        self.pen.color("peru")
        self.pen.shapesize(1.8)

        for row in range(self.board.row_num):
            for a_pit in self.pits_position[row]:
                self.pen.goto(a_pit.x, a_pit.y)
                self.pen.stamp()

    def initialize_pegs(self):
        """
        Method: initialize_pegs
            Initialize all pegs on the status-area of the Board.
        Parameter: nothing
        Return: nothing
        """

        self.peg_pen.clearstamps()
        self.peg_pen.up()
        self.peg_pen.shape("circle")
        self.peg_pen.shapesize(0.5)

        for row in range(self.board.row_num):
            self.draw_pegs(row)

    def draw_pegs(self, row, peg_space = PEG_SPACE):
        """
        Method: draw_pegs
            Draw all pegs in a given row on the Board .
        Parameters: 
            row (int) -- the index of current row
            peg_space (int) -- the space between each two pegs
        Return: nothing
        """

        # check if the arguments are valid
        if not (isinstance(peg_space, int) and isinstance(row, int)):
            raise TypeError("Peg drawing arguments must be integer!")
        elif peg_space <= 0:
            raise ValueError("Peg space must be positive!")
        elif row not in range(self.board.row_num):
            raise IndexError("Peg row is out of the row range on Board!")

        if not self.board.is_end:
            # go to the first peg position in the given row        
            self.peg_pen.goto(self.pegs_position[row].x, self.pegs_position[row].y)

            # draw all pegs in the given row
            # peg position in one row corresponds to vertices of the polygon
            # peg_num = vertex_num = board_column = length of code
            for a_color in self.get_peg_colors():
                self.peg_pen.color(a_color)
                self.peg_pen.stamp()
                # peg space = side length of the polygon
                self.peg_pen.forward(peg_space)
                # turn angle = internal angle of the polygon
                self.peg_pen.right(360 / self.board.column_num)

    def get_peg_colors(self):
        """
        Method: get_peg_colors
            Get the peg colors generated from the last round.
        Parameter: nothing
        Return: nothing
        """

        bull_num, cow_num = self.board.controller.get_bulls_and_cows()
        # black-pegs = bull_num
        # red-pegs = cow_num 
        # white-pegs = code length - bull_num - cow_num
        peg_colors = ["black"] * bull_num + ["firebrick"] * cow_num + \
                     ["white"] * (self.board.column_num - bull_num - cow_num)

        return peg_colors

    def get_current_pits_row(self):
        """
        Method: get_current_pits_row
            Get the positions of pits row in the current round.
        Parameter: nothing
        Return: nothing
        """

        try:
            return self.pits_position[self.board.controller.current_round - 1]
        except IndexError:
            return []

    def __str__(self):
        """
        Method: __str__
            Return a string representation of BoardStatusArea instance.
        Parameter: nothing
        Return:
            A string representation
        """

        return self.name

    def __eq__(self, other):
        """
        Method: __eq__
            Compare current BoardStatusArea instance to another one.
        Parameter:
            other (BoardStatusArea) -- another instance of BoardStatusArea
        Return:
            A boolean representing whether the two instances are equal
        """

        return isinstance(other, BoardStatusArea) and self.board is other.board
