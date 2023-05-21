##########################################################################################
# FILE : snake.py
# WRITER : Yonatan Zhenin , Yonatanzh , 208623397, Yahel Uffenheimer, yahelo, 318377751
# EXERCISE : intro2cs1 ex10 2021
# DESCRIPTION: Ligament and Snake class for the ex10 game.
##########################################################################################
from typing import Tuple, Literal, Dict, Callable, Optional, List

Direction = Literal['Up', 'Down', 'Left', 'Right']


class Ligament:
    """
    Linked list nodes, to be used by the Snake class.
    """

    def __init__(self, position: Tuple[int, int], next_node: Optional = None):
        """
        A constructor for a Ligament object.
        :param position: The position of the ligament, represented by a Tuple with an x,y coordinates.
        :param next_node: The next ligament referenced. If The ligament if the head, the value is None.
        """
        self.__next = next_node
        self.__x, self.__y = position

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def next(self):
        return self.__next

    def set_next(self, next_ligament):
        """
        Sets the __next value to point to another Ligament object.
        :param next_ligament: A Ligament object.
        :return: None.
        """
        self.__next = next_ligament

    def advance(self):
        """
        Advances the Ligament forward in the linked list.
        :return: Returns the next ligament, or None.
        """
        n = self.__next
        self.__next = None
        return n


class Snake:
    """
    Snake that uses the Ligaments class as its infrastructure.
    """
    __movement_handlers: Dict[Direction, Callable] = {
        'Up': lambda head: Ligament((head.x, head.y + 1)),
        'Down': lambda head: Ligament((head.x, head.y - 1)),
        'Right': lambda head: Ligament((head.x + 1, head.y)),
        'Left': lambda head: Ligament((head.x - 1, head.y))
    }
    __allowed_turns: Dict[Direction, List[Direction]] = {
        'Up': ['Up', 'Right', 'Left'],
        'Down': ['Down', 'Right', 'Left'],
        'Right': ['Right', 'Up', 'Down'],
        'Left': ['Left', 'Up', 'Down'],
    }

    def __init__(self, position: Tuple[int, int], direction: Direction, length: int):
        """
        Constructor for the Snake class. The position of the snake will be determined by the values given.
        :param position: The starting position of the Snakes tail.
        :param direction: The direction the snake will face once created.
        :param length: The length of the snake.
        """
        if direction not in self.__movement_handlers:
            self.__direction = "Up"
        else:
            self.__direction = direction
        self.__length = length
        self.__current_length = 0
        self.__tail, self.__head = self.__generate_tail_and_head(position, direction, length)

    def __generate_tail_and_head(self, position: Tuple[int, int], direction: Direction, length: int) -> \
            Tuple[Ligament, Ligament]:
        """
        Generates all the Ligaments of the Snake based on values received from the constructor.
        :param position: The starting position of the snakes tail.
        :param direction: The direction of the snake. all the Ligaments will be created based on direction given, using
        handler functions.
        :param length: The amount of Ligaments to be created.
        :return: Returns a tuple for pointer for both the head and tail of the snake.
        """
        tail = Ligament(position, None)
        head = tail
        for _ in range(length - 1):
            handler = self.__movement_handlers.get(direction)
            if handler:
                new = handler(head)
                head.set_next(new)
                head = new
        self.__current_length = length
        return tail, head

    def move(self):
        """
        Moves the Snake one position forward depending on the value of its direction.
        :return: None.
        """
        handler = self.__movement_handlers.get(self.__direction)
        if not handler:
            # do something bad input
            pass
        new_head = handler(self.__head)
        self.__head.set_next(new_head)
        self.__head = new_head
        self.__current_length += 1
        if self.__current_length > self.__length:
            self.__tail = self.__tail.advance()
            self.__current_length -= 1

    def turn(self, turn_direction: Direction):
        """
        Changes the direction of the Snake.
        :param turn_direction: New snake direction.
        :return: None.
        """
        good_options = self.__allowed_turns.get(self.__direction)
        if turn_direction in good_options:
            self.__direction = turn_direction

    def grow_by_x(self, amount: int):
        """
        Adds a given amount of Ligaments to the snake.
        :param amount: The mount of Ligaments to be added to the Snake.
        :return: None.
        """
        self.__length += amount

    def snake_positions(self):
        """
        :return: Returns a list of all the positions of the Snakes Ligaments.
        """
        coordinates = []
        current = self.__tail
        while current:
            coordinates.append((current.x, current.y))
            current = current.next
        return coordinates

    @property
    def head(self) -> Tuple[int, int]:
        return self.__head.x, self.__head.y
