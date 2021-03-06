"""
PLAN

Create a several stations and have an agent automatically work at/between them
- Mine
- Refinery
- Store

Have the agent mine ore, refine it and sell it for gold. Then repeat.

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

        # Triggers when the player reaches 100% progress
        if self.progress > 99:
            player.inventory['copper_ore'] += 1
            self.progress = 0
            print("Successfully mined some copper ore")
            print("Player now has {} copper ore".format(player.inventory['copper_ore']))
        else:
            self.progress += self.mine_rate
            time.sleep(0.5)
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

    def station_refine_ore(self, player):

        if self.progress > 99:
            player.inventory['copper_bar'] += 1
            self.progress = 0
            print("Successfully refined a copper bar")
            print("Player now has {} copper bar(s)".format(player.inventory['copper_bar']))
        else:
            self.progress += self.refine_rate
            time.sleep(0.5)
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

    def define_action(self):
        if self.inventory['copper_ore'] > 3:
            self.action = 'Refine Ore'
        if self.inventory['copper_bar'] > 3 and self.inventory == 0:
            self.action = 'Sell Goods'
        if self.inventory['copper_ore'] == 0 and self.inventory['copper_bar'] == 0:
            self.action = 'Mine Ore'

    def take_action(self, station_list):
        if self.action == 'Mine Ore':
            mine = self.locate_mine(station_list)
            self.player_mine_ore(mine)

        if self.action == 'Refine Ore':
            refinery = self.locate_refinery(station_list)
            self.player_refine_ore(refinery)

        if self.action == 'Sell Goods':
            store = self.locate_store(station_list)
            self.player_mine_ore(store)

    def locate_mine(self, station_list):
        return station_list['mines'][0]

    def locate_refinery(self, station_list):
        return station_list['refineries'][0]

    def locate_store(self, station_list):
        return station_list['stores'][0]

    def player_mine_ore(self, mine):
        # move to the mine, if close enough start to mine
        close_enough = True
        if close_enough:
            mine.station_mine_ore(self)

    def player_refine_ore(self, refinery):
        # move to the mine, if close enough start to mine
        close_enough = True
        if close_enough:
            refinery.station_refine_ore(self)

    def player_sell_goods(self, store):
        # move to the mine, if close enough start to mine
        close_enough = True
        if close_enough:
            store.station_sell_goods(self)


def draw_game(display, station_list, player_list):

    display.fill(BLACK)

    for stations in station_list:
        for station in stations:
            station.draw(display)

    for player in player_list:
        player.draw(display)


# Initialise game window
pygame.init()
pygame.display.set_caption('Mine, Refine, Sell')
frame_size_x = 400
frame_size_y = 400
game_window = pygame.display.set_mode([frame_size_x, frame_size_y])

fps = pygame.time.Clock()
render_gfx = True

# --- Main --- #
my_player = Player(10, 10, 1)
copper_mine = Mine(150, 10, mine_rate=5, ore='Copper Ore')
copper_refinery = Refinery(120, 100, refine_rate=5)
copper_store = Store(20, 120)

players = [my_player]
stations = {'mines': [copper_mine],
            'refineries': [copper_refinery],
            'stores': [copper_store]}

# Game loop starts here
while render_gfx:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    """
    player defines his action
    player takes his action
    game loop continues and repeats
    """

    my_player.define_action()
    my_player.take_action(stations)

    if my_player.gold > 10:
        print('Player final gold value: {}'.format(my_player.gold))
        pygame.quit()

    draw_game(game_window, stations.values(), players)
    pygame.display.flip()
    fps.tick(30)  # FPS

pygame.quit()
