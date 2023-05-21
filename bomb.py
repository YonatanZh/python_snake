##########################################################################################
# FILE : bomb.py
# WRITER : Yonatan Zhenin , Yonatanzh , 208623397, Yahel Uffenheimer, yahelo, 318377751
# EXERCISE : intro2cs1 ex10 2021
# DESCRIPTION: Bomb class for the ex10 game
##########################################################################################
from typing import Tuple, List
from game_parameters import get_random_bomb_data

class Bomb:
    """
    Class that represents a bomb.
    """
    def __init__(self):
        """
        Constructor for the Bomb class.
        """
        self.__x, self.__y, self.__radius, self.__time = get_random_bomb_data()

    def bomb_positions(self) -> List[Tuple[int, int]]:
        """
        :return: Returns a list of the current bomb positions.
        """
        if self.exploding:
            return self.__manhattan_radius()
        elif self.__time <= 0:
            return []
        return [(self.__x, self.__y)]

    def __manhattan_radius(self) -> List[Tuple[int, int]]:
        """
        Calculates the positions of the shock wave created when a bomb explodes.
        :return: Returns a list of the bombs shock waves in current state.
        """
        if self.__time == 0:
            return [(self.__x, self.__y)]
        r = - self.__time
        point_a, point_b, point_c, point_d = (self.__x - r, self.__y), (self.__x, self.__y + r), \
                                             (self.__x + r, self.__y), (self.__x, self.__y - r)
        result = []
        for i in range(0, r):
            result += [(point_a[0] + i, point_a[1] + i), (point_b[0] + i, point_b[1] - i),
                       (point_c[0] - i, point_c[1] - i), (point_d[0] - i, point_d[1] + i)]
        return result

    @property
    def radius(self) -> int:
        return self.__radius

    @property
    def finished_exploding(self):
        return (self.__radius + self.__time) < 0

    @property
    def exploding(self):
        return self.__time <= 0 and not (self.__radius + self.__time) < 0

    def tick(self):
        """
        Reduces the life time of a bomb.
        :return: None.
        """
        self.__time -= 1
