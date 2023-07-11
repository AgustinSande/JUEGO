import pygame
import sys
from settings import *
from tile import Tile
from level import Level
from overworld import Overworld
from ui import UI
from button import Button

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))


class Game:
    
    def __init__(self) -> None:
        
        #game attributes
        self.max_level = 4
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        self.current_stamina = 99
        self.max_stamina = 100
        self.able_stamina_regen = True
        self.able_stamina_consume = True
        
        
        #audio
        self.volume_level = 0.25
        self.level_bg_music = pygame.mixer.Sound(".//JUEGO 2//audio//level_music.wav")
        self.level_bg_music.set_volume(self.volume_level)
        self.overworld_bg_music = pygame.mixer.Sound(".//JUEGO 2//audio//overworld_music.wav")
        self.overworld_bg_music.set_volume(self.volume_level)
        
        
        #score
        self.current_score = 0
        
        
        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level)
        self.overworld_bg_music.play(loops = -1)
        self.status = "overworld"

        #ui
        self.ui = UI(screen)
        
    
    def create_level (self, current_level):
        
        self.level = Level(screen, current_level, self.create_overworld, self.change_coins, self.change_health, self.change_stamina, self.change_score)
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)
        self.status = "level"

    def create_overworld (self, current_level, new_max_level):
        
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.current_health = 100
        self.coins = 0
        self.current_stamina = 99
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops = -1)
        self.status = "overworld"
    
    
    
    def change_coins(self, amount):
        self.coins += amount
    
    def change_health(self, amount):
        self.current_health += amount
    
    def change_stamina(self, amount):
        self.current_stamina += amount

    def change_volume(self, amount):
        self.volume_level += amount
    
    def change_score(self,amount):
        self.current_score += amount
    

    def check_game_over(self):
        if self.current_health <= 0: 
            
            self.current_health = 100
            self.coins = 0
            self.current_stamina = 99
            self.level_bg_music.stop()

            self.overworld = Overworld(0, self.max_level, screen, self.create_level)
            self.overworld_bg_music.play(loops = -1)
            self.status = "overworld"
    
    
    def check_stamina_status(self):
        if self.current_stamina <= 100 and self.current_stamina >= 0:
            self.able_stamina_regen = True
            self.able_stamina_consume = True  
        
    def check_stamina_regen(self):
        if self.current_stamina >= 100:
            self.able_stamina_regen = False
        else:
            self.able_stamina_regen = True
    
    def check_stamina_consume(self):
        if self.current_stamina <= 0:
            self.able_stamina_consume = False
        else:
            self.able_stamina_consume = True
    
    def check_health_restore(self):
        if self.current_health >= 100:
            self.current_health = 100
    def toggle_volume(self):
        
        if self.volume_level == 0:
            self.volume_level = 0.25
            self.overworld_bg_music.set_volume(self.volume_level)
            self.level_bg_music.set_volume(self.volume_level)
        
        else:
            self.volume_level = 0
            self.overworld_bg_music.set_volume(self.volume_level)
            self.level_bg_music.set_volume(self.volume_level)
    
    
    
    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run(self.able_stamina_consume, self.able_stamina_regen, self.change_health)

            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.ui.show_stamin(self.current_stamina, self.max_stamina)
            self.ui.show_score(self.current_score)
            self.ui.volume_button.draw()
            
            if self.ui.volume_button.detect_colliction():
                self.toggle_volume()
                
            self.check_stamina_status()
            self.check_stamina_regen()
            self.check_stamina_consume()
            self.check_health_restore()
            self.check_game_over()
            
            
            

         


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
    