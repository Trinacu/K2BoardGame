

import pygame as pg
from .. import tools, data
from ..GUI import button
import os

from .. card import Card #States.set_cards()

import re
# for sorting cards
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


class Viewer(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.options = ['Back']
        self.next_list = ['MENU']
        self.title, self.title_rect = tools.make_text('Card Viewer', self.title_color, (self.screen_rect.centerx, 75), 150)
        
        self.pre_render_options()
        self.from_bottom = 550
        self.spacer = 75
        self.card_offsetY = 55
        
        self.card_db = data.cards
        
        self.create_deck()
        self.update_image(0)
        
        button_config = {
            "hover_color"        : (150,150,150),
            "clicked_color"      : (255,255,255),
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (0,0,0),
            'font'               : tools.Font.load('impact.ttf', 12)
        }
        self.next_button = button.Button((self.screen_rect.centerx+150,190,100,25),(100,100,100), 
            lambda x=1:self.switch_card(x), text='Next', **button_config
        )
        self.prev_button = button.Button((self.screen_rect.centerx-250,190,100,25),(100,100,100), 
            lambda x=-1:self.switch_card(x), text='Previous', **button_config
        )
    def callback_test(self):
        print('callback')
        
    def update_category(self, text):
        self.category, self.category_rect = tools.make_text(text, (255,255,255), (self.screen_rect.centerx, 250), 15, fonttype='impact.ttf')
        
    def update_image(self, val):
        self.image = self.cards[val].surf
        self.image_rect = self.image.get_rect(centerx=self.screen_rect.centerx-500, centery=self.screen_rect.centery + self.card_offsetY)
        self.path = self.cards[val].path
        category = tools.get_category(self.path)
        self.update_category(category.title())
        
    def switch_card(self, num):
        for i, obj in enumerate(self.cards):
            if obj.surf == self.image:
                ind = i
        ind += num
        if ind < 0:
            ind = len(self.cards)-1
        elif ind > len(self.cards)-1:
            ind = 0
            
        self.update_image(ind)
        self.button_sound.sound.play()

    def get_event(self, event, keys):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key in self.keybinding['left']:
                self.switch_card(-1)
            elif event.key in self.keybinding['right']:
                self.switch_card(1)
            
            elif event.key in self.keybinding['up']:
                self.change_selected_option(-1)
            elif event.key in self.keybinding['down']:
                self.change_selected_option(1)
                
            elif event.key == self.keybinding['select']:
                self.select_option(self.selected_index)
            elif event.key == self.keybinding['back']:
                self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'
        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track]) 
            pg.mixer.music.play()
        self.mouse_menu_click(event)
        self.next_button.check_event(event)
        self.prev_button.check_event(event)

    def update(self, now, keys):
        pg.mouse.set_visible(True)
        self.mouse_hover_sound()
        self.change_selected_option()
        
        filename = tools.get_filename(self.path)
        self.help_overlay_title, self.help_overlay_title_rect = tools.make_text(filename.title(),
            (255,255,255), (self.screen_rect.centerx, 200), 60, fonttype='impact.ttf')
        
        string = self.card_db[filename]['info']
        my_font = tools.Font.load('impact.ttf', 20)
        self.help_overlay_text_rect = pg.Rect((425, 350, 300, 300))
        self.help_overlay_text = tools.render_textrect(string, my_font, self.help_overlay_text_rect, (216, 216, 216), self.bg_color, 0)
        
        string2 = '\n'.join([f"{k}: {v}" for (k,v) in self.card_db[filename]['effect'].items()])
        my_font = tools.Font.load('impact.ttf', 20)
        self.help_overlay_text2_rect = pg.Rect((425, 450, 300, 300))
        self.help_overlay_text2 = tools.render_textrect(string2, my_font, self.help_overlay_text2_rect, (216, 216, 216), self.bg_color, 0)

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.title,self.title_rect)
        screen.blit(self.category, self.category_rect)
        screen.blit(self.image ,self.image_rect)
        screen.blit(self.help_overlay_title, self.help_overlay_title_rect)
        screen.blit(self.help_overlay_text, self.help_overlay_text_rect)
        screen.blit(self.help_overlay_text2, self.help_overlay_text2_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screen_rect.centerx, self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])
        self.next_button.render(screen)
        self.prev_button.render(screen)
        
    def create_deck(self):
        self.cards = []
        path = os.path.join(tools.Image.path, 'cards')
        for root, dirs, files in os.walk(path):
            files.sort(key=natural_keys)
            for f in files:
                if f.endswith('.png') and 'backside' not in f:
                    path = os.path.abspath(os.path.join(root, f))
                    image = pg.image.load(path)
                    self.cards.append(Card(path, image, **self.card_db[tools.get_filename(f)]['effect']))
                    
    def cleanup(self):
        pg.display.set_caption("Boom")
        
    def entry(self):
        pass
