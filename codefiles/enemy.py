import pygame
from tile import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    def __init__(self, size, x, y ) -> None:
        super().__init__(size, x, y, ".//JUEGO 2//graphics//enemy//run")
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2,4)
        self.direction = "right"
        
        
    def move(self):
        if self.direction == "right":
            
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        
    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            
            
    def reverse_speed(self):
        self.speed *= -1

          
    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        