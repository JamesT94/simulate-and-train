"""
Info?
"""

import pygame
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Mine(object):
    def __init__(self, x, y, mine_rate, ore):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.mine_rate = mine_rate
        self.ore = ore
        self.progress = 0

    def station_mine_ore(self, player):

        if self.progress > 0.99:
            player.inventory['copper_ore'] += 1
            self.progress = 0
            print("Successfully mined some copper ore")
            print("Player now has {} copper ore".format(player.inventory['copper_ore']))
        else:
            self.progress += self.mine_rate
            time.sleep(0.2)
            print('Mining Progress: {}'.format(self.progress))

    def draw(self, display):
        pygame.draw.rect(display, RED, (self.x, self.y, self.width, self.height))


class Refinery(object):
    def __init__(self, x, y, refine_rate):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.refine_rate = refine_rate
        self.progress = 0

    def station_refine_ore(self, ore, player):

        if self.progress > 0.99:
            player.inventory['copper_bar'] += 1
            self.progress = 0
            print("Successfully refined a copper bar")
            print("Player now has {} copper bar(s)".format(player.inventory['copper_bar']))
        else:
            self.progress += self.refine_rate
            time.sleep(0.2)
            print('Refining Progress: {}'.format(self.progress))

    def draw(self, display):
        pygame.draw.rect(display, BLUE, (self.x, self.y, self.width, self.height))


class Store(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20

    def station_sell_goods(self, player):
        gold = 0
        for i in range(player.inventory['copper_bar']):
            gold += 1
            print('Sold a copper bar')
        player.inventory['copper_bar'] = 0
        player.gold += gold

    def draw(self, display):
        pygame.draw.rect(display, GREEN, (self.x, self.y, self.width, self.height))


class Player(object):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = speed
        self.inventory = {'copper_ore': 0,
                          'copper_bar': 0}
        self.gold = 0
        self.action = 'Mine Ore'

    def draw(self, display):
        pygame.draw.circle(display, WHITE, (self.x, self.y), self.radius)

    def player_mine_ore(self, mine):
        # move to the mine, if close enough start to mine
        close_enough = True
        if close_enough:
            mine.station_mine_ore(self)

    def player_refine_ore(self, refinery):
        # move to the mine, if close enough start to mine
        close_enough = False
        if close_enough:
            refinery.station_refine_ore(self)

    def player_sell_goods(self, store):
        # move to the mine, if close enough start to mine
        close_enough = False
        if close_enough:
            store.station_sell_goods(self)


def draw_game(display, station_list, player_list):

    display.fill(BLACK)

    for station in station_list:
        station.draw(display)

    for player in player_list:
        player.draw(display)

    pygame.display.update()


# Initialise game window
pygame.display.set_caption('Mine, Refine, Sell')
frame_size_x = 200
frame_size_y = 200
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

fps = pygame.time.Clock()
render_gfx = True

# --- Main --- #
my_player = Player(10, 10, 1)
copper_mine = Mine(150, 10, 0.01, 'Copper Ore')
copper_refinery = Refinery(120, 100, 0.02)
copper_store = Store(20, 120)

players = [my_player]
stations = [copper_mine, copper_refinery, copper_store]

# Game Loop Starts Here
while render_gfx:
    fps.tick(2)
    draw_game(game_window, stations, players)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    while my_player.action == 'Mine Ore':
        my_player.player_mine_ore(copper_mine)

    my_player.action = 'Refine Ore'
    while my_player.action == 'Refine Ore':
        my_player.player_refine_ore(copper_refinery)

    my_player.action = 'Sell Goods'
    while my_player.action == 'Sell Goods':
        my_player.player_sell_goods(copper_store)

    print('Player final gold value: {}'.format(my_player.gold))
