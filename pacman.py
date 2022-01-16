from statistics import mode
import pygame
from pygame import K_LEFT, K_RIGHT, K_SPACE, K_UP, KEYDOWN, USEREVENT, K_s, key, rect
from math import fabs, sqrt
from settings import (
    BLACK, BLUE, BLUE_GHOST_STARTING_POSITION, CELL_LENGHT, COIN_RADIOUS, GHOST_HEIGHT, GHOST_RADIOUS, GHOST_WIDTH, ORANGE, ORANGE_GHOST_STARTING_POSITION, PINK, PINK_GHOST_STARTING_POSITION, POWERUP_VALUE, RED, RED_GHOST_STARTING_POSITION, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    MAZE_WIDTH, MAZE_HEIGHT,
    PLAYERS_HEIGHT,
    PLAYERS_SPEED,
    PLAYERS_STARTING_POSITION,
    PLAYERS_WIDTH, TOP_EMPTY_SPACE, TURQUOISE, WALL_SIDE_LENGHT, WHITE, YELLOW,
    COIN_VALUE, FRUIT_VALUE, frightened_mode
)
from random import sample


class Player:
    def __init__(self, image, game):
        """
        Creating MovingObject class, which will

        Arg:
        speed (int): speed of the object
        position x and y: starting position on the map
        image (.png file): image representing object
        """
        self.speed = PLAYERS_SPEED
        self.positionx = PLAYERS_STARTING_POSITION[0]
        self.positiony = PLAYERS_STARTING_POSITION[1]
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (PLAYERS_WIDTH, PLAYERS_HEIGHT))
        self.image = image
        self.image_right = image
        self.image_left = pygame.transform.rotate(image, 180)
        self.image_up = pygame.transform.rotate(image, 90)
        self.image_down = pygame.transform.rotate(image, 270)
        self.game = game
        # self.initialize_wall_sensors()
        # self.image_right = image
        # self.image_left = pygame.transform.rotate(image, 180)
        # self.image_up = pygame.transform.rotate(image, 90)
        # self.image_left = pygame.transform.rotate(image, 180)
        self.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        self.direction = None
        self.lives = 2
        self.score = 0

    def map_position(self):
        x_map_pos = self.rect.x // 20
        y_map_pos = (self.rect.y - TOP_EMPTY_SPACE) // 20
        return (x_map_pos, y_map_pos)


    def move(self, keys_pressed):
        """
        Takes pressed keys and makes the object move that direction
        Arg:
        keys_pressed: direction of movement is based on keys(W, A, S, D)
        """
        self.change_direction(keys_pressed)
        # if self.able_to_move(self.direction):
        for _ in range(self.speed):
            if self.able_to_move():
                if self.direction == 'right':
                    self.rect.x += 1
                elif self.direction == 'left':
                    self.rect.x -= 1
                elif self.direction == 'down':
                    self.rect.y += 1
                elif self.direction == 'up':
                    self.rect.y -= 1
        # self.move_sensors()

    def next_direction(self, keys_pressed):
        if keys_pressed[pygame.K_a] or keys_pressed[K_LEFT]:
            return 'left'
        elif keys_pressed[pygame.K_w] or keys_pressed[K_UP]:
            return 'up'
        elif keys_pressed[pygame.K_d] or keys_pressed[K_RIGHT]:
            return 'right'
        elif keys_pressed[pygame.K_s] or keys_pressed[K_s]:
            return 'down'

    def change_direction(self, keys_pressed):
        next_direction = self.next_direction(keys_pressed)
        if next_direction == 'left' and self.able_to_change_direction('left'):
            self.direction = 'left'
            self.image = self.image_left
        if next_direction == 'up' and self.able_to_change_direction('up'):
            self.direction = 'up'
            self.image = self.image_up
        if next_direction == 'down' and self.able_to_change_direction('down'):
            self.direction = 'down'
            self.image = self.image_down
        if next_direction == 'right' and self.able_to_change_direction('right'):
            self.direction = 'right'
            self.image = self.image_right

    def able_to_move(self):
        x, y = self.map_position()
        if (self.rect.x % 20 == 0 and self.rect.y % 20 == 0):
            if self.direction == 'left':
                return not self.game.map_dict[(x - 1, y)] == '1'
            elif self.direction == 'right':
                return not self.game.map_dict[(x + 1, y)] == '1'
            elif self.direction == 'up':
                return not self.game.map_dict[(x, y - 1)] == '1'
            elif self.direction == 'down':
                return not self.game.map_dict[(x, y + 1)] == '1'
        else:
            return True

    def able_to_change_direction(self, direction):
        x, y = self.map_position()
        if (self.rect.x % 20 == 0 and self.rect.y % 20 == 0) or self.is_opposite(direction):
            if direction == 'left':
                return not self.game.map_dict[(x - 1, y)] == '1'
            elif direction == 'right':
                return not self.game.map_dict[(x + 1, y)] == '1'
            elif direction == 'up':
                return not self.game.map_dict[(x, y - 1)] == '1'
            elif direction == 'down':
                return not self.game.map_dict[(x, y + 1)] == '1'
        else:
            return False

    def is_opposite(self, direction):
        if self.direction == 'left':
            if direction == 'right':
                return True
        if self.direction == 'right':
            if direction == 'left':
                return True
        if self.direction == 'up':
            if direction == 'down':
                return True
        if self.direction == 'down':
            if direction == 'up':
                return True

    def draw(self):
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.draw_lives()

    def draw_lives(self):
        self.game.draw_text('Georgia Pro Black', 40, 'Lives:', YELLOW,
        20, 680)
        for i in range(self.lives):
            self.game.screen.blit(self.image_right, (110 + i * 20, 685))

    def eat_object(self):
        eat_rect = pygame.Rect(self.rect.x, self.rect.y, PLAYERS_WIDTH - 10, PLAYERS_HEIGHT - 10)
        for coin in self.game.coins:
            if eat_rect.colliderect(coin.rect):
                if isinstance(coin, PowerupCoin):
                    pygame.time.set_timer(frightened_mode, 1, loops=1)
                    self.game.state = 'win'
                # for event in pygame.event.get():
                    # if frightened_mode.type == event.type:
                    #     print('kek')
                    #     pygame.event.pump()
                    # pass
                self.game.coins.remove(coin)
                self.score += coin.value
        # print(pygame.event.get())

    def ghost_interaction(self):
        eat_rect = pygame.Rect(self.rect.x, self.rect.y, PLAYERS_WIDTH - 10, PLAYERS_HEIGHT - 10)
        for ghost in self.game.ghosts:
            if eat_rect.colliderect(ghost.rect):
                if ghost.mode == 'normal':
                    self.game.back_to_start()
                    self.lives -= 1
                elif ghost.mode == 'scared':
                    ghost.dead_mode()
                    self.score += 200


