import py
import pygame
from math import fabs, sqrt
from settings import (
    BLACK, BLUE, BLUE_GHOST_STARTING_POSITION, CELL_LENGHT,
    GHOST_HEIGHT, GHOST_RADIOUS, GHOST_WIDTH, ORANGE, ORANGE_GHOST_STARTING_POSITION,
    PINK, PINK_GHOST_STARTING_POSITION, POWERUP_VALUE, RED,
    RED_GHOST_STARTING_POSITION,
    PLAYERS_HEIGHT,
    PLAYERS_SPEED,
    PLAYERS_STARTING_POSITION,
    PLAYERS_WIDTH, TOP_EMPTY_SPACE, TURQUOISE, WALL_SIDE_LENGHT, WHITE, YELLOW,
    COIN_VALUE, frightened_mode
)
from random import sample


class MovingObject:
    def __init__(self, game):
        """
        Initializes moving object object, sets its attributes like game,
        direction, speed, and its position.
        """
        self.game = game
        self.direction = None
        self.speed = PLAYERS_SPEED
        self.rect = pygame.Rect(300, 300, 20, 20)

    def map_position(self):
        """
        Takes pixel position and transfers it to position on map,
        each unit in map position is 20 pixels, the y object position
        is subtracted by 60, because on top of the screen there is space
        for score.
        """
        x_map_pos = self.rect.x // 20
        y_map_pos = (self.rect.y - TOP_EMPTY_SPACE) // 20
        return (x_map_pos, y_map_pos)

    def able_to_move(self):
        """
        Checks on map dictionary if object can move to desired location,
        returns true or false, also if player is object is out of map it teleports
        it back to other side of the map.
        """
        x, y = self.map_position()
        try:
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
        except KeyError:
            self.teleport_back_to_map()
            return True

    def able_to_change_direction(self, direction):
        """
        Checks on map dictionary if object can move to desired location,
        returns true or false.
        """
        x, y = self.map_position()
        try:
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
        except KeyError:
            return True

    def is_opposite(self, direction):
        """
        Checks if the given direction is opposite to the direction attribute.
        Returns true or false.
        """
        if self.direction == self.opposite(direction):
            return True
        else:
            return False

    def opposite(self, direction):
        """
        Returns the opposite of the given direction.
        """
        if direction == 'left':
            return 'right'
        if direction == 'right':
            return 'left'
        if direction == 'down':
            return 'up'
        if direction == 'up':
            return 'down'

    def teleport_back_to_map(self):
        """
        If player is out of map sets player position back on map.
        """
        if self.rect.x < 20:
            self.rect.x = 540
            self.direction = 'left'
        elif self.rect.x > 540:
            self.rect.x = 20
            self.direction = 'right'


class Player(MovingObject):
    def __init__(self, image, game):
        """
        Creates player object sets its position, image, lives, position, score,
        ghost eaten.
        """
        super().__init__(game)
        self.positionx = PLAYERS_STARTING_POSITION[0]
        self.positiony = PLAYERS_STARTING_POSITION[1]
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (PLAYERS_WIDTH, PLAYERS_HEIGHT))
        self.image = image
        self.image_right = image
        self.image_left = pygame.transform.rotate(image, 180)
        self.image_up = pygame.transform.rotate(image, 90)
        self.image_down = pygame.transform.rotate(image, 270)
        self.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        self.lives = 3
        self.score = 0
        self.ghost_eaten = 0
        self.next_direction = None

    def move(self, keys_pressed):
        """
        Takes pressed keys and makes the object move that direction
        keys_pressed: direction of movement is based on keys(W, A, S, D)
        """
        self.teleport_back_to_map()
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_s] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_d]:
            self.next_direction = self.chose_direction(keys_pressed)
            print(self.next_direction)
        if self.next_direction:
            self.change_direction(self.next_direction)
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

    def chose_direction(self, keys_pressed):
        if keys_pressed[pygame.K_a]:
            return 'left'
        elif keys_pressed[pygame.K_w]:
            return 'up'
        elif keys_pressed[pygame.K_s]:
            return 'down'
        elif keys_pressed[pygame.K_d]:
           return 'right'

    def change_direction(self, next_direction):
        """
        Takes keys that are pressed on keyboard as an argument, changes direction
        of player and its image direction if it is able to.
        """
        if next_direction == 'left' and self.able_to_change_direction('left'):
            self.direction = 'left'
            self.image = self.image_left
        elif next_direction == 'up' and self.able_to_change_direction('up'):
            self.direction = 'up'
            self.image = self.image_up
        elif next_direction == 'down' and self.able_to_change_direction('down'):
            self.direction = 'down'
            self.image = self.image_down
        elif next_direction == 'right' and self.able_to_change_direction('right'):
            self.direction = 'right'
            self.image = self.image_right

    def draw(self):
        """
        Displays player and its lives on screen.
        """
        self.game.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.draw_lives()

    def draw_lives(self):
        """
        Draws pacman on the bottom of the screen for each life of player.
        """
        self.game.draw_text('Georgia Pro Black', 40, 'Lives:', YELLOW,
        20, 680)
        for i in range(self.lives):
            self.game.screen.blit(self.image_right, (110 + i * 20, 685))

    def eat_object(self):
        """
        When player collides with coin eats it and add its value to score.
        """
        eat_rect = pygame.Rect(self.rect.x, self.rect.y, PLAYERS_WIDTH - 10, PLAYERS_HEIGHT - 10)
        for coin in self.game.coins:
            if eat_rect.colliderect(coin.rect):
                if isinstance(coin, PowerupCoin):
                    pygame.time.set_timer(frightened_mode, 1, loops=1)
                self.game.coins.remove(coin)
                self.score += coin.value

    def ghost_interaction(self):
        """"
        Checks for collisions with ghosts and based on their state either calls the back to start,
        or eats the ghost.
        """
        eat_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 10, PLAYERS_WIDTH - 18, PLAYERS_HEIGHT - 18)
        for ghost in self.game.ghosts:
            if eat_rect.colliderect(ghost.rect):
                if ghost.mode() == 'normal':
                    self.game.back_to_start()
                    self.lives -= 1
                    if self.lives < 1:
                        self.game.state = 'game over'
                elif ghost.mode() == 'scared':
                    ghost.dead_mode()
                    self.score += 200 * (self.ghost_eaten + 1)
                    self.ghost_eaten += 1


