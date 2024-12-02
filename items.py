import pygame.sprite


class Item(pygame.sprite.Sprite):



    def __init__(self, x, y, item_type, animacion_list):
            
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0 = MONEDA // 1 = POSION
        self.animacion_list = animacion_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animacion_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, posicion_pantalla, personaje):

        self.rect.x += posicion_pantalla[0]
        self.rect.y += posicion_pantalla[1]

        #COMPROBAR COLISION
        #MONEDAS
        if self.rect.colliderect(personaje.forma):
            if self.item_type == 0:
                personaje.score += 1
            elif self.item_type == 1:
                personaje.energia += 50
                if personaje.energia > 100:
                    personaje.energia = 100
            self.kill()


        cooldown_animacion = 50
        self.image = self.animacion_list[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animacion_list):
            self.frame_index = 0

        