

import pygame as pg
from .. import tools, data, options
from ..GUI import button
import os

from .. board import Board

from copy import copy

class Options(tools.States):
    def __init__(self, screen_rect):
        tools.States.__init__(self)
        self.screen_rect = screen_rect
        self.options = ['Save and exit', 'Back']
        self.next_list = ['MENU', 'MENU']
        self.title, self.title_rect = tools.make_text('Options', self.title_color, (self.screen_rect.centerx, 75), 150)
        
        self.pre_render_options()
        self.from_bottom = 550
        self.spacer = 75
        self.board_offsetY = 0
        
        self.load_images()

        button_config = {
            "hover_color"        : (150,150,150),
            "clicked_color"      : (255,255,255),
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (0,0,0),
            'font'               : tools.Font.load('impact.ttf', 12)
        }
        self.next_board_button = button.Button((self.screen_rect.centerx+100,150,100,25),(100,100,100), 
            lambda x=1:self.switch_board(x), text='Next', **button_config
        )
        self.prev_board_button = button.Button((self.screen_rect.centerx-200,150,100,25),(100,100,100), 
            lambda x=-1:self.switch_board(x), text='Previous', **button_config
        )
        button_config = {
            "hover_color"        : (150,150,150),
            "clicked_color"      : (255,255,255),
            "clicked_font_color" : (0,0,0),
            "hover_font_color"   : (0,0,0),
            'font'               : tools.Font.load('impact.ttf', 16),
            'disabled'           : True
        }
        self.save_options_button = button.Button((self.screen_rect[2]-300,self.screen_rect[3]-200,150,40),(100,100,100), 
            self.save_options, text='Save options', **button_config
        )
    def callback_test(self):
        print('callback')

    def read_options(self):
        self.options = options.options
        self.old_options = copy(self.options)

    def save_options(self):
        with open('data/options.py', 'w') as f:
            f.write('options = ' + str(self.options))

        self.old_options = copy(self.options)
        self.enable_save_button()


    def update_board_title(self, text):
        self.board_title, self.board_title_rect = tools.make_text(text, (255,255,255), (self.board_image_rect.centerx, self.screen_rect[3] - self.board_image.get_height() - 30), 15, fonttype='impact.ttf')
        
    def update_board_image(self, val):
        for i, obj in enumerate(self.boards):
            if tools.get_filename(obj.path)[6:] == val:
                ind = i
        self.board_image = self.boards[ind].surf
        self.board_image_rect = self.board_image.get_rect(x=0, y=self.screen_rect[3] - self.board_image.get_height())
        #self.path = self.boards[ind].path
        
        board_title = val[0].upper() + val[1:]
        self.update_board_title(board_title)

    def enable_save_button(self):
        if self.old_options != self.options:
            self.save_options_button.disabled = False
        else:
            self.save_options_button.disabled = True


    def switch_board(self, num):
        for i, obj in enumerate(self.boards):
            if obj.surf == self.board_image:
                ind = i
        ind += num
        if ind < 0:
            ind = len(self.boards)-1
        elif ind > len(self.boards)-1:
            ind = 0

        name = tools.get_filename(self.boards[ind].path)[6:]
        self.options['board'] = name
        self.update_board_image(name)
        self.button_sound.sound.play()
        
        self.enable_save_button()

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
                self.switch_board(-1)
            elif event.key in self.keybinding['right']:
                self.switch_board(1)
            
            elif event.key in self.keybinding['up']:
                self.change_selected_option(-1)
            elif event.key in self.keybinding['down']:
                self.change_selected_option(1)
                
            elif event.key == self.keybinding['select']:
                if self.selected_index != len(self.next_list) - 1:
                    self.save_options()
                self.select_option(self.selected_index)

            if event.key == self.keybinding['back']:
                self.button_sound.sound.play()
                self.done = True
                self.next = 'MENU'

        elif event.type == self.background_music.track_end:
            self.background_music.track = (self.background_music.track+1) % len(self.background_music.tracks)
            pg.mixer.music.load(self.background_music.tracks[self.background_music.track]) 
            pg.mixer.music.play()
        self.mouse_menu_click(event)
        self.next_board_button.check_event(event)
        self.prev_board_button.check_event(event)
        self.save_options_button.check_event(event)

    def update(self, now, keys):
        pg.mouse.set_visible(True)
        self.mouse_hover_sound()
        self.change_selected_option()
        '''
        filename = tools.get_filename(self.path)
        self.help_overlay_title, self.help_overlay_title_rect = tools.make_text(filename.title(),
            (255,255,255), (self.screen_rect.centerx, 100), 60, fonttype='impact.ttf')
        
        string = self.database[filename]['info']
        my_font = tools.Font.load('impact.ttf', 20)
        self.help_overlay_text_rect = pg.Rect((425, 200, 300, 300))
        self.help_overlay_text = tools.render_textrect(string, my_font, self.help_overlay_text_rect, (216, 216, 216), self.bg_color, 0)
        '''

    def render(self, screen):
        screen.fill(self.bg_color)
        screen.blit(self.title,self.title_rect)
        screen.blit(self.board_title, self.board_title_rect)
        screen.blit(self.board_image ,self.board_image_rect)
        #screen.blit(self.help_overlay_title, self.help_overlay_title_rect)
        #screen.blit(self.help_overlay_text, self.help_overlay_text_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (self.screen_rect.centerx, self.from_bottom+i*self.spacer)
            if i == self.selected_index:
                rend_img,rend_rect = self.rendered["sel"][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img,rend_rect)
            else:
                screen.blit(opt[0],opt[1])
        self.next_board_button.render(screen)
        self.prev_board_button.render(screen)
        self.save_options_button.render(screen)
        
    def load_images(self):
        self.boards = []
        path = os.path.join(tools.Image.path, 'boards')
        for root, dirs, files in os.walk(path):
            for f in sorted(files):
                if f.endswith('.jpg'):
                    path = os.path.abspath(os.path.join(root, f))
                    image = pg.image.load(path)
                    # scale down
                    scale = 0.8
                    size = image.get_size()
                    size = (size[0] * scale, size[1] * scale)
                    image = pg.transform.scale(image, size)
                    self.boards.append(Board(path, image))
        
        # also load weather images to prepare for showing and selections

    def cleanup(self):
        pg.display.set_caption("Boom")
        
    def entry(self):
        self.read_options()

        self.update_board_image(self.options['board'])
        
