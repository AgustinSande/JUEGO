import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction) -> None:
        super().__init__()
        self.sprite = pygame.sprite.Sprite()
        self.speed = 10
        self.image = pygame.image.load("..//JUEGO 2//graphics//enemy//bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.direction = direction
        
        