class Ghost:
    def __init__(self, game):
        positionx, positiony = RED_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(positionx, positiony, GHOST_WIDTH, GHOST_HEIGHT)
        self.game = game
        self.starting_pos = RED_GHOST_STARTING_POSITION
        self.player_position = self.game.player.map_position()
        self.direction = None
        self.color = RED
        self.mode = 'normal'
        self.speed = PLAYERS_SPEED

    def map_position(self):
        x_map_pos = self.rect.x // 20
        y_map_pos = (self.rect.y - TOP_EMPTY_SPACE) // 20
        return (x_map_pos, y_map_pos)

    def starting_map_position(self):
        return (self.starting_pos[0] // 20, self.starting_pos[1] // 20)

    def draw(self):
        if not self.mode == 'dead':
            color = BLUE if self.mode == 'scared' else self.color
            pygame.draw.circle(self.game.screen, color, (self.rect.x + 10, self.rect.y + 10), GHOST_RADIOUS)
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 6, self.rect.y + 8), 2)
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 14, self.rect.y + 8), 2)
        else:
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 6, self.rect.y + 8), GHOST_RADIOUS - 7)
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 14, self.rect.y + 8), GHOST_RADIOUS - 7)

    def destination(self):
        if self.mode == 'dead':
            if self.map_position()[1] == 11 and self.map_position()[0] < 15 and self.map_position()[0] > 11:
                self.normal_mode()
            return self.starting_map_position()
        else:
            return self.normal_destination()

    def normal_destination(self):
        return self.game.player.map_position()

    def move(self):
        # print(self.destination())
        # print(self.rect.x, self.rect.y)
        # if (self.rect.x % 20 == 0 and self.rect.y % 20 == 0):
        #     if self.mode == 'scared':
        #         self.speed = 1
        # if self.rect.x % 20 == 0 and self.rect.y % 20 == 0:
        #     if self.mode == 'scared':
        #         self.speed = 1
        #         print('scared')
        #     elif self.mode == 'normal' or self.mode == 'dead':
        #         self.speed = 2
        turning_hierarchy = self.random_path() if self.mode == 'scared' else self.find_path()
        if self.able_to_change_direction(turning_hierarchy[0]) and not self.is_opposite(turning_hierarchy[0]):
            self.direction = turning_hierarchy[0]
        elif self.able_to_change_direction(turning_hierarchy[1]) and not self.is_opposite(turning_hierarchy[1]):
            self.direction = turning_hierarchy[1]
        elif self.able_to_change_direction(turning_hierarchy[2]) and not self.is_opposite(turning_hierarchy[2]):
            self.direction = turning_hierarchy[2]
        elif not self.able_to_move():
            self.direction = turning_hierarchy[3]
        for _ in range(self.speed):
            if self.able_to_move():
                self.move_body()

    def move_body(self):
        if self.direction == 'right':
            self.rect.x += 1
        elif self.direction == 'left':
            self.rect.x -= 1
        elif self.direction == 'down':
            self.rect.y += 1
        elif self.direction == 'up':
            self.rect.y -= 1

    def able_to_move(self):
        x, y = self.map_position()
        if (self.rect.x % 20 == 0 and self.rect.y % 20 == 0):
            if self.direction == 'left':
                return not self.game.map_dict[(x - 1, y)] == '1'
            elif self.direction == 'right':
                return not self.game.map_dict[(x + 1, y)] == '1'
            elif self.direction == 'up':
                return not self.game.map_dict[(x, y - 1)] == '1'
            elif self.direction == 'down':
                return not self.game.map_dict[(x, y + 1)] == '1'
        else:
            return True

    def able_to_change_direction(self, direction):
        x, y = self.map_position()
        if self.rect.x % 20 == 0 and self.rect.y % 20 == 0:
            if direction == 'left':
                return not self.game.map_dict[(x - 1, y)] == '1'
            elif direction == 'right':
                return not self.game.map_dict[(x + 1, y)] == '1'
            elif direction == 'up':
                return not self.game.map_dict[(x, y - 1)] == '1'
            elif direction == 'down':
                return not self.game.map_dict[(x, y + 1)] == '1'
        else:
            return False

    def find_path(self):
        # print(self.destination(), self.__class__)
        upright_road = fabs(self.destination()[1] - self.map_position()[1])
        horizontal_road = fabs(self.destination()[0] - self.map_position()[0])
        turning_hierarchy = []
        if upright_road > horizontal_road:
            up_or_down = 'up' if self.destination()[1] < self.map_position()[1] else 'down'
            turning_hierarchy.append(up_or_down)
            if self.destination()[0] < self.map_position()[0]:
                turning_hierarchy.append('left')
                turning_hierarchy.append('right')
            else:
                turning_hierarchy.append('right')
                turning_hierarchy.append('left')
            turning_hierarchy.append(self.opposite(up_or_down))
        else:
            left_or_right = 'left' if self.destination()[0] < self.map_position()[0] else 'right'
            turning_hierarchy.append(left_or_right)
            if self.destination()[1] < self.map_position()[1]:
                turning_hierarchy.append('up')
                turning_hierarchy.append('down')
            else:
                turning_hierarchy.append('down')
                turning_hierarchy.append('up')
            turning_hierarchy.append(self.opposite(left_or_right))
        # print(turning_hierarchy)
        return turning_hierarchy

    def random_path(self):
        return sample(['left', 'right', 'up', 'down'], k=4)

    def is_opposite(self, direction):
        if self.direction == 'left':
            if direction == 'right':
                return True
        if self.direction == 'right':
            if direction == 'left':
                return True
        if self.direction == 'up':
            if direction == 'down':
                return True
        if self.direction == 'down':
            if direction == 'up':
                return True

    def opposite(self, direction):
        if direction == 'left':
            return 'right'
        if direction == 'right':
            return 'left'
        if direction == 'down':
            return 'up'
        if direction == 'up':
            return 'down'

    def scared_mode(self):
        self.mode = 'scared'
        self.speed = 1
        self.direction = self.opposite(self.direction)

    def normal_mode(self):
        self.mode = 'normal'
        self.speed = PLAYERS_SPEED

    def dead_mode(self):
        self.mode = 'dead'
        self.speed = 4


