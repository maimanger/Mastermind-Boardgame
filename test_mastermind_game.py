"""
    CS 5001
    Spring 2021
    Fangying Li
    Project: Mastermind Game -- Game Test
    Test classes and functions in Mastermind Game.
"""

from mastermind_game_model import GameModel
from mastermind_game_controller import Controller
from mastermind_game import count_bulls_and_cows
from mastermind_game_helper import Point, validate_position
import unittest
import random

guess = ["", "black", "", "red"]
guess2 = ["red", "black", "black", "blue"]

model = GameModel()

model2 = GameModel()
random.seed(0)
model2.create_code()

model3 = GameModel()
random.seed(1)
model3.create_code()

model4 = GameModel()
random.seed(0)
model4.create_code()


class GameModelTest(unittest.TestCase):
    """
    A TestCase class that test the methods in class GameModel.
    Methods: test_init, test_create_code, test_update, test_check_status,
    test_restart, test_str, test_eq
    """

    def test_init(self):

        self.assertEqual(model.name, "Mastermind Game")
        self.assertEqual(model.code, [])
        self.assertEqual(model.code_range, ["red", "blue", "green", "yellow",
                                            "purple", "black", ""])
        self.assertEqual(model.guess, [])
        self.assertEqual(model.score, 0)
        self.assertEqual(model.bull_num, 0)
        self.assertEqual(model.cow_num, 0)
        self.assertEqual(model.max_guess, 10)

    def test_bad_init(self):

        self.assertRaises(TypeError, GameModel, max_guess="a")
        self.assertRaises(ValueError, GameModel, max_guess=-10)
        self.assertRaises(TypeError, GameModel, code_range="a")
        self.assertRaises(ValueError, GameModel, code_range=[])

    def test_create_code(self):

        self.assertEqual(model2.code, ["black", "black", "green", "blue"])
        self.assertEqual(model3.code, ["red", "black", "black", "blue"])

        self.assertRaises(TypeError, model.create_code, "a")
        self.assertRaises(ValueError, model.create_code, -2)

    def test_update(self):

        model2.update(guess)
        self.assertEqual(model2.guess, ["", "black", "", "red"])
        self.assertEqual(model2.score, 1)
        self.assertEqual(model2.bull_num, 1)
        self.assertEqual(model2.cow_num, 0)

        model2.update(guess2)
        self.assertEqual(model2.guess, ["red", "black", "black", "blue"])
        self.assertEqual(model2.score, 2)
        self.assertEqual(model2.bull_num, 2)
        self.assertEqual(model2.cow_num, 1)

        self.assertRaises(TypeError, model.update, "a")
        self.assertRaises(ValueError, model2.update, ["red"])

    def test_check_status(self):

        for i in range(9):
            model3.update(guess)
        self.assertEqual(model3.check_status(), "running")

        model3.update(guess2)
        self.assertEqual(model3.check_status(), "win")

        for i in range(10):
            model4.update(guess)
        self.assertEqual(model4.check_status(), "lost")

    def test_restart(self):

        random.seed(0)
        model3.restart()
        self.assertEqual(model3.code, ["black", "black", "green", "blue"])
        self.assertEqual(model3.guess, [])
        self.assertEqual(model3.score, 0)
        self.assertEqual(model3.bull_num, 0)
        self.assertEqual(model3.cow_num, 0)

    def test_str(self):

        msg = "Mastermind Game\tCode: ['black', 'black', 'green', 'blue']\tScore: 10"
        self.assertEqual(model4.__str__(), msg)

    def test_eq(self):

        model5 = GameModel()
        random.seed(2)
        model5.create_code()
        model5.update(guess)

        model6 = GameModel()
        random.seed(2)
        model6.create_code()
        model6.update(guess)
        self.assertTrue(model5.__eq__(model6))

        self.assertFalse(model2.__eq__(model3))
        self.assertFalse(model2.__eq__("a"))


