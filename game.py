from curses import KEY_MARK
from datetime import date
import json
from turtle import pos
from matplotlib.font_manager import json_dump
import pygame
from pygame.event import Event
from pacman import Coin, EatableObject, Ghost, GhostBlue, GhostOrange, GhostPink, GhostRed, Player, PowerupCoin, Wall
from settings import (
    BLACK, BLUE, GHOST_HEIGHT, GHOST_WIDTH, RED, RED_GHOST_STARTING_POSITION, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    MAZE_WIDTH, MAZE_HEIGHT,
    PLAYERS_HEIGHT,
    PLAYERS_SPEED,
    PLAYERS_STARTING_POSITION,
    PLAYERS_WIDTH, TOP_EMPTY_SPACE, WALL_SIDE_LENGHT,
    WHITE, YELLOW, frightened_mode, normal_mode
)

pygame.init()
pygame.font.init()


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False
        self.walls = []
        self.coins = []
        self.ghosts = []
        self.map = 1
        self.load_images()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pacman')
        pygame.display.set_icon(self.icon)
        self.screen = screen
        self.state = 'start'

    def start_new_game(self):
        self.initialize_game()

    def initialize_game(self):
        self.player = Player(self.player_image, self)
        self.ghosts = [GhostRed(self), GhostOrange(self), GhostPink(self), GhostBlue(self)]
        self.load_map()

    def create_player_ghosts(self):
        """
        Creates object that can move that will represent player.
        """
        self.player = Player(self.player_image, self)
        # self.ghosts = [GhostRed(self), GhostOrange(self), GhostPink(self), GhostBlue(self)]

    def create_map(self, maze_map):
        map_dict = {}
        self.walls = []
        self.coins = []
        with open(maze_map) as file_handle:
            for y, row in enumerate(file_handle):
                for x, number in enumerate(row):
                    posx = x * WALL_SIDE_LENGHT
                    posy = y * WALL_SIDE_LENGHT + TOP_EMPTY_SPACE
                    if number != '\n':
                        map_dict[(x, y)] = number
                    if number == '1':
                        self.walls.append(Wall(posx, posy, self))
                    if number == '2':
                        self.coins.append(Coin(posx, posy, self))
                    if number == '3':
                        self.coins.append(PowerupCoin(posx, posy, self))
        self.map_dict = map_dict

    def run(self):
        """
        Game loopa
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print(self.player.score)
                if frightened_mode == event.type:
                    print('kek')
                    pygame.time.set_timer(normal_mode, 6000, loops=1)
                    for ghost in self.ghosts:
                        if not ghost.mode == 'dead':
                            ghost.scared_mode()
                elif normal_mode == event.type:
                    print('xD')
                    for ghost in self.ghosts:
                        if not ghost.mode == 'dead':
                            ghost.normal_mode()
                        self.player.ghost_eaten = 0
                if self.state == 'game':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.pause = True
            if self.state == 'start':
                self.display_start_screen()
                self.update_state_start()
            elif self.state == 'game':
                self.update_game()
                while self.pause:
                    self.save_game()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            self.pause = False
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            self.pause = False
            elif self.state == 'game over':
                self.display_game_over()
                self.update_game_over()
            elif self.state == 'win':
                self.display_win_screen()
                self.update_win_screen()
            self.clock.tick(FPS)
        pygame.quit()

    def save_game(self):
        player_position = self.player.map_position()
        score = self.player.score
        coins_data = []
        ghosts_data = []
        map = self.map
        for coin in self.coins:
            posx = coin.rect.x
            posy = coin.rect.y
            if isinstance(coin, PowerupCoin):
                type = 'powerup'
            else:
                type = 'coin'
            coin_data = {
                'pos': (posx, posy),
                'type': type
            }
            coins_data.append(coin_data)
        for ghost in self.ghosts:
            ghost_data = {
                'direction': ghost.direction,
                'mode': ghost.mode,
                'position': ghost.map_position(),
                'name': ghost.name
            }
            ghosts_data.append(ghost_data)
        game_data = {
            'coins': coins_data,
            'player_position': player_position,
            'score': score,
            'ghosts_data': ghosts_data,
            'map': map
        }
        print(map)
        with open('save.txt', 'w') as file_handle:
            json.dump(game_data, file_handle)

    def load_game(self):
        with open('save.txt') as handle:
            file_handle = json.load(handle)
            player_positionx = file_handle['player_position'][0] * 20
            player_positiony = file_handle['player_position'][1] * 20 + TOP_EMPTY_SPACE
            score = file_handle['score']
            map = file_handle['map']
            self.map = map
            self.load_player((player_positionx, player_positiony), score)
            self.load_map()
            ghosts_data = file_handle['ghosts_data']
            self.coins = []
            for coin_data in file_handle['coins']:
                self.load_coin(coin_data)
            for ghost_data in ghosts_data:
                self.load_ghost(ghost_data)

    def load_player(self, position, score):
        self.player = Player(self.player_image, self)
        x, y = position
        self.player.score = score
        self.player.rect = pygame.Rect(x, y, PLAYERS_WIDTH, PLAYERS_WIDTH)


    def load_coin(self, coin_data):
        posx = coin_data['pos'][0]
        posy = coin_data['pos'][1]
        if coin_data['type'] == 'coin':
            self.coins.append(Coin(posx, posy, self))
        else:
            self.coins.append(PowerupCoin(posx, posy, self))

    def load_ghost(self, ghost_data):
        name = ghost_data['name']
        posx = ghost_data['position'][0] * 20
        posy = ghost_data['position'][1] * 20 + TOP_EMPTY_SPACE
        mode = ghost_data['mode']
        direction = ghost_data['direction']
        if name == 'red':
            ghost = GhostRed(game)
        elif name == 'pink':
            ghost = GhostPink(game)
        elif name == 'orange':
            ghost = GhostOrange(game)
        elif name == 'blue':
            ghost = GhostBlue(game)
        ghost.rect = pygame.Rect(posx, posy, GHOST_HEIGHT, GHOST_WIDTH)
        ghost.direction = direction
        if mode == 'dead':
            ghost.dead_mode()
        elif mode == 'normal':
            ghost.normal_mode()
        elif mode == 'scared':
            ghost.scared_mode()
            pygame.time.set_timer(normal_mode, 3000, loops=1)
        self.ghosts.append(ghost)

    def update_game(self):
        keys_pressed = pygame.key.get_pressed()
        self.player.move(keys_pressed)
        self.player.eat_object()
        self.player.ghost_interaction()
        for ghost in self.ghosts:
            ghost.move()
        if len(self.coins) == 0:
            if self.map < 3:
                self.map += 1
                self.load_map()
                self.back_to_start()
            else:
                self.state = 'win'
                self.back_to_start()
        self.display_screen()

    def load_map(self):
        if self.map == 1:
            self.create_map('map1.txt')
        elif self.map == 2:
            self.create_map('map2.txt')

    def display_screen(self):
        """
        Creates screen, loads images that represents objects
        and then displays background, player and all other objects.
        """
        # for i in range(40):
        #     x = i * (MAZE_WIDTH//28)
        #     pygame.draw.line(self.background, (255, 0, 0), (x, 0), (x, MAZE_HEIGHT)) # pionowe
        #     pygame.draw.line(self.background, (0, 255, 0), (0, x), (MAZE_WIDTH, x)) # poziome
            # jeden kwadracik ma 20 na 20, wymiary planszy to 28x31
        self.screen.fill(BLACK)
        # self.screen.blit(self.background, (0, TOP_EMPTY_SPACE))
        for wall in self.walls:
            wall.draw()
        for coin in self.coins:
            coin.draw()
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.draw_text('Arial Black', 40, f'SCORE: {self.player.score}', WHITE, 10, 5, True)
        pygame.display.update()

    def load_images(self):
        self.player_image = 'pacman_player.png'
        background = pygame.image.load('maze.png')
        background = pygame.transform.scale(background, (MAZE_WIDTH, MAZE_HEIGHT))
        self.background = background
        self.icon = pygame.image.load('pacman.png')

    def draw_text(self, font_name, size, message, color, positionx, positiony, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(message, False, color)
        if centered:
            lenght_of_text = text.get_size()[0]
            positionx = (SCREEN_WIDTH - lenght_of_text) // 2
        self.screen.blit(text, (positionx, positiony))

    def display_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('Georgia Pro Black', 50, 'PUSH SPACEBAR TO START', YELLOW,
        100, 300, True)
        self.draw_text('Georgia Pro Black', 50, 'L TO LOAD', YELLOW,
        100, 600, True)
        pygame.display.update()

    def update_state_start(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if event.type
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.start_new_game()
                self.state = 'game'
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.load_game()
                self.state = 'game'


    def back_to_start(self):
        self.player.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        for ghost in self.ghosts:
            ghost.rect = pygame.Rect(ghost.starting_pos[0], ghost.starting_pos[1], GHOST_WIDTH, GHOST_HEIGHT)
            ghost.normal_mode()

        if self.player.lives < 1:
            self.state = 'game over'

    def display_game_over(self):
        self.screen.fill(BLACK)
        self.draw_text('Georgia Pro Black', 50, 'GAME OVER', RED,
        100, 300, True)
        self.draw_text('Georgia Pro Black', 50, 'PUSH SPACE TO START OVER', RED,
        100, 500, True)
        pygame.display.update()

    def update_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if event.type
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.write_highscore()
                self.reset()
                self.state = 'game'

    def reset(self):
        self.coins = []
        self.walls = []
        self.map = 1
        self.load_map()
        self.player.lives = 2
        self.player.score = 0
        self.player.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        for ghost in self.ghosts:
            ghost.normal_mode()
            ghost.rect = pygame.Rect(ghost.starting_pos[0], ghost.starting_pos[1], GHOST_WIDTH, GHOST_HEIGHT)

    def update_win_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
                self.state = 'game'

    def display_win_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('Georgia Pro Black', 50, 'YOU WON', BLUE,
        100, 300, True)
        self.draw_text('Georgia Pro Black', 50, 'PUSH SPACE TO START AGAIN', WHITE,
        100, 500, True)
        pygame.display.update()

    def write_highscore(self):
        with open('highscore.txt', '+a') as file_handle:
            file_handle.write(f', {self.player.score}')


if __name__ == '__main__':
    game = Game()
    game.run()