class GhostPink(Ghost):
    def __init__(self, game):
        # super().__init__(game)
        # x, y = PINK_GHOST_STARTING_POSITION
        # self.starting_pos = PINK_GHOST_STARTING_POSITION
        # self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        # self.color = PINK
        self.game = game
        x, y = PINK_GHOST_STARTING_POSITION
        self.starting_pos = PINK_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.direction = None
        self.color = PINK
        self.mode = 'normal'
        self.speed = PLAYERS_SPEED

    def normal_destination(self):
        if self.game.player.direction == 'left':
            return (self.game.player.map_position()[0] - 4, self.game.player.map_position()[1])
        elif self.game.player.direction == 'right' or self.game.player.direction is None:
            return (self.game.player.map_position()[0] + 4, self.game.player.map_position()[1])
        elif self.game.player.direction == 'up':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] - 4)
        elif self.game.player.direction == 'down':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] + 4)

    # def draw(self):
    #     pygame.draw.circle(self.game.screen, PINK, (self.rect.x + 10, self.rect.y + 10), GHOST_RADIOUS)


class GhostOrange(Ghost):
    def __init__(self, game):
        self.game = game
        x, y = ORANGE_GHOST_STARTING_POSITION
        self.starting_pos = ORANGE_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.direction = None
        self.color = ORANGE
        self.mode = 'normal'
        self.speed = PLAYERS_SPEED

    def normal_destination(self):
        if self.road_to_player() > 5:
            return self.game.player.map_position()
        else:
            return (20, 80)

    def road_to_player(self):
        road_horizontal = self.game.player.map_position()[0] - self.map_position()[0]
        road_vertical = self.game.player.map_position()[1] - self.map_position()[1]
        return sqrt(road_horizontal ** 2 + road_vertical ** 2)

    # def draw(self):
    #     pygame.draw.circle(self.game.screen, ORANGE, (self.rect.x + 10, self.rect.y + 10), GHOST_RADIOUS)


