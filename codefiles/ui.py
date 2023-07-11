import pygame
from settings import *
from button import Button
class UI:
    def __init__(self, surface) -> None:
        
        #setup
        self.display_surface = surface
        
        #health
        self.health_bar = pygame.image.load(".//JUEGO 2//graphics//ui//health_bar.png").convert_alpha()
        self.health_bar_topleft = (54,39)
        self.bar_max_width = 152
        self.bar_heigth = 4
        
        
        #stamina
        self.stamina_bar = pygame.image.load(".//JUEGO 2//graphics//ui//stamina_bar.png").convert_alpha()
        self.stamina_bar = pygame.transform.scale(self.stamina_bar, (215,30))
        self.stamina_bar_topleft = (54,69)
        self.stamina_max_width = 152
        self.stamina_height = 12
        
        #coins
        self.coin = pygame.image.load(".//JUEGO 2//graphics//ui//coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50,111))
        
        #font
        self.font = pygame.font.Font(".//JUEGO 2//graphics//ui//ARCADEPI.TTF", 30)
        
        #score
        self.score = pygame.image.load(".//JUEGO 2//graphics//ui//score.png")
        self.score = pygame.transform.scale(self.score, (200, 90))
        self.score_rect = self.score.get_rect(topleft = (700,0))
        
        #volume
        self.volume_button = Button((1560,10), self.display_surface,".//JUEGO 2//graphics//ui//volume_on.png")
       
        
    def show_health(self, current_health, max_health):
        self.display_surface.blit(self.health_bar, (20,10))
        current_health_ratio = current_health / max_health
        
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect((self.health_bar_topleft), (current_bar_width,self.bar_heigth))
        pygame.draw.rect(self.display_surface, C_DEEP_RED, health_bar_rect)
        
    def show_stamin(self, current_stamina, max_stamina):
        self.display_surface.blit(self.stamina_bar, (5,60))
        current_stamina_ratio = current_stamina / max_stamina
        current_stamina_width = self.stamina_max_width * current_stamina_ratio
        stamina_bar_rect = pygame.Rect((self.stamina_bar_topleft),(current_stamina_width, self.stamina_height))
        pygame.draw.rect(self.display_surface, C_BLUE_2, stamina_bar_rect)
        
    def show_coins(self, amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surface = self.font.render(str(amount), False, C_PURPLE)
        coin_amount_rect = coin_amount_surface.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surface, coin_amount_rect)

    
    def show_score(self, amount):
        self.display_surface.blit(self.score, self.score_rect)
        score_amount_surface = self.font.render(str(amount), False, C_PURPLE)
        score_amount_rect = score_amount_surface.get_rect(midleft = (self.score_rect.right -110, self.score_rect.centery))
        self.display_surface.blit(score_amount_surface, score_amount_rect)
    
    
     
            