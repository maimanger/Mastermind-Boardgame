README

Program Design
    This program uses the Objected Oriented Programming and the MVC architecture.
    It contains three main classes: GameModel, Controller, and Board.

    GameModel: the Model part implements all the game functionality following the
    Controller's directives.

    Controller: the Controller part takes user input from the Board;
    tells the Model what to do and the Controller what to display;
    communicates between the Board and the Model.

    Board: the View part comprises one superclass Board and several subclasses,
    such as Marble, LeaderBoard, Check, etc.
    The Board class is in charge of the user display and user interaction.

Extra Credits Function
    1. Duplicates and blanks are allowed in the code generation.
    The GameModel method create_code() randomly chooses multiple colors with
    replacement, allowing repetition in the code. Additionally, the sample
    colors for random choice contain an empty string, representing the blank code.

    2. Same colors and blanks are available in the user interaction.
    There are two methods combined with Marbles.
    The first one is click_guess. Users can click (left-click) the Marble object to
    make a color guess. Once clicked, the Marble would automatically fill the next
    empty pit to the last guessed position. Thus, all previous blank guesses can stay
    untouched.
    Another one is drag_guess. By dragging (right-click) the Marble object to an
    empty pit in the current row,  users can make a guess without any order.
    Because the Marble would fill any open space in the current row, users can drag
    the Marble elsewhere and remain blanks in the middle.
    Both methods allow using the same Marble to fill the pits.

    3. Replay allowable.
    The method click_restart of the Restart class allows users to replay the game
     using the same player's name without relaunching the game program.
