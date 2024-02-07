class Board:
    def __init__(self, path, image):
        self.surf = image
        self.rect = self.surf.get_rect()
        self.path = path