class ControllerTest(unittest.TestCase):
    """
    A TestCase class that test the methods in class Controller.
    Methods: test_init, test_bad_init, test_add_model, test_reset_guess,
             test_add_guess, test_validate_filename, test_load_leaderboard_file,
             test_save_leaderboard_file, test_create_top_leaders_list, 
             test_update_round, test_get_bulls_and_cows,
             test_get_current_guess_index, test_restart, test_str, test_eq
    """

    def test_init(self):
        controller = Controller()

        self.assertEqual(controller.name, "MasterMind Game Controller")
        self.assertEqual(controller.player, "")
        self.assertEqual(controller.model, None)
        self.assertEqual(controller.current_guess, [])
        self.assertEqual(controller.current_round, 1)
        self.assertEqual(controller.game_status, "running")

        model = GameModel()
        controller2 = Controller(model, "abc")

        self.assertEqual(controller2.name, "MasterMind Game Controller")
        self.assertEqual(controller2.player, "abc")
        self.assertEqual(controller2.model, model)
        self.assertEqual(controller2.current_guess, [])
        self.assertEqual(controller2.current_round, 1)
        self.assertEqual(controller2.game_status, "running")

    def test_bad_init(self):
        self.assertRaises(TypeError, Controller, 10, "abc")
        self.assertRaises(TypeError, Controller, model, 50)

    def test_add_model(self):
        model = GameModel()
        controller = Controller()
        controller.add_model(model)

        self.assertEqual(controller.model, model)
        # test bad argument
        self.assertRaises(TypeError, controller.add_model, "a")

    def test_reset_guess(self):
        controller = Controller()
        controller.reset_guess()

        self.assertEqual(controller.current_guess, [])

        model = GameModel()
        model.code = ["black", "black", "green", "blue"]
        controller.add_model(model)
        controller.reset_guess()

        self.assertEqual(controller.current_guess, ["", "", "", ""])

    def test_add_guess(self):
        model = GameModel()
        model.code = ["black", "black", "green", "blue"]
        controller = Controller(model, "abc")
        controller.reset_guess()

        controller.add_guess("black", 0)
        self.assertEqual(controller.current_guess, ["black", "", "", ""])

        controller.add_guess("blue", 3)
        self.assertEqual(controller.current_guess, ["black", "", "", "blue"])

        # test bad argument
        self.assertRaises(TypeError, controller.add_guess, 50, 1)
        self.assertRaises(TypeError, controller.add_guess, "green", "a")
        self.assertRaises(IndexError, controller.add_guess, "green", 4)
        self.assertRaises(ValueError, controller.add_guess, "hello", 1)

    def test_validate_filename(self):
        controller = Controller()
        self.assertRaises(TypeError, controller.validate_filename, 123)

    def test_load_leaderboard_file(self):
        # delete the file "test_leaderboard.txt" in the folder for testing

        controller = Controller()
        data = controller.load_leaderboard_file(filename = "test_leaderboard.txt")
        self.assertEqual(data, [])

        # test bad argument
        self.assertRaises(TypeError, controller.load_leaderboard_file, filename = 123)

    def test_save_leaderboard_file(self):
        # delete the file "test_leaderboard1.txt" in the folder for testing

        model = GameModel()
        model.score = 10
        controller = Controller(model, "def")
        controller.game_status = "win"
        starting_data = [["aaa", "10"], ["bbb", "5"], ["ccc", "1"],
                         ["ddd", "3"], ["eee", "7"]]

        controller.save_leaderboard_file(starting_data,
                                         filename = "test_leaderboard1.txt")
        saved_data = controller.load_leaderboard_file(filename = "test_leaderboard1.txt")
        self.assertEqual(saved_data, starting_data)

        # test bad argument
        self.assertRaises(TypeError, controller.save_leaderboard_file, "a",
                          filename = "test_leaderboard1.txt")
        self.assertRaises(TypeError, controller.save_leaderboard_file, [],
                          filename = 123)
        self.assertRaises(TypeError, controller.save_leaderboard_file,
                          [[1, 2], [3, 4]], filename = "test_leaderboard1.txt")
        

    def test_create_top_leaders_list(self):
        model = GameModel()
        model.score = 2
        controller = Controller(model, "abc")
        starting_data = [["aaa", "10"], ["bbb", "5"], ["ccc", "1"],
                         ["ddd", "3"], ["eee", "7"]]

        leaders_list = controller.create_top_leaders_list(starting_data)
        expected = [["ccc", "1"], ["abc", "2"], ["ddd", "3"], ["bbb", "5"],
                    ["eee", "7"]]
        self.assertEqual(leaders_list, expected)

        model.score = 10
        leaders_list2 = controller.create_top_leaders_list(starting_data)
        expected2 = [["ccc", "1"], ["ddd", "3"], ["bbb", "5"], ["eee", "7"],
                     ["abc", "10"]]
        self.assertEqual(leaders_list2, expected2)

        # test bad argument
        self.assertRaises(TypeError, controller.create_top_leaders_list, 456)
        self.assertRaises(TypeError, controller.create_top_leaders_list,
                          [[1, 2], [3, 4]])

    def test_update_round(self):
        # delete the files "test_leaderboard1.txt", "test_leaderboard2.txt"
        # "test_leaderboard3.txt", "test_leaderboard4.txt" in the folder for testing

        # 1. First update test of controller
        model = GameModel()
        model.code = ["black", "black", "green", "blue"]
        controller = Controller(model, "abc")
        controller.current_guess = ["black", "", "", "blue"]
        controller.update_round(infile_name = "test_leaderboard1.txt",
                                outfile_name = "test_leaderboard2.txt")

        self.assertEqual(model.guess, ["black", "", "", "blue"])
        self.assertEqual(model.score, 1)
        self.assertEqual(model.bull_num, 2)
        self.assertEqual(model.cow_num, 0)
        self.assertEqual(controller.game_status, "running")
        self.assertEqual(controller.current_guess, ["", "", "", ""])
        self.assertEqual(controller.current_round, 2)
        # test whether the file is successfully saved
        data1 = controller.load_leaderboard_file(filename="test_leaderboard2.txt")
        self.assertEqual(data1, [])

        # 2. Second update test of controller
        controller.current_guess = ["black", "black", "green", "blue"]
        controller.update_round(infile_name = "test_leaderboard1.txt",
                                outfile_name = "test_leaderboard3.txt")

        self.assertEqual(model.guess, ["black", "black", "green", "blue"])
        self.assertEqual(model.score, 2)
        self.assertEqual(model.bull_num, 4)
        self.assertEqual(model.cow_num, 0)
        self.assertEqual(controller.game_status, "win")
        self.assertEqual(controller.current_guess, ["", "", "", ""])
        self.assertEqual(controller.current_round, 3)
        # test whether the file is successfully saved
        data2 = controller.load_leaderboard_file(filename = "test_leaderboard3.txt")
        expected = [["ccc", "1"], ["abc", "2"], ["ddd", "3"], ["bbb", "5"],
                    ["eee", "7"]]
        self.assertEqual(data2, expected)

        # 3. Update test of controller2
        model2 = GameModel()
        model2.code = ["black", "black", "green", "blue"]
        model2.score = 9
        controller2 = Controller(model2, "def")
        controller2.current_guess = ["", "blue", "black", ""]
        controller2.update_round(infile_name = "test_leaderboard1.txt",
                                 outfile_name = "test_leaderboard4.txt")

        self.assertEqual(model2.guess, ["", "blue", "black", ""])
        self.assertEqual(model2.score, 10)
        self.assertEqual(model2.bull_num, 0)
        self.assertEqual(model2.cow_num, 2)
        self.assertEqual(controller2.game_status, "lost")
        self.assertEqual(controller2.current_guess, ["", "", "", ""])
        self.assertEqual(controller2.current_round, 2)
        # test whether the file is successfully saved
        data3 = controller2.load_leaderboard_file(filename = "test_leaderboard4.txt")
        self.assertEqual(data3, [])

        # 4. test bad argument
        self.assertRaises(TypeError, controller2.update_round, in_filename=123,
                          out_filename = "test_leaderboard4.txt")
        self.assertRaises(TypeError, controller2.update_round,
                          in_filename = "test_leaderboard1.txt", out_filename=123)

    def test_get_bulls_and_cows(self):
        model = GameModel()
        model.bull_num = 1
        model.cow_num = 2
        controller = Controller(model, "abc")
        self.assertEqual(controller.get_bulls_and_cows(), (1, 2))

    def test_get_current_guess_index(self):
        controller = Controller()

        controller.current_guess = []
        self.assertEqual(controller.get_current_guess_index(), -1)

        controller.current_guess = ["", "", "", ""]
        self.assertEqual(controller.get_current_guess_index(), -1)

        controller.current_guess = ["red", "", "", ""]
        self.assertEqual(controller.get_current_guess_index(), 0)

        controller.current_guess = ["red", "", "", "red"]
        self.assertEqual(controller.get_current_guess_index(), 3)

        controller.current_guess = ["", "red", "red", ""]
        self.assertEqual(controller.get_current_guess_index(), 2)

    def test_restart(self):
        # after update, model.score = 10
        # model.guess = ["black", "", "", "blue"]
        # model.bull_num = 1, model.cow_num = 1
        # controller.game_status = "lost"
        model = GameModel()
        random.seed(0)
        model.create_code()
        model.score = 9
        model.update(["black", "", "blue", ""])
        controller = Controller(model, "abc")
        controller.current_round = 10
        controller.game_status = model.check_status()

        random.seed(0)
        controller.restart()

        self.assertEqual(controller.current_round, 1)
        self.assertEqual(controller.game_status, "running")
        self.assertEqual(model.code, ["black", "black", "green", "blue"])
        self.assertEqual(model.guess, [])
        self.assertEqual(model.score, 0)
        self.assertEqual(model.bull_num, 0)
        self.assertEqual(model.cow_num, 0)

    def test_str(self):
        controller = Controller(GameModel(), "abc")
        msg = "MasterMind Game Controller\tPlayer: abc\tGame status: running"

        self.assertEqual(controller.__str__(), msg)

        controller2 = Controller()
        controller2.game_status = "lost"
        msg2 = "MasterMind Game Controller\tPlayer: \tGame status: lost"

        self.assertEqual(controller2.__str__(), msg2)

    def test_eq(self):
        model = GameModel()
        model2 = GameModel()
        controller = Controller(model, "abc")
        controller2 = Controller(model, "abc")
        controller3 = Controller(model2, "abc")
        controller4 = Controller(model, "def")

        self.assertTrue(controller.__eq__(controller2))
        self.assertFalse(controller.__eq__("a"))
        self.assertFalse(controller == controller3)
        self.assertFalse(controller == controller4)