class Ghost(MovingObject):
    def __init__(self, game):
        super().__init__(game)
        self._mode = 'normal'

    def starting_map_position(self):
        """
        returns starting position of ghost on the map.
        """
        return (self.starting_pos[0] // 20, self.starting_pos[1] // 20)

    def draw(self):
        """"
        Draws ghost on screen, based on its mode.
        """
        if not self.mode() == 'dead':
            color = BLUE if self.mode() == 'scared' else self.color
            pygame.draw.circle(self.game.screen, color, (self.rect.x + 10, self.rect.y + 10), GHOST_RADIOUS)
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 6, self.rect.y + 8), 2)
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 14, self.rect.y + 8), 2)
        else:
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 6, self.rect.y + 8), GHOST_RADIOUS - 7)
            pygame.draw.circle(self.game.screen, WHITE, (self.rect.x + 14, self.rect.y + 8), GHOST_RADIOUS - 7)

    def destination(self):
        """
        Returns map position that the ghost will move towards.
        """
        if self.mode() == 'dead':
            if self.map_position()[1] == 11 and self.map_position()[0] < 15 and self.map_position()[0] > 11:
                self.normal_mode()
            return self.starting_map_position()
        else:
            return self.normal_destination()

    def move(self):
        """
        Based on ghost's destination changes its position, and changes direction.
        """
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
        """
        Changes ghost position.
        """
        if self.direction == 'right':
            self.rect.x += 1
        elif self.direction == 'left':
            self.rect.x -= 1
        elif self.direction == 'down':
            self.rect.y += 1
        elif self.direction == 'up':
            self.rect.y -= 1

    def find_path(self):
        """
        Returns the most optimal changing direction options to ghost's destination.
        """
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
        return turning_hierarchy

    def random_path(self):
        """
        Returns list of random ghost's directions.
        """
        return sample(['left', 'right', 'up', 'down'], k=4)

    def scared_mode(self):
        """"
        Sets ghost mode to scared, slows it down and changes its direction.
        """
        self._mode = 'scared'
        self.speed = 1
        self.direction = self.opposite(self.direction)

    def normal_mode(self):
        """
        Sets ghost mode to normal and sets its speed to normal.
        """
        self._mode = 'normal'
        self.speed = PLAYERS_SPEED

    def dead_mode(self):
        """
        Sets ghost mode to dead and speeds it up.
        """
        self._mode = 'dead'
        self.speed = 4

    def mode(self):
        """
        Returns actual ghost's mode.
        """
        return self._mode


class GhostRed(Ghost):
    def __init__(self, game):
        """
        Sets ghost's position, and color.
        """
        super().__init__(game)
        x, y = RED_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.starting_pos = RED_GHOST_STARTING_POSITION
        self.player_position = self.game.player.map_position()
        self.color = RED
        self.name = 'red'

    def normal_destination(self):
        """
        Returns the destination for ghost while its mode is normal.
        Here it is directly to the player.
        """
        return self.game.player.map_position()



