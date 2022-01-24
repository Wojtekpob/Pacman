import json
import pygame
import csv
from pacman import Coin, GhostBlue, GhostOrange, GhostPink, GhostRed, Player, PowerupCoin, Wall
from settings import (
    BLACK, BLUE, CELL_LENGHT, DARK_GREEN, GHOST_HEIGHT,
    GHOST_WIDTH, GREEN, ORANGE, PACMAN_ICON, PAUSE_RECT_SIDE,
    PLAYER_PHOTO, RED, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    PLAYERS_HEIGHT,
    PLAYERS_STARTING_POSITION,
    PLAYERS_WIDTH, TOP_EMPTY_SPACE, WALL_SIDE_LENGHT,
    WHITE, YELLOW, frightened_mode, normal_mode
)
pygame.init()
pygame.font.init()


class Game:
    def __init__(self):
        """
        while creating game it initializes clock, sets running to True, pause to False,
        initializes walls, coins, ghosts lists and name, sets map to first, alse creates
        pygame display instantion and sets it's sie, icon and caption and makes the screen
        atribute so other functions can use it to display things, sets state to start screen.
        """
        self.clock = pygame.time.Clock()
        self.running = True
        self.pause = False
        self.walls = []
        self.coins = []
        self.ghosts = []
        self.name = ''
        self.map = 1
        self.load_images()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pacman')
        pygame.display.set_icon(self.icon)
        self.screen = screen
        self.state = 'start'

    def initialize_game(self):
        """
        This method initializes player and ghosts instantions, loads the map proper map,
        it is used to start a new game.
        """
        self.player = Player(self.player_image, self)
        self.ghosts = [GhostRed(self), GhostOrange(self), GhostPink(self), GhostBlue(self)]
        self.load_map()

    def create_map(self, maze_map):
        """
        Creates map from maps txt files by reading it and creating wall objects for each 1,
        normal coins objects for 2, powerup coins for 3 and does nothing for 0,
        also creates or replaces map dictionary so the moving objects can see the enviroment,
        also replaces or makes walls and coins lists so the game can iteract with it.
        """
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
        Game loop; enables to display the game, checks for the pygame events,
        updates start screen, game, highscores and winning screen, limits the fps.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print(self.player.score)
                if frightened_mode == event.type:
                    pygame.time.set_timer(normal_mode, 6000, loops=1)
                    for ghost in self.ghosts:
                        if not ghost.mode() == 'dead':
                            ghost.scared_mode()
                elif normal_mode == event.type:
                    for ghost in self.ghosts:
                        if not ghost.mode() == 'dead':
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
                    self.display_pause()
                    self.update_pause()
            elif self.state == 'game over':
                self.display_game_over()
                self.update_game_over()
            elif self.state == 'win':
                self.display_win_screen()
                self.update_win_screen()
            elif self.state == 'highscore':
                self.display_highscore_screen()
                self.update_highscore_screen()
            self.clock.tick(FPS)
        pygame.quit()

    def display_pause(self):
        """
        This method displays the screen while state of the game is pause,
        draws rectangle in the middle, says the game is paused and tells you what to
        press to unpause.
        """
        y_rect_position = (SCREEN_HEIGHT - TOP_EMPTY_SPACE - PAUSE_RECT_SIDE) // 2
        x_rect_position = (SCREEN_WIDTH - PAUSE_RECT_SIDE) // 2
        pause_rect = pygame.Rect(x_rect_position, y_rect_position, PAUSE_RECT_SIDE, PAUSE_RECT_SIDE)
        pygame.draw.rect(self.screen, DARK_GREEN, pause_rect)
        self.draw_text('Georgia Pro Black', 130, "PAUSED", WHITE, 1, 200, True)
        self.draw_text('Georgia Pro Black', 60, "SPACE TO CONTINUE", WHITE, 1, 400, True)
        pygame.display.update()

    def update_pause(self):
        """
        Updates all events that happens while the game is paused, the game also
        saves while its paused.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.pause = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.pause = False
            if event.type == normal_mode:
                pygame.time.set_timer(normal_mode, 6000, loops=1)

    def save_game(self):
        """
        Saves coins, player, map, ghosts positions and attributes data by writing
        it to the json file.
        """
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
                'mode': ghost.mode(),
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
        with open('saved/save.txt', 'w') as file_handle:
            json.dump(game_data, file_handle)

    def load_game(self):
        """
        Loads the game from the saved json file that contains informations about
        player, ghosts, map and coins attributes data.
        """
        with open('saved/save.txt') as handle:
            file_handle = json.load(handle)
            player_positionx = file_handle['player_position'][0] * CELL_LENGHT
            player_positiony = file_handle['player_position'][1] * CELL_LENGHT + TOP_EMPTY_SPACE
            score = file_handle['score']
            map = file_handle['map']
            self.map = map
            self.load_player((player_positionx, player_positiony), score)
            self.load_map()
            ghosts_data = file_handle['ghosts_data']
            self.coins = []
            self.ghosts = []
            for coin_data in file_handle['coins']:
                self.load_coin(coin_data)
            for ghost_data in ghosts_data:
                self.load_ghost(ghost_data)

    def load_player(self, position, score):
        """
        Creates player after load form saved file. By setting its position,
        score and his image.
        """
        self.player = Player(self.player_image, self)
        x, y = position
        self.player.score = score
        self.player.rect = pygame.Rect(x, y, PLAYERS_WIDTH, PLAYERS_WIDTH)

    def load_coin(self, coin_data):
        """
        Creates a coin and sets its position for each coin saved.
        """
        posx = coin_data['pos'][0]
        posy = coin_data['pos'][1]
        if coin_data['type'] == 'coin':
            self.coins.append(Coin(posx, posy, self))
        else:
            self.coins.append(PowerupCoin(posx, posy, self))

    def load_ghost(self, ghost_data):
        """
        Creates all ghosts by setting their positions, directions and modes
        from the saved file.
        """
        name = ghost_data['name']
        posx = ghost_data['position'][0] * CELL_LENGHT
        posy = ghost_data['position'][1] * CELL_LENGHT + TOP_EMPTY_SPACE
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
        """
        Each frame updates player, ghosts position, loads next map when there are
        no more coins to eat, also updates coin list by player eating coins.
        """
        keys_pressed = pygame.key.get_pressed()
        self.player.move(keys_pressed)
        self.player.eat_object()
        self.player.ghost_interaction()
        for ghost in self.ghosts:
            ghost.move()
        if len(self.coins) == 0:
            self.player.score += 2000
            if self.map < 4:
                self.map += 1
                self.load_map()
                self.back_to_start()
            else:
                self.state = 'win'
                self.back_to_start()
        self.display_screen()

    def load_map(self):
        """
        Calls the create map method based on what map should be active now.
        """
        if self.map == 1:
            self.create_map('maps/map1.txt')
        elif self.map == 2:
            self.create_map('maps/map2.txt')
        elif self.map == 3:
            self.create_map('maps/map3.txt')

    def display_screen(self):
        """
        Displays the screen while the game state is active, fills the screen with black,
        draws coins, player and ghosts and displays score on top of screen.
        """
        self.screen.fill(BLACK)
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
        """"
        Loads player photo and game icon.
        """
        self.player_image = PLAYER_PHOTO
        self.icon = pygame.image.load(PACMAN_ICON)

    def draw_text(self, font_name, size, message, color, positionx, positiony, centered=False):
        """
        Helping method that enables to display text on screen in easier way.
        """
        font = pygame.font.SysFont(font_name, size)
        text = font.render(message, False, color)
        if centered:
            lenght_of_text = text.get_size()[0]
            positionx = (SCREEN_WIDTH - lenght_of_text) // 2
        self.screen.blit(text, (positionx, positiony))

    def display_start_screen(self):
        """
        Displays the screen while its the start of the game, writes helping texts
        to inform player how to start game, see highscores and how to load game.
        """
        self.screen.fill(BLACK)
        self.draw_text('Georgia Pro Black', 80, 'SPACE TO START', YELLOW, 100, 100, True)
        self.draw_text('Georgia Pro Black', 50, 'L TO LOAD SAVED GAME', YELLOW, 100, 600, True)
        self.draw_text('Georgia Pro Black', 50, 'H TO SEE HIGHSCORES', YELLOW, 100, 400, True)
        self.draw_text('Georgia Pro Black', 30, 'By Wojciech Pobocha', WHITE, 340, 700)
        pygame.display.update()

    def update_state_start(self):
        """
        Takes care of all events (keys clicked) while the game is in
        start state.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.initialize_game()
                    self.state = 'game'
                if event.key == pygame.K_l:
                    self.load_game()
                    self.state = 'game'
                if event.key == pygame.K_h:
                    self.state = 'highscore'

    def back_to_start(self):
        """"
        Resets player and ghosts to their starting positions and sets ghosts to normal mode.
        """
        self.player.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        for ghost in self.ghosts:
            ghost.rect = pygame.Rect(ghost.starting_pos[0], ghost.starting_pos[1], GHOST_WIDTH, GHOST_HEIGHT)
            ghost.normal_mode()

    def display_game_over(self):
        """
        Displays the screen while game state is game over, writes information text,
        informs that user lost, updates player's name.
        """
        self.screen.fill(BLACK)
        self.draw_text('Georgia Pro Black', 100, 'GAME OVER', RED, 100, 100, True)
        self.draw_text('Georgia Pro Black', 50, 'PUSH SPACE TO START OVER', RED, 100, 500, True)
        self.change_name_interface()
        pygame.display.update()

    def update_game_over(self):
        """
        Takes care of all events in game over screen, writes
        player's score to the highscore file,
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.write_highscore()
                    self.reset()
                    self.state = 'start'
                else:
                    self.change_name(event)

    def change_name_interface(self):
        """
        Displays the live name on the screen while changing it.
        """
        self.draw_text('Georgia Pro Black', 50, 'ENTER YOUR NAME:', YELLOW, 100, 250, True)
        self.draw_text('Georgia Pro Black', 50, self.name, YELLOW, 300, 300, True)

    def change_name(self, event):
        """
        Changes the name game attribute that is assigned to scored points.
        """
        if not len(self.name) > 8 or event.key == pygame.K_BACKSPACE:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[0:-1]
            else:
                self.name += event.unicode

    def reset(self):
        """
        Resets the coins, walls, player, ghosts position, loads a new map after
        lost game.
        """
        self.coins = []
        self.walls = []
        self.map = 1
        self.load_map()
        self.player.lives = 3
        self.player.score = 0
        self.player.rect = pygame.Rect(PLAYERS_STARTING_POSITION[0], PLAYERS_STARTING_POSITION[1], PLAYERS_WIDTH, PLAYERS_HEIGHT)
        for ghost in self.ghosts:
            ghost.normal_mode()
            ghost.rect = pygame.Rect(ghost.starting_pos[0], ghost.starting_pos[1], GHOST_WIDTH, GHOST_HEIGHT)

    def update_win_screen(self):
        """
        Takes care of all winning screen events, writes highscore.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.write_highscore()
                    self.reset()
                    self.state = 'start'
                else:
                    self.change_name(event)

    def display_win_screen(self):
        """"
        Displays the screen while its win state, writes text that informs user
        of game state and what to do next.
        """
        self.screen.fill(BLACK)
        self.draw_text('Georgia Pro Black', 100, 'YOU WON', BLUE, 100, 100, True)
        self.draw_text('Georgia Pro Black', 50, 'PUSH SPACE TO START AGAIN', GREEN, 100, 500, True)
        self.change_name_interface()
        pygame.display.update()

    def write_highscore(self):
        """
        If user added the name after the game saves it to highscores file.
        """
        if self.name:
            with open('saved/highscore.txt', 'a') as file_handle:
                writer = csv.DictWriter(file_handle, ['name', 'score'])
                writer.writerow({
                    'name': self.name,
                    'score': self.player.score
                })

    def read_highscore(self):
        """
        Reads highscores from highscores files, returns names list and scores list.
        """
        with open('saved/highscore.txt', 'r') as file_handle:
            reader = csv.DictReader(file_handle)
            names = []
            scores = []
            for row in reader:
                name = row['name']
                score = int(row['score'])
                names.append(name)
                scores.append(score)
            return names, scores

    def find_8_highscores(self):
        """
        Sorts highscores by from highest to lowest and returns list
        of tuples with name and score in it.
        """
        names, scores = self.read_highscore()
        scores_sorted = sorted(zip(scores, names), reverse=True)
        highscores = []
        try:
            for i in range(8):
                highscores.append(scores_sorted[i])
        except IndexError:
            pass
        return highscores

    def update_highscore_screen(self):
        """
        Takes care of all events that happen in highscore screen.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'start'

    def display_highscore_screen(self):
        """"
        Displays the screen while its highscore game mode, writes 8 best players
        to screen.
        """
        self.screen.fill(BLACK)
        highscores = self.find_8_highscores()
        i = 0
        for score in highscores:
            name = score[1]
            score = str(score[0])
            self.draw_text('Georgia Pro Black', 80, name, WHITE, 10, 80 + 80*i)
            self.draw_text('Georgia Pro Black', 80, score, YELLOW, 350, 80 + 80*i)
            self.draw_text('Georgia Pro Black', 100, 'HIGHSCORES', ORANGE, 10, 0, True)
            self.draw_text('Georgia Pro Black', 40, 'ESCAPE TO BACK', BLUE, 10, 690, True)
            i += 1
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
