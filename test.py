import random
from unittest import TestCase, mock

import snake_main
from bomb import Bomb
from game_parameters import get_random_bomb_data, get_random_apple_data


def mock_random_bomb_data(seed):
    def wrapped():
        random.seed(seed)
        return get_random_bomb_data()
    return wrapped


def mock_random_apple_data(seed):
    d = 0
    c = [2, 3, 4]
    def wrapped():
        nonlocal d
        if d == 3:
            d = 0
        random.seed(c[d])
        d += 1
        return get_random_apple_data()
    return wrapped


class Test(TestCase):
    def setUp(self) -> None:
        self.counter = 0
        self.cells = []

    def mock_key_input(self, input_list):
        self.counter = 0
        def wrapped(s):
            nonlocal self, input_list
            if self.counter >= len(input_list):
                self.counter += 1
                return None
            v = input_list[self.counter]
            self.counter += 1
            return v
        return wrapped

    def mock_draw_cell(self):
        self.cells = []

        def wrapped(s, x, y, color):
            nonlocal self
            if self.counter == len(self.cells):
                self.cells.append({(x, y): color})
            else:
                self.cells[self.counter][(x, y)] = color
        return wrapped

    def test_bomb_manhattan(self):
        with mock.patch('bomb.get_random_bomb_data', lambda: (2, 2, 2, 2)):
            bomb = Bomb()
        self.assertEqual([(2, 2)], bomb.bomb_positions())
        bomb.tick()
        self.assertEqual([(2, 2)], bomb.bomb_positions())
        bomb.tick()
        self.assertEqual([(2, 2)], bomb.bomb_positions())
        bomb.tick()
        self.assertEqual([(1, 2), (2, 3), (3, 2), (2, 1)], bomb.bomb_positions())
        bomb.tick()
        self.assertEqual({(0, 2), (1, 1), (2, 0), (3, 1), (4, 2), (3, 3), (2, 4), (1, 3)}, set(bomb.bomb_positions()))

    @mock.patch('bomb.get_random_bomb_data', mock_random_bomb_data(567))
    @mock.patch('apple.get_random_apple_data', mock_random_apple_data(30))
    def test_full_game(self):
        class GameMock(mock.Mock):
            draw_cell = self.mock_draw_cell()
        gd = GameMock()

        with mock.patch('snake_main.get_key', self.mock_key_input(
                [None, None, None, None, None, None, None, None, None, 'Left', None, None, 'Down'])):
            snake_main.main_loop(gd)

        result = []
        for c in self.cells:
            result.append(" ".join([
                'Black::', str([k for k, v in c.items() if v == 'black']),
                '|Red::', str([k for k, v in c.items() if v == 'red']),
                '|Orange::', str([k for k, v in c.items() if v == 'orange'])]))
        self.assertEqual("""Black:: [(10, 8), (10, 9), (10, 10)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 9), (10, 10), (10, 11)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 10), (10, 11), (10, 12)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 11), (10, 12), (10, 13)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 12), (10, 13), (10, 14)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 13), (10, 14), (10, 15)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 14), (10, 15), (10, 16)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 15), (10, 16), (10, 17)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 16), (10, 17), (10, 18)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 17), (10, 18), (10, 19)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 18), (10, 19), (9, 19)] |Red:: [(9, 10)] |Orange:: []
Black:: [(10, 19), (9, 19), (8, 19)] |Red:: [(9, 10)] |Orange:: []
Black:: [(9, 19), (8, 19), (7, 19)] |Red:: [(9, 10)] |Orange:: []
Black:: [(8, 19), (7, 19), (7, 18)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 19), (7, 18), (7, 17)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 18), (7, 17), (7, 16)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 17), (7, 16), (7, 15)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 16), (7, 15), (7, 14)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 15), (7, 14), (7, 13)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 14), (7, 13), (7, 12)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 13), (7, 12), (7, 11)] |Red:: [(9, 10)] |Orange:: []
Black:: [(7, 12), (7, 11), (7, 10)] |Red:: [] |Orange:: [(9, 10)]
Black:: [(7, 11), (7, 10), (7, 9)] |Red:: [] |Orange:: [(8, 10), (9, 11), (10, 10), (9, 9)]
Black:: [(7, 9), (7, 8)] |Red:: [] |Orange:: [(7, 10), (9, 12), (11, 10), (9, 8), (8, 11), (10, 11), (10, 9), (8, 9)]""",
                         "\n".join(result))

    def test_ex(self):
        a = [(0, {(10, 8): 'black', (10, 9): 'black', (10, 10): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(10, 9): 'black', (10, 10): 'black', (10, 11): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(10, 10): 'black', (10, 11): 'black', (10, 12): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(10, 11): 'black', (10, 12): 'black', (10, 13): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(10, 12): 'black', (10, 13): 'black', (11, 13): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(10, 13): 'black', (11, 13): 'black', (12, 13): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(11, 13): 'black', (12, 13): 'black', (12, 14): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(12, 13): 'black', (12, 14): 'black', (11, 14): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(12, 14): 'black', (11, 14): 'black', (10, 14): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(11, 14): 'black', (10, 14): 'black', (9, 14): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(10, 14): 'black', (9, 14): 'black', (8, 14): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 14): 'black', (8, 14): 'black', (8, 15): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(8, 14): 'black', (8, 15): 'black', (9, 15): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(8, 15): 'black', (9, 15): 'black', (9, 14): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 15): 'black', (9, 14): 'black', (9, 13): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 14): 'black', (9, 13): 'black', (9, 12): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 13): 'black', (9, 12): 'black', (9, 11): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 12): 'black', (9, 11): 'black', (9, 10): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 11): 'black', (9, 10): 'black', (9, 9): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 10): 'black', (9, 9): 'black', (9, 8): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 9): 'black', (9, 8): 'black', (9, 7): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 8): 'black', (9, 7): 'black', (9, 6): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 7): 'black', (9, 6): 'black', (9, 5): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 6): 'black', (9, 5): 'black', (9, 4): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 5): 'black', (9, 4): 'black', (9, 3): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 4): 'black', (9, 3): 'black', (9, 2): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 3): 'black', (9, 2): 'black', (9, 1): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'red'}), (0, {(9, 2): 'black', (9, 1): 'black', (9, 0): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (28, 14): 'orange'}), (0, {(9, 1): 'black', (9, 0): 'black', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (27, 14): 'orange', (28, 15): 'orange', (29, 14): 'orange', (28, 13): 'orange'})]
        x = [(0, {(10, 10): 'black', (10, 9): 'black', (10, 8): 'black', (28, 14): 'red', (2, 19): 'green', (7, 10): 'green', (7, 2): 'green'}), (0, {(2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (9, 10): 'black', (10, 10): 'black', (10, 9): 'black', (28, 14): 'red'}), (0, {(2, 19): 'green', (7, 10): 'green', (7, 2): 'green', (8, 10): 'black', (9, 10): 'black', (10, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (7, 9): 'black', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (8, 9): 'black', (7, 9): 'black', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (9, 9): 'black', (8, 9): 'black', (7, 9): 'black', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (9, 10): 'black', (9, 9): 'black', (8, 9): 'black', (7, 9): 'black', (7, 10): 'black', (8, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (8, 10): 'black', (9, 10): 'black', (9, 9): 'black', (8, 9): 'black', (7, 9): 'black', (7, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (9, 9): 'black', (8, 9): 'black', (7, 9): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (6, 10): 'black', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (9, 9): 'black', (8, 9): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (5, 10): 'black', (6, 10): 'black', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (9, 9): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (5, 11): 'black', (5, 10): 'black', (6, 10): 'black', (7, 10): 'black', (8, 10): 'black', (9, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (6, 11): 'black', (5, 11): 'black', (5, 10): 'black', (6, 10): 'black', (7, 10): 'black', (8, 10): 'black', (28, 14): 'red'}), (4, {(2, 19): 'green', (7, 2): 'green', (29, 1): 'green', (6, 10): 'black', (6, 11): 'black', (5, 11): 'black', (5, 10): 'black', (7, 10): 'black', (28, 14): 'red'})]
        self.assertEqual(x, a[:15])
