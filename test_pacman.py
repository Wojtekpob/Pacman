from telnetlib import GA
from matplotlib.pyplot import sca
import pygame
from pacman import (
MovingObject, Player, Ghost,
GhostBlue, GhostOrange,
GhostPink, GhostRed)
from game import Game
from settings import *


def test_map_positon_00():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(0, 60, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (0, 0)

def test_map_positon_11():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (1, 1)

def test_map_positon_12():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (1, 2)


def test_map_positon_22():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(40, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (2, 2)


def test_map_positon_33():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(60, 120, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (3, 3)


def test_map_position_right():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(30, 90, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (1, 1)


def test_map_position_right_move():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(40, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 2
    assert pacman.map_position()[1] == 1

def test_map_position_right_move_barely():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(39, 99, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 1


def test_map_position_down_move():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 2


def test_map_position_left_move():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(0, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 0
    assert pacman.map_position()[1] == 2

def test_map_position_up_move():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 60, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 0


def test_pacman_is_able_to_turn_right_wall_start_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_right_wall_end_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_right_wall_mid_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 120, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is False


def test_pacman_is_able_to_turn_right_wall_start_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 90, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is False


def test_pacman_is_able_to_turn_right_wall_end_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_left_wall_end_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is True


def test_pacman_is_able_to_turn_left_wall_start_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is True


def test_pacman_is_able_to_turn_left_wall_mid_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 120, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is False


def test_pacman_is_able_to_turn_left_wall_start_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 81, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is False


def test_pacman_is_able_to_turn_left_wall_end_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 151, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is False


def test_pacman_is_able_to_turn_up_wall_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 85, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_move() is True


def test_pacman_is_able_to_turn_up_wall_end_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('up') is False


def test_pacman_is_able_to_turn_up_wall_start_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('up') is True


def test_pacman_is_able_to_turn_down_wall_start_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is True


def test_pacman_is_able_to_turn_down_wall_end_true():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(120, 180, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is True


def test_pacman_is_able_to_turn_up_wall_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('up') is False


def test_pacman_is_able_to_turn_down_wall_true_1():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 200, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is True


def test_pacman_is_able_to_turn_down_wall_true_2():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 210, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_move() is True


def test_pacman_is_able_to_turn_down_wall_false():
    game = Game()
    game.load_map()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 220, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is False


def test_is_opposite_left():
    game = Game()
    object = MovingObject(game)
    object.direction = 'left'
    assert object.is_opposite('right')
    assert object.is_opposite('up') is False


def test_is_opposite_right():
    game = Game()
    object = MovingObject(game)
    object.direction = 'right'
    assert object.is_opposite('left')
    assert object.is_opposite('up') is False


def test_is_opposite_up():
    game = Game()
    object = MovingObject(game)
    object.direction = 'up'
    assert object.is_opposite('down')
    assert object.is_opposite('up') is False


def test_is_opposite_down():
    game = Game()
    object = MovingObject(game)
    object.direction = 'down'
    assert object.is_opposite('up')
    assert object.is_opposite('rghit') is False


def test_opposite():
    game = Game()
    object = MovingObject(game)
    assert object.opposite('left') == 'right'
    assert object.opposite('right') == 'left'
    assert object.opposite('up') == 'down'
    assert object.opposite('down') == 'up'


def test_ghost_interaction_normal_hit():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    player.rect = pygame.Rect(50, 50, 50, 50)
    ghost.rect = pygame.Rect(40, 40, 40, 40)
    game.ghosts = [ghost]
    player.ghost_interaction()
    assert player.lives == 2
    assert player.rect.x, player.rect.y == PLAYERS_STARTING_POSITION
    assert ghost.rect.x, ghost.rect.y == RED_GHOST_STARTING_POSITION
    assert ghost.mode() == 'normal'


def test_ghost_interaction_normal_hit_game_over():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    player.rect = pygame.Rect(50, 50, 50, 50)
    ghost.rect = pygame.Rect(40, 40, 40, 40)
    game.ghosts = [ghost]
    player.lives = 1
    player.ghost_interaction()
    assert player.lives == 0
    assert ghost.mode() == 'normal'
    assert game.state == 'game over'

def test_ghost_interaction_normal_not_hit():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    player.rect = pygame.Rect(50, 50, 50, 50)
    ghost.rect = pygame.Rect(200, 200, 40, 40)
    game.ghosts = [ghost]
    player.ghost_interaction()
    assert player.lives == 3
    assert player.rect.x, player.rect.y == (50, 50)
    assert ghost.rect.x, ghost.rect.y == (200, 200)
    assert ghost.mode() == 'normal'


def test_ghost_interaction_scared_hit():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    player.rect = pygame.Rect(50, 50, 50, 50)
    ghost.rect = pygame.Rect(40, 40, 40, 40)
    game.ghosts = [ghost]
    ghost.scared_mode()
    player.ghost_interaction()
    assert player.lives == 3
    assert player.rect.x, player.rect.y == (50, 50)
    assert ghost.rect.x, ghost.rect.y == (40, 40)
    assert ghost.mode() == 'dead'
    assert player.ghost_eaten == 1
    assert player.score == 200


def test_ghost_interaction_dead_hit():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    player.rect = pygame.Rect(50, 50, 50, 50)
    ghost.rect = pygame.Rect(40, 40, 40, 40)
    game.ghosts = [ghost]
    ghost.dead_mode()
    player.ghost_interaction()
    assert player.lives == 3
    assert player.rect.x, player.rect.y == (50, 50)
    assert ghost.rect.x, ghost.rect.y == (40, 40)
    assert ghost.mode() == 'dead'


def test_ghost_destination():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    game.ghosts = [ghost]
    ghost.dead_mode()
    assert ghost.destination() == ghost.starting_map_position()


def test_ghost_destination_revive():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    game.ghosts = [ghost]
    ghost.dead_mode()
    ghost.rect.x = 280
    ghost.rect.y = 220 + TOP_EMPTY_SPACE
    ghost.destination()
    assert ghost.mode() == 'normal'


def test_ghost_move_body():
    game = Game()
    game.initialize_game()
    ghost = GhostRed(game)
    ghost.direction = 'right'
    ghost.move_body()
    assert ghost.rect.x == RED_GHOST_STARTING_POSITION[0] + 1
    assert ghost.rect.y == RED_GHOST_STARTING_POSITION[1]


# def test_ghost_find_path_up_left(monkeypatch):
#     game = Game()
#     ghost = Ghost(game)
#     def return_set_position():
#         return 1
#     monkeypatch.setattr('ghost.destination()', return_set_position())
#     # dest = ghost.destination
#     # print(ghost.destination())
#     assert ghost.destination() == 1


def test_ghost_modes():
    game = Game()
    ghost = Ghost(game)
    assert ghost.mode() == 'normal'
    assert ghost.speed == 2
    ghost.dead_mode()
    assert ghost.mode() == 'dead'
    assert ghost.speed == 4
    ghost.scared_mode()
    assert ghost.mode() == 'scared'
    assert ghost.speed == 1


def test_red_ghost_normal_destination():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostRed(game)
    assert ghost.normal_destination() == player.map_position()


def test_pink_ghost_normal_destination_left():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    player.rect = pygame.Rect(200, 200, 20, 20)
    player.direction = 'left'
    ghost = GhostPink(game)
    assert ghost.normal_destination() == (6, 7)


def test_pink_ghost_normal_destination_right():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    player.rect = pygame.Rect(200, 200, 20, 20)
    player.direction = 'right'
    ghost = GhostPink(game)
    assert ghost.normal_destination() == (14, 7)


def test_pink_ghost_normal_destination_up():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    player.rect = pygame.Rect(200, 200, 20, 20)
    player.direction = 'up'
    ghost = GhostPink(game)
    assert ghost.normal_destination() == (10, 3)


def test_pink_ghost_normal_destination_down():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    player.rect = pygame.Rect(200, 200, 20, 20)
    player.direction = 'down'
    ghost = GhostPink(game)
    assert ghost.normal_destination() == (10, 11)


def test_orange_ghost_road_to_player():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostOrange(game)
    player.rect = pygame.Rect(20, 140, 20, 20)
    ghost.rect = pygame.Rect(80, 60, 20, 20)
    assert int(ghost.road_to_player()) == 5


def test_orange_ghost_normal_destionation_close_to_player():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostOrange(game)
    player.rect = pygame.Rect(20, 100, 20, 20)
    ghost.rect = pygame.Rect(80, 60, 20, 20)
    assert ghost.road_to_player() < 5
    assert ghost.normal_destination() == (20, 80)


def test_orange_ghost_normal_destionation_far_from_player():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost = GhostOrange(game)
    player.rect = pygame.Rect(20, 1000, 20, 20)
    ghost.rect = pygame.Rect(80, 60, 20, 20)
    assert ghost.road_to_player() > 5
    assert ghost.normal_destination() == player.map_position()


def test_ghost_blue_normal_destionation_left_to_right():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost_blue = GhostBlue(game)
    player.direction = 'right'
    ghost_red = GhostRed(game)
    game.ghosts = [ghost_red, ghost_blue]
    player.rect = pygame.Rect(420, 140, 20, 20)
    ghost_blue.rect = pygame.Rect(80, 60, 20, 20)
    ghost_red.rect = pygame.Rect(400, 140, 20, 20)
    assert ghost_blue.two_cells_in_front_of_player() == (23, 4)
    assert ghost_red.map_position() == (20, 4)
    assert ghost_blue.normal_destination() == (26, 4)


def test_ghost_blue_normal_destionation_right_to_left():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost_blue = GhostBlue(game)
    player.direction = 'right'
    ghost_red = GhostRed(game)
    game.ghosts = [ghost_red, ghost_blue]
    player.rect = pygame.Rect(420, 140, 20, 20)
    ghost_blue.rect = pygame.Rect(80, 60, 20, 20)
    ghost_red.rect = pygame.Rect(520, 140, 20, 20)
    assert ghost_blue.two_cells_in_front_of_player() == (23, 4)
    assert ghost_red.map_position() == (26, 4)
    assert ghost_blue.normal_destination() == (20, 4)


def test_ghost_blue_normal_destionation_bot_to_top():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost_blue = GhostBlue(game)
    player.direction = 'right'
    ghost_red = GhostRed(game)
    game.ghosts = [ghost_red, ghost_blue]
    player.rect = pygame.Rect(420, 140, 20, 20)
    ghost_blue.rect = pygame.Rect(80, 60, 20, 20)
    ghost_red.rect = pygame.Rect(460, 100, 20, 20)
    assert ghost_blue.two_cells_in_front_of_player() == (23, 4)
    assert ghost_red.map_position() == (23, 2)
    assert ghost_blue.normal_destination() == (23, 6)


def test_ghost_blue_normal_destionation_top_to_bot():
    game = Game()
    player = Player('pacman_player.png', game)
    game.player = player
    ghost_blue = GhostBlue(game)
    player.direction = 'right'
    ghost_red = GhostRed(game)
    game.ghosts = [ghost_red, ghost_blue]
    player.rect = pygame.Rect(420, 140, 20, 20)
    ghost_blue.rect = pygame.Rect(80, 60, 20, 20)
    ghost_red.rect = pygame.Rect(460, 180, 20, 20)
    assert ghost_blue.two_cells_in_front_of_player() == (23, 4)
    assert ghost_red.map_position() == (23, 6)
    assert ghost_blue.normal_destination() == (23, 2)