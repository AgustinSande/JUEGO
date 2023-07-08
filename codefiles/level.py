import pygame
from tile import Tile, StaticTile, Crate, Coin, Palm
from settings import *
from player import Player
from particles import ParticleEffect
from support import *
from enemy import Enemy
from decoration import Sky, Water, Cloud
from game_data import levels

import os
current_directory = os.getcwd()
print("Current directory:", current_directory)

class Level():
    #, level_data
    def __init__(self, surface, current_level, create_overworld, change_coins, change_health):

        #level setup
        self.display_surface = surface
        level_data = levels[current_level]
        self.new_max_level = level_data["unlock"]
        
        #audio
        self.coin_sound = pygame.mixer.Sound(".//JUEGO 2//audio//effects//coin.wav")
        self.coin_sound.set_volume(0.25)
        self.stomp_sound = pygame.mixer.Sound(".//JUEGO 2//audio//effects//stomp.wav")
        self.stomp_sound.set_volume(0.25)
        #overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        
        #self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = None
        
        
        
        #player setup
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        
        #ui
        self.change_coins = change_coins
        
        
        #terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")
        
        
        #grass setup 
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")
        
        
        #crates
        crate_layout = import_csv_layout(level_data["crate"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crate")
        
        #coins 
        coins_layout = import_csv_layout(level_data["coins"])
        self.coins_sprites = self.create_tile_group(coins_layout, "coins")
        
        #fg_palm
        fg_palm_layout = import_csv_layout(level_data["fg_palm"])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, "fg_palm")
        
        #bg_palm
        bg_palm_layout = import_csv_layout(level_data["bg_palm"])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, "bg_palm")
        
        #enemy 
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")
        
        #constrain
        contrain_layout = import_csv_layout(level_data["constrains"])
        self.constrain_sprites = self.create_tile_group(contrain_layout, "constrains")
        
        
        #decoration 
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(ALTO_VENTANA - 24, level_width)
        self.clouds = Cloud(400, level_width, 60)
        
        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        self.explosion_sprite = pygame.sprite.Group()
        
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index , row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != "-1":
                    x  = column_index * tile_size
                    y = row_index * tile_size
                    
                    if type == "terrain": 
                        terrain_tile_list = import_cut_graphics(".//JUEGO 2//graphics//terrain//terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y , tile_surface)
                       
                    if type == "grass":
                        
                        grass_tile_list = import_cut_graphics(".//JUEGO 2//graphics//decoration//grass//grass.png")
                        tile_surface = grass_tile_list[int(value)]
                        sprite = StaticTile(tile_size,x,y, tile_surface)
                    
                    if type == "crate":
                        sprite = Crate(tile_size, x , y)
                    if type == "coins":
                        if value == "0":
                            sprite = Coin(tile_size, x,y,".//JUEGO 2//graphics//coins//gold",5 )
                        if value == "1":
                            sprite = Coin(tile_size, x,y, ".//JUEGO 2//graphics//coins//silver",1)
                            
                    if type == "fg_palm":
                        if value == "0":
                            sprite = Palm(tile_size, x, y, ".//JUEGO 2//graphics//terrain//palm_small",38)     
                        if value == "1":
                            sprite = Palm(tile_size, x, y, ".//JUEGO 2//graphics//terrain//palm_large",64)
                    if type =="bg_palm":
                        sprite = Palm(tile_size, x, y, ".//JUEGO 2//graphics//terrain//palm_bg",64)
                    
                    if type == "enemies":
                        sprite = Enemy(tile_size, x,y)
                    
                    if type == "constrains":
                        sprite = Tile(tile_size, x,y)
                    sprite_group.add(sprite)   
        return sprite_group

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,"jump")
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()


        for row_index, row in enumerate(layout):
            for column_index, cell in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if cell == "X":

                    tile = Tile((x,y),tile_size)
                    self.tiles.add(tile)

                if cell == "P":
                        
                    player_sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < ANCHO_VENTANA/4 and direction_x < 0:
            self.world_shift  = 8
            player.speed = 0
        elif player_x > ANCHO_VENTANA - ANCHO_VENTANA/4 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player =self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidible_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidible_sprites :
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x  = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x  = player.rect.right


        

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidible_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidible_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y  = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y  = 0
                    player.on_ceiling = True


        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

        

    
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            
            if pygame.sprite.spritecollide(enemy, self.constrain_sprites, False):
                enemy.reverse_speed()
    
    def player_setup(self, layout, change_health):
        for row_index , row in enumerate(layout):
            for column_index, value in enumerate(row):
                x  = column_index * tile_size
                y = row_index * tile_size
                if value == "0":
                    sprite = Player((x,y), self.display_surface, self.create_jump_particles, change_health )
                    self.player.add(sprite)
                if value == "1":
                    hat_surface = pygame.image.load(".//JUEGO 2//graphics//character//hat.png").convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)
    
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_BACKSPACE]:
            self.create_overworld(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)
    
    def check_death(self):
        if self.player.sprite.rect.top  > ALTO_VENTANA:
            self.create_overworld(self.current_level, 0)
            
        
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)
    
    def check_coins_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)
        
        if enemy_collisions:
            
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >  0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -16
                    explosion_sprite = ParticleEffect(enemy.rect.center, "explosion")
                    self.explosion_sprite.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damaged()
                    
    def run(self):
        
        self.input()
        
        
        #decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        

        #bg palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)


        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        
        
        #terrain tiles
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        
        
        self.scroll_x()
        
        #enemy #constrains
        self.enemy_sprites.update(self.world_shift)
        self.constrain_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        self.explosion_sprite.update(self.world_shift)
        self.explosion_sprite.draw(self.display_surface)
        
        
        #crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
        
        
        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        
        
        #coins
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)
        
        
        #fg palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)
        
        
        #player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface )
        
        
        #player updates
        self.player.update()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        
        #checks
        self.check_death()
        self.check_win()
        self.check_coins_collision()
        self.check_enemy_collisions()
        
        #water
        self.water.draw(self.display_surface, self.world_shift)




