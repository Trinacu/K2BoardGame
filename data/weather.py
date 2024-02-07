import pygame as pg
from copy import copy

class WeatherCard():
    def __init__(self, path, image, **kwargs):
        super().__init__()
        self.path = path

        self.clean_surf = image
        size = self.clean_surf.get_size()
        scale = 0.5
        size_hand = (size[0] * scale, size[1] * scale)
        self.clean_surf = pg.transform.scale(image, size_hand)
        self.surf = copy(self.clean_surf)
        self.rect = self.surf.get_rect()
        
        
        self.process_kwargs(kwargs)
    
    # idx=0 - day 1
    def set_day(self, idx):
        self.surf = copy(self.clean_surf)
        if idx > -1:
            pg.draw.circle(self.surf, (10,10,10), (70 + 123*idx, 39), 20, 0)
        
    
    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            "day1": {
                "below_6k"  : (0, 0),
                "6k_to_7k"  : (0, 0),
                "7k_to_8k"  : (0, 0),
                "above_8k"  : (0, 0)
            },
            "day2": {
                "below_6k"  : (0, 0),
                "6k_to_7k"  : (0, 0),
                "7k_to_8k"  : (0, 0),
                "above_8k"  : (0, 0)
            },
            "day3": {
                "below_6k"  : (0, 0),
                "6k_to_7k"  : (0, 0),
                "7k_to_8k"  : (0, 0),
                "above_8k"  : (0, 0)
            }
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)
