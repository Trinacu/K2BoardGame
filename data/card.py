import pygame as pg

class Card:
    def __init__(self, path, image, **kwargs):
        self.surf = image
        size = self.surf.get_size()
        scale = 0.6
        size_hand = (size[0] * scale, size[1] * scale)
        self.surf_hand = pg.transform.scale(image, size_hand)
        scale = 0.4
        size_table = (size[0] * scale, size[1] * scale)
        self.surf_table = pg.transform.scale(image, size_table)
        
        self.path = path
        self.rect = self.surf.get_rect()
        self.rect_hand = self.surf_hand.get_rect()
        self.rect_table = self.surf_table.get_rect()
        
        half_width = int(self.rect_hand[2]/2)
        self.rect_hand_half = self.rect_hand.inflate(-half_width, 0)
        half_width = int(self.rect_table[2]/2)
        self.rect_table_half = self.rect_table.inflate(-half_width, 0)

        self.selected = False
        
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            "move"      : 0,
            "move_down" : 0,
            "accl"      : 0,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def __repr__(self):
        if self.move > 0:
            if self.move_down > 0:
                return f"Move {self.move}|{self.move_down}"
            else:
                return f"Move {self.move}"
        else:
            return f"Acclimatize {self.accl}"