class GhostBlue(Ghost):
    def __init__(self, game):
        self.game = game
        self.direction = None
        self.mode = 'normal'
        self.starting_pos = BLUE_GHOST_STARTING_POSITION
        x, y = BLUE_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.color = TURQUOISE
        self.speed = PLAYERS_SPEED

    def normal_destination(self):
        a, b = self.two_cells_in_front_of_player()
        c, d = self.game.ghosts[0].map_position()
        return (2 * a - c, 2 * b - d)

    def two_cells_in_front_of_player(self):
        if self.game.player.direction == 'left':
            return (self.game.player.map_position()[0] - 2, self.game.player.map_position()[1])
        elif self.game.player.direction == 'right' or self.game.player.direction is None:
            return (self.game.player.map_position()[0] + 2, self.game.player.map_position()[1])
        elif self.game.player.direction == 'up':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] - 2)
        elif self.game.player.direction == 'down':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] + 2)

class Wall:
    def __init__(self, posx, posy):
        self.width = WALL_SIDE_LENGHT
        self.height = WALL_SIDE_LENGHT
        self.rect = pygame.Rect(posx, posy, WALL_SIDE_LENGHT, WALL_SIDE_LENGHT)

    # def display_wall(self, screen):
    #     screen.


class EatableObject:
    def __init__(self, positionx, positiony, game):
        self.rect = pygame.Rect(positionx, positiony, CELL_LENGHT, CELL_LENGHT)
        self.game = game
        self.radius = 0
        # image = pygame.image.load('coin.png')
        # image = pygame.transform.scale(image, (3, 3))
        # self.image = image

    def draw(self):
        # if not self.eaten:
            # self.game.screen.blit(self.image, (self.rect.x + 7, self.rect.y + 7))
        pygame.draw.circle(self.game.screen, YELLOW, (self.rect.x + 10, self.rect.y + 10), self.radius)


class Coin(EatableObject):
    def __init__(self, positionx, positiony, game):
        super().__init__(positionx, positiony, game)
        self.value = COIN_VALUE
        self.radius = 3


class PowerupCoin(EatableObject):
    def __init__(self, positionx, positiony, game):
        super().__init__(positionx, positiony, game)
        self.value = POWERUP_VALUE
        self.radius = 6


class Fruit(EatableObject):
    def __init__(self, positionx, positiony, game, image):
        super().__init__(positionx, positiony, game)
        self.value = FRUIT_VALUE
        self.image = image

    def draw(self):
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
