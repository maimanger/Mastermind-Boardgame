"""
    CS 5001
    Spring 2021
    Fangying Li
    Project: Mastermind Game -- Helper class and function
    Create Point class for Mastermind Game.
"""


class Point:
    """
    A class that records and calculate the position of points.
    Attributes: x (int or float), y (int or float)
    Methods: __init__, get_distance, __str__, __eq__
    """

    def __init__(self, x = 0, y = 0):
        """
        Method: __init__
            Create an instance of Point.
        Parameters:
            x (int or float) -- the x coordinate of the point
            y (int or float) -- the y coordinate of the point
        Return: nothing
        """

        if not (isinstance(x, float) or isinstance(x, int)) or \
                not (isinstance(y, float) or isinstance(y, int)):
            raise TypeError("Arguments must be int or float!")

        self.x = x
        self.y = y

    def get_distance(self, other):
        """
        Method: get_distance
            Calculate the distance between two points.
        Parameter:
            other (Point) -- another instance of Point
        Return:
            A float representing the distance between two points
        """

        if not isinstance(other, Point):
            raise TypeError("Argument must be of Point class!")

        delta_x = (self.x - other.x)
        delta_y = (self.y - other.y)
        return (delta_x ** 2 + delta_y ** 2) ** (1 / 2)

    def __str__(self):
        """
        Method: __str__
            Return a string representation of Point instance.
        Parameter: nothing
        Return:
            A string representation
        """

        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        """
        Method: __eq__
            Compare current Point instance to another one.
        Parameter:
            other (Point) -- another instance of Point
        Return:
            A boolean representing whether the two instances are equal
        """

        return isinstance(other, Point) and self.x == other.x and self.y == self.y


def validate_position(position):
    """
    Function: validate_position
        A validating function to check if the given position tuple is valid.
    Parameter:
        position (tuple) -- a tuple of two numbers (int or float), representing
                            the position coordinate
    Return: nothing
    """

    if len(position) != 2 \
            or not (isinstance(position[0], int) or
                    isinstance(position[0], float)) \
            or not (isinstance(position[1], int) or
                    isinstance(position[1], float)):
        raise ValueError("Position argument must be " +
                         "a 2-tuple of ints or floats!")
    else:
        return True
