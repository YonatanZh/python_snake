##########################################################################################
# FILE : apple.py
# WRITER : Yonatan Zhenin , Yonatanzh , 208623397, Yahel Uffenheimer, yahelo, 318377751
# EXERCISE : intro2cs1 ex10 2021
# DESCRIPTION: Apple class for the ex10 game.
##########################################################################################
from typing import Tuple
from game_parameters import get_random_apple_data


class Apple:
    """
    Class that represents an apple.
    """
    def __init__(self):
        """
        Constructor fo the Apple class.
        """
        self.__x, self.__y, self.__score = get_random_apple_data()

    def apple_position(self) -> Tuple[int, int]:
        """
        :return: Returns the x,y coordinates of the apple.
        """
        return self.__x, self.__y

    @property
    def score(self) -> int:
        return self.__score
