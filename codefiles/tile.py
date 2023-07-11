import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x,y) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        
        self.rect = self.image.get_rect(topleft = (x,y))

    
    def update(self, x_shift):
        self.rect.x += x_shift
        
        
class StaticTile(Tile):
    def __init__(self, size, x, y, surface) -> None:
        super().__init__(size, x,y)
        self.image = surface
        
class Crate(StaticTile):
    def __init__(self, size, x, y) -> None:
        super().__init__(size, x, y, pygame.image.load(".//JUEGO 2//graphics//terrain//crate.png").convert_alpha())
        offset_y  = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class Orange(StaticTile):
    def __init__(self, size, x, y) -> None:
        super().__init__(size, x, y, pygame.image.load(".//JUEGO 2//graphics//food//orange.png").convert_alpha())
        #self.rect = self.image.get_rect()
class Apple(StaticTile):
    def __init__(self, size, x, y) -> None:
        super().__init__(size, x, y, pygame.image.load(".//JUEGO 2//graphics//food//apple.png").convert_alpha())
     
class Banana(StaticTile):
    def __init__(self, size, x, y) -> None:
        
        super().__init__(size, x, y, pygame.transform.scale(pygame.image.load(".//JUEGO 2//graphics//food//banana.png").convert_alpha(), (size/2,size/2)))
        
        
class AnimatedTile(Tile):
    def __init__(self, size, x, y, path) -> None:
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
    def update(self,x_shift):
        self.animate()
        self.rect.x += x_shift
        
        
class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, value) -> None:
        super().__init__(size, x, y, path)
        center_x = x + int(size/2) 
        center_y = y + int(size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.value = value
        
class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset) -> None:
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x,offset_y)
        

        