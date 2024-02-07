from .climber import Climber
from copy import copy
from random import shuffle
from . import tools
import pygame as pg

class Player():
    def __init__(self, graph, name, color, deck):
        self.name = name
        self.color = color
        self.climbers = {'round': Climber(self, graph, 'round'),
                         'square': Climber(self, graph, 'square')}
        self.hand = []
        self.played_cards = []

        self.full_deck = deck
        self.init_deck()

        self.accl_surf = pg.Surface((300, 120))
        self.title_surf = tools.make_text(name, self.color, (0,0), 20, fonttype='impact.ttf')[0]

    def draw_cards(self, cnt):
        [self.hand.append(self.deck.pop()) for _ in range(cnt)]

    def init_deck(self):
        self.deck = copy(self.full_deck)
        shuffle(self.deck)

    def hand_selected(self):
        return [c.selected for c in self.hand]
    
    def selected_cards(self):
        return [card for idx, card in enumerate(self.hand) if self.hand_selected()[idx]]

    def play_selected_cards(self):
        if sum(self.hand_selected()) != 3:
            return False
        [self.played_cards.append(self.hand[idx]) for idx, selected in enumerate(self.hand_selected()) if selected]
        [self.hand.remove(card) for card in self.selected_cards()]
        for c in self.played_cards:
            c.selected = False
        return True

    def update_accl_surf(self):
        self.accl_surf.fill((177,177,177))
        x = 10
        y = 10
        self.accl_surf.blit(self.title_surf, (x, y))
        for idx, climber_name in enumerate(self.climbers):
            climber = self.climbers[climber_name]
            self.accl_surf.blit(climber.surf, (x+20, y+(idx+1)*40))
            self.accl_surf.blit(climber.accl_surf, (x+40, y+(1+idx)*40 - (climber.accl_surf.get_height() - climber.surf.get_height())/2))
