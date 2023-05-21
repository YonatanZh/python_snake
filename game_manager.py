##########################################################################################
# FILE : game_manager.py
# WRITER : Yonatan Zhenin , Yonatanzh , 208623397, Yahel Uffenheimer, yahelo, 318377751
# EXERCISE : intro2cs1 ex10 2021
# DESCRIPTION: The game manager for the the game.
##########################################################################################
from typing import List, Tuple, Optional, Dict, Literal, Set

from game_parameters import WIDTH, HEIGHT
from snake import Snake
from apple import Apple
from bomb import Bomb

INITIAL_POSITION = (10, 8)
INITIAL_LENGTH = 3
GROWTH_LENGTH = 3
INITIAL_DIRECTION: Literal['Up'] = "Up"
NUMBER_OF_APPLES = 3
MINIMUM_LENGTH = 4

Colour = Literal['black', 'green', 'red', 'orange']


def is_in_bounds(position: Tuple[int, int]) -> bool:
    """
    Checks if position is in the board bounds.
    :param position: Position to be checked.
    :return: True if the position is in bounds False other-wise.
    """
    if 0 <= position[0] < WIDTH and 0 <= position[1] < HEIGHT:
        return True
    return False


class GameManager:
    """
    A class that's responsible for the games rules.
    """
    def __init__(self):
        """
        Constructor for the Class
        """
        self.__snake = Snake(INITIAL_POSITION, INITIAL_DIRECTION, INITIAL_LENGTH)
        self.__bomb: Optional[Bomb] = None
        self.__apples: List[Apple] = []
        self.__score: int = 0
        self.__snake_positions: List[Tuple[int, int]] = []
        self.__bomb_positions: List[Tuple[int, int]] = []
        self.__apple_positions: List[Tuple[int, int]] = []
        self.__update_snake_positions()
        self.__check_bomb()
        self.__check_num_of_apples()

    def __is_placement_empty(self, position: Tuple[int, int]) -> bool:
        """
        Checks if given position is already Occupied by anything else on the board.
        :param position: Position to be checked.
        :return: True if the position is empty, False if not.
        """
        if position in self.__bomb_positions or position in self.__snake_positions or position in self.__apple_positions:
            return False
        return True

    def __update_apple_positions(self) -> None:
        """
        Updates the lists that keeps track of where all the apples are on the board.
        :return: None.
        """
        self.__apple_positions = [apple.apple_position() for apple in self.__apples]

    def __check_num_of_apples(self) -> None:
        """
        Checks how many apples are on the board. If the current amount of apples is lower than NUMBER_OF_APPLES, creates
        a new apple and adds it to the board.
        :return: None.
        """
        for apple in self.__apples:
            if apple.apple_position() in self.__bomb_positions:
                self.__apples.remove(apple)

        while NUMBER_OF_APPLES > len(self.__apples):
            new_apple = Apple()
            if self.__is_placement_empty(new_apple.apple_position()):
                self.__apples.append(new_apple)
                self.__update_apple_positions()

    def __update_bomb_positions(self) -> None:
        """
        Updates the lists that keeps track of where the bomb is on the board.
        :return: None.
        """
        self.__bomb_positions = self.__bomb.bomb_positions()

    def __check_bomb(self) -> None:
        """
        Checks if there's a bomb on the board. If there is no bomb on the board creates one.
        If the current Bomb shock wave reaches the edges of the board, gets rid of the bomb and creates a new one.
        :return: None.
        """
        if self.__bomb and not self.__bomb.finished_exploding:
            in_bounds = all(is_in_bounds(location) for location in self.__bomb_positions)
            if not in_bounds:
                self.__bomb = None

        while self.__bomb is None or self.__bomb.finished_exploding:
            new_bomb = Bomb()
            base_location = new_bomb.bomb_positions()[0]
            if self.__is_placement_empty(base_location):
                self.__bomb = new_bomb
                self.__update_bomb_positions()

    def __update_snake_positions(self) -> None:
        """
        Updates the lists that keeps track of where the snake is on the board.
        :return: None.
        """
        self.__snake_positions = self.__snake.snake_positions()

    def __is_snake_alive(self) -> bool:
        """
        Checks if the snake is alive, i.e, did not go out of bounds, did not eat a bomb or touched the bomb's shock
        wave, did not eat one of his own ligaments.
        :return: True if the snake is alive, False other-wise
        """
        if not is_in_bounds(self.__snake.head):
            self.__snake_positions.remove(self.__snake.head)
            return False
        is_in_bomb_range = any(ligament in self.__bomb_positions for ligament in self.__snake_positions)
        if is_in_bomb_range:
            if not self.__bomb.exploding:
                self.__snake_positions.remove(self.__snake.head)
            return False
        has_ate_himself = len(set(self.__snake_positions)) != len(self.__snake_positions)
        if has_ate_himself:
            return False
        return True

    def __eat_apples(self) -> None:
        """
        Checks if the snake has eaten an apple, if so, enlarges the snake by GROWTH_LENGTH, and updates the number of
        apples on the board.
        :return: None.
        """
        for apple in self.__apples:
            if self.__snake.head == apple.apple_position():
                self.__snake.grow_by_x(GROWTH_LENGTH)
                self.__score += apple.score
                self.__apples.remove(apple)
                self.__check_num_of_apples()
                self.__update_apple_positions()
        return None

    def tick(self, direction: Optional[str]) -> bool:
        """
        Implements one tick(round) of the game.
        Checks if the snake needs to turn.
        Moves the snake one position in given direction.
        Updates the bombs life time.
        Updates all known positions on the board.
        Checks if the snake is alive.
        Checks if the snake has eaten an apple.
        Updates any missing objects on the board.
        :param direction: Desired direction of the snake.
        :return: True if the game can be played another round, False if not.
        """
        self.__snake.turn(direction)
        self.__snake.move()
        self.__update_snake_positions()
        self.__bomb.tick()
        self.__update_bomb_positions()
        if not self.__is_snake_alive():
            return False
        if not self.__space_left():
            return False
        self.__eat_apples()
        self.__check_bomb()
        self.__check_num_of_apples()
        return True

    def __space_left(self) -> bool:
        """
        Checks if there's any space left on the board.
        :return: False if the board is full i.e not enough place to place a bomb or an apple, True other-wise.
        """
        if len(self.__snake_positions) == (WIDTH * HEIGHT) - MINIMUM_LENGTH:
            return False
        return True

    def as_colours(self) -> Dict[Colour, List[Tuple[int, int]]]:
        """
        Uses all known positions to create a dictionary that is used to colour the board
        :return: Dictionary of colours as keys and positions as values.
        """
        return {
            'black': self.__snake_positions,
            'green': self.__apple_positions,
            'orange' if self.__bomb.exploding else 'red': self.__bomb_positions
        }

    @property
    def score(self) -> int:
        return self.__score
