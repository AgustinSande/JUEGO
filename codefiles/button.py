import pygame

class Button:
    def __init__(self, pos, display_surface, path) -> None:
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.display_surface = display_surface
        
        
        
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_lenght = 500
        
    def draw(self):
        
       
        self.display_surface.blit(self.image, self.rect)
        
    
    
    
                
    
    
                        
    def detect_colliction(self):
        
        print(self.allow_input)
        self.pos = pygame.mouse.get_pos()
        pressed = False
        if self.rect.collidepoint((self.pos)):
            if pygame.mouse.get_pressed()[0]:
                pressed = True
                
        return pressed