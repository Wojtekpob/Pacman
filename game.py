import pygame
from pygame.constants import K_SPACE
from pygame.event import Event
from pacman import Coin, EatableObject, Ghost, Player, PowerupCoin, Wall
from settings import (
    BLACK, GHOST_HEIGHT, GHOST_WIDTH, RED, RED_GHOST_STARTING_POSITION, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    MAZE_WIDTH, MAZE_HEIGHT,
    PLAYERS_HEIGHT,
    PLAYERS_SPEED,
    PLAYERS_STARTING_POSITION,
    PLAYERS_WIDTH, TOP_EMPTY_SPACE, WALL_SIDE_LENGHT,
    WHITE, YELLOW, scatter_mode
)

pygame.init()
pygame.font.init()
HIT_WALL = pygame.event.custom_type()


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.walls = []
        self.coins = []
        self.powerup_coins = []
        self.initialize_game()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pacman')
        pygame.display.set_icon(self.icon)
        self.screen = screen
        self.state = 'start'

    def initialize_game(self):
        self.load_images()
        self.create_player_ghosts()
        self.create_map()

    def create_player_ghosts(self):
        """
        Creates object that can move that will represent player.
        """
        self.player = Player(self.player_image, self)
        self.ghosts = [Ghost('red', self)]

    def create_map(self):
        map_dict = {}
        with open('walls.txt') as file_handle:
            for y, row in enumerate(file_handle):
                for x, number in enumerate(row):
                    posx = x * WALL_SIDE_LENGHT
                    posy = y * WALL_SIDE_LENGHT + TOP_EMPTY_SPACE
                    if number != '\n':
                        map_dict[(x, y)] = number
                    if number == '1':
                        self.walls.append(Wall(posx, posy))
                    if number == '2':
                        self.coins.append(Coin(posx, posy, self))
                    if number == '3':
                        self.coins.append(PowerupCoin(posx, posy, self))
        self.map_dict = map_dict

    def run(self):
        """
        Game loop
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print(self.player.score)
            if self.state == 'start':
                # pygame.time.set_timer(scatter_mode, loops=)
                self.display_start_screen()
                self.update_state_start()
            elif self.state == 'game':
                self.upadate_game()
                # print(self.player.map_position())
            elif self.state == 'game over':
                self.display_game_over()
                self.update_game_over()
            self.clock.tick(FPS)
        pygame.quit()

    # def remove_coins(self):
    #     for coin in self.coins:
    #         if self.player.rect.colliderect(coin.rect):
    #             self.coins.remove(coin)

    def upadate_game(self):
        keys_pressed = pygame.key.get_pressed()
        self.player.move(keys_pressed)
        for ghost in self.ghosts:
            ghost.move()
        self.player.eat_object()
        self.player.get_eaten()
        self.display_screen()

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
        self.screen.blit(self.background, (0, TOP_EMPTY_SPACE))
        for coin in self.coins:
            coin.draw()
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.draw_text('Arial Blssssssack', 40, f'SCORE: {self.player.score}', WHITE, 10, 5, True)
        # for wall in self.walls:
        #     if self.player.rect.colliderect(wall.rect):
        #         self.player.direction = None
        # if pygame.eventaaaaaa.get(HIT_WALL):
        #     for wall in self.walls:
        #         scrssssssssssseen.blit(self.player.image, (wall.rect.x, wall.rect.y))
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
        pygame.display.update()

    def update_state_start(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # if event.type

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'game'


    def back_to_start(self):
        self.player.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        for ghost in self.ghosts:
            ghost.rect = pygame.Rect(RED_GHOST_STARTING_POSITION[0], RED_GHOST_STARTING_POSITION[1], GHOST_WIDTH, GHOST_HEIGHT)
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
                self.reset()
                self.state = 'game'

    def reset(self):
        self.coins = []
        self.walls = []
        self.create_map()
        self.player.lives = 2
        for ghost in self.ghosts:
            ghost.rect = pygame.Rect(RED_GHOST_STARTING_POSITION[0], RED_GHOST_STARTING_POSITION[1], GHOST_WIDTH, GHOST_HEIGHT)


if __name__ == '__main__':
    game = Game()
    game.run()
