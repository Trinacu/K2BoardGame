import pygame as pg
from .. import tools, player, card, board, weather, graph, data, options
from ..GUI import button
import os
import random

class Game(tools.States):
    def __init__(self, screen_rect): 
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        #self.score_text, self.score_rect = self.make_text("SCOREBOARD_PLACEHOLDER",
        #    (255,255,255), (screen_rect.centerx,100), 50)
        #self.help_overlay_title, self.help_overlay_title_rect = self.make_text("help_overlay",
        #    (255,255,255), screen_rect.center, 50)
        #self.help_overlay_text, self.help_overlay_text_rect = self.make_text("help_overlay",
        #    (255,255,255), screen_rect.center, 50)
            
        
        self.deck = []
        self.weather_deck = []
        self.card_db = data.cards
        self.create_deck()
        
        self.bg_color = (25,25,25)
        self.card_inhand_width = self.deck[0].surf_hand.get_width()
        self.card_selected_offsetY = 40
        self.hand_offsetX = 25
        
        #self.bg = tools.Image.load('greenbg.png')
        #self.bg_rect = self.bg.get_rect()

        self.selected_node = None
        self.current_player = None
        self.selected_climber = None

        self.current_day = 1


        self.game_phases = ['card_selection', 'risk_tokens',
                            'action_phase', 'acclimatization_checks']

        self.current_game_phase = self.game_phases[0]
        
        button_config = {
            "hover_color"        : (100,255,100),
            "clicked_color"      : (255,255,255),
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (0,0,0),
            'font'               : tools.Font.load('impact.ttf', 24),
            'font_color'         : (0,0,0),
            'call_on_release'    : False
        }
        
        self.next_phase_button = button.Button((self.screen_rect[2]-200,self.screen_rect[3]/4,175,50),(100,200,100), 
            self.next_phase, text='Next Phase', **button_config
        )
        # caption=Play cards but changes according to phase in next_phase()
        self.done_button = button.Button((self.screen_rect[2]-200,self.screen_rect[3]/2,175,50),(100,200,100), 
            self.action_done, text='Play cards', **button_config
        )

        self.selection = button.SelectionList((100,100), (70, 25), (100,100,100), [])
        self.selection.enabled = False

        self.gui_elements = [self.next_phase_button, self.done_button, self.selection]

    def select_square_climber(self):
        self.selected_climber = self.current_player.climbers['square']

    def select_round_climber(self):
        self.selected_climber = self.current_player.climbers['round']

    def build_tent(self, node):
        print(f'trying to build a tent on node {node.name}')

    def update_day_title(self):
        text = f"Day {self.current_day}:"
        self.day_title, self.day_title_rect = tools.make_text(text, (255,255,255), (self.screen_rect.centerx+220, 250), 30, fonttype='impact.ttf')


    def next_phase(self):
        # after action phase, clear played_cards list
        if self.current_game_phase == 'action_phase':
            [p.played_cards.clear() for p in self.player_list]
        # LAST PHASE - get ready for next turn/day
        elif self.current_game_phase == 'acclimatization_checks':
            self.player_list.append(self.player_list.pop(0))
            # check for game end here? 18 turns?
            if len(self.current_player.deck) != 0:
                [player.draw_cards(3) for player in self.player_list]
            elif len(self.current_player.hand) == 0:
                [player.init_deck() for player in self.player_list]
                [player.draw_cards(6) for player in self.player_list]
            # TODO - weather advances 1 day forward
            self.current_day += 1
            self.update_day_title()
            self.update_weather()

            # TODO - remove this; just for testing
            #for card in self.player_list[0].hand[:3]:
            #    card.selected = True

            
        for i, phase in enumerate(self.game_phases):
            if phase == self.current_game_phase:
                ind = i + 1
                break

        self.current_game_phase = self.game_phases[ind%len(self.game_phases)]
        # button text?
        if self.current_game_phase == 'card_selection':
            self.done_button.text = 'Play cards'
            self.done_button.render_text()
        else:
            self.done_button.text = 'Done'
            self.done_button.render_text()


    def next_player(self):
        for i, player in enumerate(self.player_list):
            if player == self.player_list[i]:
                ind = i + 1
                break
        self.current_player = self.player_list[ind]

    def player_action_done(self):
        for i, player in enumerate(self.player_list):
            if player == self.current_player:
                ind = i + 1
                break
        if ind > len(self.player_list) - 1:
            ind = 0
            self.next_phase()
        
        self.current_player = self.player_list[ind]


    def action_done(self):
        if self.current_game_phase == 'card_selection':
            if self.current_player.play_selected_cards():
                self.player_action_done()
        elif self.current_game_phase == 'risk_tokens':
            self.player_action_done()
        elif self.current_game_phase == 'action_phase':
            self.player_action_done()
        elif self.current_game_phase == 'acclimatization_checks':
            self.player_action_done()


    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track]) 
            pg.mixer.music.play()
            
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_game_phase == 'card_selection':
                self.select_card_in_hand()
            elif self.current_game_phase == 'action_phase':
                self.select_card_on_table()
                for _, node in self.graph.nodes.items():
                    # clicked on node
                    if node.rect.collidepoint(pg.mouse.get_pos()):
                        print(f"{node.name} move: {node.move_cost}, accl: {node.accl_cost}, VP: {node.VP}, weather_penalty: {node.weather_penalty}")
                        # TODO - what if both climbers on same node? button selection?
                        # what about tent placement?
                        if (self.current_player.climbers['square'] in node.climber_list) and (self.current_player.climbers['round'] in node.climber_list):
                            # use the other thing (not lambda but something about function expression)
                            # because passing node here always results in node27 (last one)
                            self.selection.update_options([['square', self.select_square_climber],
                                                           ['round', self.select_round_climber],
                                                           ['tent', lambda:self.build_tent(node)]])

                        elif self.current_player.climbers['square'] in node.climber_list:
                            self.selected_climber = self.current_player.climbers['square']
                        elif self.current_player.climbers['round'] in node.climber_list:
                            self.selected_climber = self.current_player.climbers['round']
                            for node in self.selected_climber.reachable_nodes():
                                self.graph.nodes[node].set('highlighted', True)
                        else:
                            # TODO - try and move climber?
                            pass


        elif event.type == pg.KEYDOWN:
            if event.key == self.keybinding['back']:
                self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'

        for item in self.gui_elements:
            item.check_event(event)
                
    def select_card_on_table(self):
        sel = None
        for card in self.current_player.played_cards:
            # last card in hand has full hitbox, others only half
            if card == self.current_player.played_cards[-1]:
                if card.rect_table.collidepoint(pg.mouse.get_pos()):
                    sel = card
            else:
                half_width = int(card.rect_table[2]/2)
                if card.rect_table_half.collidepoint(pg.mouse.get_pos()):
                    sel = card
        # deselect all cards of different type - only want to move OR acclimatize
        if sel != None:
            sel.selected = not sel.selected
            if sel.move > 0:
                for c in self.current_player.played_cards:
                    if c.move == 0:
                        c.selected = False
            else:
                for c in self.current_player.played_cards:
                    if c.move > 0:
                        c.selected = False

            
    def select_card_in_hand(self):
       for card in self.current_player.hand:
            # last card in hand has full hitbox, others only half
            if card == self.current_player.hand[-1]:
                if card.rect_hand.collidepoint(pg.mouse.get_pos()):
                    if (sum(self.current_player.hand_selected()) < 3) or card.selected:
                        card.selected = not card.selected
            else:
                if card.rect_hand_half.collidepoint(pg.mouse.get_pos()):
                    if (sum(self.current_player.hand_selected()) < 3) or card.selected:
                        card.selected = not card.selected
                    

    def update(self, now, keys):
        if self.current_game_phase == 'card_selection':
            self.update_hand_position()

            if sum(self.current_player.hand_selected()) < 3:
                self.done_button.disabled = True
            else:
                self.done_button.disabled = False
        elif self.current_game_phase == 'risk_tokens':
            self.update_table_position()
        elif self.current_game_phase == 'action_phase':
            self.update_table_position()

            
    def render(self, screen):
        screen.fill(self.bg_color)
        #screen.blit(self.bg, self.bg_rect)
        screen.blit(self.board.surf, self.board.rect)
        
        for item in self.gui_elements:
            item.render(screen)

        
        screen.blit(self.day_title, self.day_title_rect)
        screen.blit(*self.game_phase_titles[self.current_game_phase])
        screen.blit(self.current_player.title_surf, (self.screen_rect.right-300,250))

        if self.current_game_phase == 'card_selection':
            for card in self.current_player.hand:
                screen.blit(card.surf_hand, (card.rect_hand.x, card.rect_hand.y))

        elif self.current_game_phase == 'risk_tokens' or self.current_game_phase == 'action_phase':
            for card in self.current_player.played_cards:
                screen.blit(card.surf_table, (card.rect_table.x, card.rect_table.y))
        
        for card in self.weather_deck[:2]:
            screen.blit(card.surf, card.rect)
            
        #for _, node in self.graph.nodes.items():
        #    pg.draw.circle(screen, (10,10,10), node.pos, 34, 4)
        
        # draw nodes highlights and climbers
        for _, n in self.graph.nodes.items():
            screen.blit(n.surf, (n.rect.x, n.rect.y))
            for i, climber in enumerate(n.climber_list):
                screen.blit(climber.surf, (n.rect.right - 17, n.rect.top + 5 + 17*i))

        # draw acclimatization display
        for i, player in enumerate(self.player_list):
            screen.blit(player.accl_surf, (720, 290+i*140))

    def update_weather(self):
        if (len(self.weather_deck) > 2) and ((self.current_day-1) % 3 == 0) and (self.current_day > 1):
            self.weather_deck.pop(0)
        if self.current_day < 16:
            self.current_weather = self.weather_deck[0]
        else:
            self.weather_deck[0].set_day(-1)
            self.current_weather = self.weather_deck[1]


        day = 'day' + str((self.current_day-1)%3 + 1)
        for _, node in self.graph.nodes.items():
            d = self.current_weather.__getattribute__(day)
            if node.altitude < 6000:
                node.weather_penalty = d['below_6k']
            elif node.altitude < 7000:
                node.weather_penalty = d['6k_to_7k']
            elif node.altitude < 8000:
                node.weather_penalty = d['7k_to_8k']
            elif node.altitude > 8000:
                node.weather_penalty = d['above_8k']

        # update display
        self.current_weather.set_day((self.current_day-1)%3)
        self.weather_deck[0].rect.x = self.board.rect[2]
        self.weather_deck[0].rect.y = 0
        self.weather_deck[1].rect.x = self.board.rect[2] + self.weather_deck[0].rect[2]
        self.weather_deck[1].rect.y = 0

    def update_table_position(self):
        for i, card in enumerate(self.current_player.played_cards):
            card.rect_table.y = self.screen_rect.bottom - card.rect_table[3]
            card.rect_table_half.y = card.rect_table.y
            if card.selected:
                card.rect_table.y -= self.card_selected_offsetY
            x = self.screen_rect[2] - 2*card.rect_table[2] + i * card.rect_table[2]/2
            card.rect_table.x = x
            card.rect_table_half.x = x

    def update_hand_position(self):
        hand_width = (((len(self.current_player.hand)-1)/2) + 1) * self.current_player.hand[0].rect_hand[2]
        for i, card in enumerate(self.current_player.hand):
            card.rect_hand.y = self.screen_rect.bottom - card.surf_hand.get_height()*2/3
            card.rect_hand_half.y = card.rect_hand.y
            if card.selected:
                card.rect_hand.y -= self.card_selected_offsetY
            card.rect_hand.x = self.screen_rect[2] - self.hand_offsetX - hand_width + i * card.rect_hand[2]/2
            card.rect_hand_half.x = card.rect_hand.x
            
    def create_deck(self):
        path = os.path.join(tools.Image.path, 'cards')
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith('.png'):
                    path = os.path.abspath(os.path.join(root, f))
                    image = pg.image.load(path)
                    filename = tools.get_filename(path)
                    for i in range(self.card_db[filename]['count']):
                        self.deck.append(card.Card(path, image, **self.card_db[filename]['effect']))
        #for c in self.deck:
        #    print('{} at {}'.format(c.path, c))
        #print(len(self.deck))

    def read_options(self):
        self.board_name = options.options['board']
        self.weather_name = options.options['weather']
        self.player_cnt = options.options['player_cnt']

    def load_graph(self):
        self.node_db = data.nodes[self.board_name]
        self.graph = graph.WeightedGraph(self.node_db)
        for _, node in self.graph.nodes.items():
            node.rect.centerx = node.pos[0]
            node.rect.centery = node.pos[1]
            #print(node.surf, node.rect)

    def load_board(self):
        path = os.path.join(tools.Image.path, 'boards')
        path = os.path.abspath(os.path.join(path, 'board_' + self.board_name + '.jpg'))
        image = pg.image.load(path)
        self.board = board.Board(path, image)

    def load_weather(self):
        self.weather_db = data.weather[self.weather_name]
        path = os.path.join(tools.Image.path, 'weather')
        for root, dirs, files in os.walk(path):
            for f in files:
                if (self.weather_name in f) and (f.endswith('.png')):
                    path = os.path.abspath(os.path.join(root, f))
                    image = pg.image.load(path)
                    filename = tools.get_filename(path)

                    self.weather_deck.append(weather.WeatherCard(path, image, **self.weather_db[filename.replace(self.weather_name+'_', '')]))
        random.shuffle(self.weather_deck)

            
    def cleanup(self):
        pass#pg.mixer.music.unpause()
        #pg.mixer.music.stop()
        #self.background_music.setup(self.background_music_volume)
        
    def entry(self):
        self.read_options()

        self.load_board()
        self.load_weather()
        self.load_graph()
        colors = [pg.color.THECOLORS['blue'], pg.color.THECOLORS['red'], pg.color.THECOLORS['green']]

        self.player_list = []
        self.player_titles = {}
        for i in range(self.player_cnt):
            name = f"Player{i}"
            p = player.Player(self.graph, name, colors[i], self.deck)
            self.player_list.append(p)
            # save just the surface [0], dont care about the rect, because we blit it at different loc
            self.player_titles[name] = tools.make_text(name, colors[i], (0,0), 20, fonttype='impact.ttf')[0]
            for _, c in p.climbers.items():
                c.update_accl_surf()
            p.update_accl_surf()
            

        self.game_phase_titles = {}
        for phase in self.game_phases:
            text = phase.replace('_', ' ')
            self.game_phase_titles[phase] = tools.make_text(text, (255,255,255), (self.screen_rect.centerx+350, 250), 30, fonttype='impact.ttf')

        [player.draw_cards(6) for player in self.player_list]

        self.current_player = self.player_list[0]
        

        self.update_day_title()

        self.update_weather()

        #pg.mixer.music.pause()
        #pg.mixer.music.play()
