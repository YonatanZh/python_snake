##########################################################################################
# FILE : snake_main.py
# WRITER : Yonatan Zhenin , Yonatanzh , 208623397, Yahel Uffenheimer, yahelo, 318377751
# EXERCISE : intro2cs1 ex10 2021
# DESCRIPTION: The main loop for the game.
##########################################################################################
from game_display import GameDisplay
from game_manager import GameManager

ALLOWED_KEYS = ['Up', 'Down', 'Left', 'Right']


def get_key(gd):
    """
    Gets key from user.
    :param gd: GameDisplay class
    :return: Key press, if none were pressed, None.
    """
    raw_key = gd.get_key_clicked()
    if raw_key in ALLOWED_KEYS:
        return raw_key
    return None


def main_loop(gd: GameDisplay) -> None:
    """
    The main loop of the snake game.
    :param gd: GameDisplay class
    :return: None
    """
    game = GameManager()
    gd.show_score(game.score)
    first = True
    while True:
        if first:
            is_alive = True
            first = False
        else:
            key = get_key(gd)
            is_alive = game.tick(key)
        colours = game.as_colours()
        for pigment, locations in colours.items():
            for coordinate in locations:
                gd.draw_cell(coordinate[0], coordinate[1], pigment)
        gd.show_score(game.score)
        gd.end_round()
        if not is_alive:
            break