class GhostPink(Ghost):
    def __init__(self, game):
        """
        Sets ghost's position, and color.
        """
        super().__init__(game)
        x, y = PINK_GHOST_STARTING_POSITION
        self.starting_pos = PINK_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.color = PINK
        self.name = 'pink'

    def normal_destination(self):
        """
        Returns the destination for ghost while its mode is normal.
        Here it is 4 cells in front of player.
        """
        if self.game.player.direction == 'left':
            return (self.game.player.map_position()[0] - 4, self.game.player.map_position()[1])
        elif self.game.player.direction == 'right' or self.game.player.direction is None:
            return (self.game.player.map_position()[0] + 4, self.game.player.map_position()[1])
        elif self.game.player.direction == 'up':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] - 4)
        elif self.game.player.direction == 'down':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] + 4)

class GhostOrange(Ghost):
    def __init__(self, game):
        """
        Sets ghost's position, and color.
        """
        super().__init__(game)
        x, y = ORANGE_GHOST_STARTING_POSITION
        self.starting_pos = ORANGE_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.color = ORANGE
        self.name = 'orange'

    def normal_destination(self):
        """
        If ghost is far from player returns player's position, else returns
        the left up corner.
        """
        if self.road_to_player() > 8:
            return self.game.player.map_position()
        else:
            return (20, 80)

    def road_to_player(self):
        """
        Returns distance in straight line to player.
        """
        road_horizontal = self.game.player.map_position()[0] - self.map_position()[0]
        road_vertical = self.game.player.map_position()[1] - self.map_position()[1]
        return sqrt(road_horizontal ** 2 + road_vertical ** 2)


class GhostBlue(Ghost):
    def __init__(self, game):
        """
        Sets ghost's position, and color.
        """
        super().__init__(game)
        x, y = BLUE_GHOST_STARTING_POSITION
        self.starting_pos = BLUE_GHOST_STARTING_POSITION
        self.rect = pygame.Rect(x, y, GHOST_WIDTH, GHOST_HEIGHT)
        self.color = TURQUOISE
        self.name = 'blue'

    def normal_destination(self):
        """
        Counts complicated destination.
        Returns it.
        """
        a, b = self.two_cells_in_front_of_player()
        c, d = self.game.ghosts[0].map_position()
        return (2 * a - c, 2 * b - d)

    def two_cells_in_front_of_player(self):
        """
        Returns two cells in from of player.
        """
        if self.game.player.direction == 'left':
            return (self.game.player.map_position()[0] - 2, self.game.player.map_position()[1])
        elif self.game.player.direction == 'right' or self.game.player.direction is None:
            return (self.game.player.map_position()[0] + 2, self.game.player.map_position()[1])
        elif self.game.player.direction == 'up':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] - 2)
        elif self.game.player.direction == 'down':
            return (self.game.player.map_position()[0], self.game.player.map_position()[1] + 2)


class Wall:
    def __init__(self, posx, posy, game):
        """
        Creates wall object, sets its position and game.
        """
        self.width = WALL_SIDE_LENGHT
        self.height = WALL_SIDE_LENGHT
        self.rect = pygame.Rect(posx, posy, WALL_SIDE_LENGHT, WALL_SIDE_LENGHT)
        self.game = game

    def draw(self):
        """Draw blue rectangle in its position."""
        pygame.draw.rect(self.game.screen, BLUE, self.rect)
        pygame.draw.circle(self.game.screen, BLACK, (self.rect.x + 10, self.rect.y + 10), 5)


class EatableObject:
    def __init__(self, positionx, positiony, game):
        """
        Creates eatable object, sets its position and game and radius.
        """
        self.rect = pygame.Rect(positionx, positiony, CELL_LENGHT, CELL_LENGHT)
        self.game = game
        self.radius = 0

    def draw(self):
        """
        Draws yellow circle.
        """
        pygame.draw.circle(self.game.screen, YELLOW, (self.rect.x + 10, self.rect.y + 10), self.radius)


class Coin(EatableObject):
    """
    Creates coin, sets its position and game and radius.
    """
    def __init__(self, positionx, positiony, game):
        super().__init__(positionx, positiony, game)
        self.value = COIN_VALUE
        self.radius = 3


class PowerupCoin(EatableObject):
    """
    Creates coin, sets its position and game and radius.
    """
    def __init__(self, positionx, positiony, game):
        super().__init__(positionx, positiony, game)
        self.value = POWERUP_VALUE
        self.radius = 6
