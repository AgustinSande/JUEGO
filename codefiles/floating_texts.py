import pygame


class FloatingText():
    def __init__(self, text : str, position,display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font(".//JUEGO 2//graphics//ui//ARCADEPI.TTF", 16) 
        self.text = text
        self.text_surface = self.font.render(text, True, (100, 14, 14))
        self.text_rect = self.text_surface.get_rect()  
        self.text_rect.center = (position)
        #self.timer = 100  
    
    # def update(self):
    #     self.timer -= 1
    #     if self.timer <= 0:
    #         self.kill() 
            
    def show_text(self):
        
        self.display_surface.blit(self.text_surface, self.text_rect)