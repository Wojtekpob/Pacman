import pygame
from pacman import Player
from game import Game
from settings import *


def test_map_positon_00():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(0, 60, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (0, 0)

def test_map_positon_11():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (1, 1)

def test_map_positon_12():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (1, 2)


def test_map_positon_22():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(40, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (2, 2)


def test_map_positon_33():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(60, 120, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (3, 3)


def test_map_position_right():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(30, 90, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position() == (1, 1)


def test_map_position_right_move():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(40, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 2
    assert pacman.map_position()[1] == 1

def test_map_position_right_move_barely():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(39, 99, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 1


def test_map_position_down_move():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 2


def test_map_position_left_move():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(0, 100, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 0
    assert pacman.map_position()[1] == 2

def test_map_position_up_move():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 60, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 0


def test_pacman_is_able_to_turn():
    game = Game()
    pacman = Player('pacman.png', game)
    assert pacman.map_position()[0] == 1
    assert pacman.map_position()[1] == 1
    assert pacman.map_position()[1] == 1
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_right_wall_start_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_right_wall_end_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_right_wall_mid_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 120, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is False


def test_pacman_is_able_to_turn_right_wall_start_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 90, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is False


def test_pacman_is_able_to_turn_right_wall_end_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('right') is True


def test_pacman_is_able_to_turn_left_wall_end_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is True


def test_pacman_is_able_to_turn_left_wall_start_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is True


def test_pacman_is_able_to_turn_left_wall_mid_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 120, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is False


def test_pacman_is_able_to_turn_left_wall_start_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 81, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is False


def test_pacman_is_able_to_turn_left_wall_end_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 151, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('left') is False


def test_pacman_is_able_to_turn_up_wall_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 85, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_move() is True


def test_pacman_is_able_to_turn_up_wall_end_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(100, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('up') is False


def test_pacman_is_able_to_turn_up_wall_start_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('up') is True


def test_pacman_is_able_to_turn_down_wall_start_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 160, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is True


def test_pacman_is_able_to_turn_down_wall_end_true():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(120, 180, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is True


def test_pacman_is_able_to_turn_up_wall_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 80, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('up') is False


def test_pacman_is_able_to_turn_down_wall_true_1():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 200, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is True


def test_pacman_is_able_to_turn_down_wall_true_2():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 210, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_move() is True


def test_pacman_is_able_to_turn_down_wall_false():
    game = Game()
    pacman = Player('pacman.png', game)
    pacman.rect = pygame.Rect(20, 220, PLAYERS_WIDTH, PLAYERS_HEIGHT)
    assert pacman.able_to_change_direction('down') is False