class PointTest(unittest.TestCase):
    """
    A TestCase class that test the methods in class Point.
    Methods: test_init, test_get_distance, test_str, test_eq
    """

    def test_init(self):
        point = Point()
        point2 = Point(1, 2)
        point3 = Point(0.5, 3.5)
        point4 = Point(-10, 0.5)

        self.assertEqual(point.x, 0)
        self.assertEqual(point.y, 0)
        self.assertEqual(point2.x, 1)
        self.assertEqual(point2.y, 2)
        self.assertEqual(point3.x, 0.5)
        self.assertEqual(point3.y, 3.5)
        self.assertEqual(point4.x, -10)
        self.assertEqual(point4.y, 0.5)

        self.assertRaises(TypeError, Point, "a", 1)
        self.assertRaises(TypeError, Point, 1, [])

    def test_get_distance(self):
        point = Point()
        point2 = Point(1, 2)
        point3 = Point(0.5, 3.5)
        point4 = Point(-10, 0.5)

        self.assertAlmostEqual(point.get_distance(point2), 2.23606798)
        self.assertAlmostEqual(point2.get_distance(point3), 1.58113883)
        self.assertAlmostEqual(point.get_distance(point4), 10.01249220)

    def test_str(self):
        point = Point()
        point4 = Point(-10, 0.5)

        self.assertEqual(point.__str__(), "(0, 0)")
        self.assertEqual(point4.__str__(), "(-10, 0.5)")

    def test_eq(self):
        point2 = Point(1, 2)
        point3 = Point(0.5, 3.5)
        point4 = Point(0.50, 3.50)

        self.assertFalse(point2.__eq__(point3))
        self.assertTrue(point3 == point4)


