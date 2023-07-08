import pygame
import sys
from settings import *
from tile import Tile
from level import Level
from overworld import Overworld
from ui import UI

class Game:
    
    def __init__(self) -> None:
        
        #game attributes
        self.max_level = 4
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        
        #audio
        self.level_bg_music = pygame.mixer.Sound(".//JUEGO 2//audio//level_music.wav")
        self.level_bg_music.set_volume(0.25)
        self.overworld_bg_music = pygame.mixer.Sound(".//JUEGO 2//audio//overworld_music.wav")
        self.overworld_bg_music.set_volume(0.25)
        
        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.overworld_bg_music.play(loops = -1)
        self.status = "overworld"

        self.ui = UI(screen)
        
    
    def create_level (self, current_level):
        
        self.level = Level(screen, current_level, self.create_overworld, self.change_coins, self.change_health)
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)
        self.status = "level"

    def create_overworld (self, current_level, new_max_level):
        
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.current_health = 100
        self.coins = 0
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops = -1)
        self.status = "overworld"
    
    def change_coins(self, amount):
        self.coins += amount
    
    def change_health(self, amount):
        self.current_health += amount
        
    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.level_bg_music.stop()
            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.overworld_bg_music.play(loops = -1)
            self.status = "overworld"
            
    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

         
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

game = Game()

while True: 
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
             pygame.quit()
             sys.exit()
             
    screen.fill(C_WHITE)
    
    
    game.run()
    
    pygame.display.flip()
    
    delta_ms = clock.tick(FPS)