class FunctionTest(unittest.TestCase):
    """
    A TestCase class that test the function count_bulls_and_cows,
    validate_position. 
    """

    def test_count_bulls_and_cows(self):
        code1 = ["red", "red", "red", "red"]
        code2 = ["", "", "", ""]
        code3 = ["blue", "green", "yellow", "purple"]
        code4 = ["black", "black", "", "blue"]
        code5 = ["black", "blue", "yellow", ""]
        guess1 = ["blue", "green", "yellow", "purple"]
        guess2 = ["red", "", "", ""]
        guess3 = ["red", "black", "black", ""]
        guess4 = ["", "blue", "black", "black"]
        guess5 = ["blue", "blue", "red", "red"]
        guess6 = ["blue", "blue", "red", "red"]

        self.assertEqual(count_bulls_and_cows(code1, guess2), (1, 0))
        self.assertEqual(count_bulls_and_cows(code2, guess1), (0, 0))
        self.assertEqual(count_bulls_and_cows(code3, guess1), (4, 0))
        self.assertEqual(count_bulls_and_cows(code4, guess3), (1, 2))
        self.assertEqual(count_bulls_and_cows(code4, guess4), (0, 4))
        self.assertEqual(count_bulls_and_cows(code3, guess5), (1, 0))
        self.assertEqual(count_bulls_and_cows(code5, guess6), (1, 0))
        self.assertEqual(count_bulls_and_cows([], []), (0, 0))

        self.assertRaises(TypeError, count_bulls_and_cows, 1, "a")
        self.assertRaises(ValueError, count_bulls_and_cows, [], ["red"])

    def test_validate_position(self):
        position1 = (0, 0)
        position2 = (1.5, 2.5)
        position3 = (-5, 0.5)
        position4 = ("a", 1)
        position5 = (1, 2, 3)

        self.assertTrue(validate_position(position1))
        self.assertTrue(validate_position(position2))
        self.assertTrue(validate_position(position3))

        self.assertRaises(ValueError, validate_position, position4)
        self.assertRaises(ValueError, validate_position, position5)


def main():
    unittest.main(verbosity=3)


if __name__ == "__main__":
    main()
