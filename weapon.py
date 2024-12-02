import pygame
from pygame.sprite import Group
import constantes
import math
import random

class Weapon ():
    def __init__(self, image, imagen_bala):
        
        self.imagen_bala = imagen_bala
        self.flip  = False
        self.imagen_original = image
        self.angulo = 0
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()
        self.disparada = False
        self.ultimo_disparo = pygame.time.get_ticks()



    def update(self, personaje):

        disparo_cooldown = constantes.COOLDOWN_BALAS
        bala = None
        self.forma.center = personaje.forma.center
        self.forma.y = self.forma.y + 4  #SUBE O BAJA LA POSICION DEL ARMA
        if personaje.flip == False:
            self.forma.x = self.forma.x + personaje.forma.width / 8 #CENTRA O CORRE LA POSICION DEL ARMA
            self.rotar_arma(False)
        if personaje.flip == True:
            self.forma.x = self.forma.x - personaje.forma.width / 8
            self.rotar_arma(True)

        #MOVER PISTOLA CPON EL MOUSE

        mouse_pos = pygame.mouse.get_pos()
        distancia_x = mouse_pos[0] - self.forma.centerx
        distancia_y = -(mouse_pos[1] - self.forma.centery)
        self.angulo = math.degrees(math.atan2(distancia_y, distancia_x))  #CALCULA EL ANGULO DEL ARMA

        #DETECTAMOS EL CLICK    
        if pygame.mouse.get_pressed()[0] and self.disparada == False and (pygame.time.get_ticks()-self.ultimo_disparo >= disparo_cooldown):
            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, self.angulo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()

        #RESETEO EL DISPARO
        if pygame.mouse.get_pressed()[0] == False: #EL MOUSE NO ESTA PRESIONADO
            self.disparada = False
        
        return bala


    def rotar_arma(self, rotar):
        
        if rotar == True:
            imagen_flip = pygame.transform.flip(self.imagen_original,
                                                True, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)
        
        else:
            imagen_flip = pygame.transform.flip(self.imagen_original,
                                                False, False)
            self.imagen = pygame.transform.rotate(imagen_flip, self.angulo)


    def dibujar(self, interfaz):

        self.imagen = pygame.transform.rotate(self.imagen, self.angulo)
        interfaz.blit(self.imagen, self.forma)
        # pygame.draw.rect(interfaz, constantes.COLOR_ARMA, self.forma, width= 1) #DIBUJA RECTANGULO EN EL ARMA


class Bullet(pygame.sprite.Sprite):

    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_orginal = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_orginal, self.angulo) #USO IMAGE PORQUE ES EL ATRIBUTO DE LA CLASE SPRITE // el atirbuto imagen va a ser un atributo de rotacion
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #VELOCIDAD DE LA BALA     
        self.delta_x = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA

    def update(self, lista_enemigos, obstaculos_tiles): 

        daño = 0
        pos_daño = None

        self.rect.x += self.delta_x 
        self.rect.y += self.delta_y

        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()

        #VERIFICA COLISION
        for enemigo in lista_enemigos:
            if enemigo.forma.colliderect(self.rect):
                daño = 15 + random.randint(-7, 7)
                pos_daño = enemigo.forma
                enemigo.energia -= daño
                self.kill()
                break
        
    
        #VERIFICA LA COLISON DE BALAS CON LAS PAREDES
        for obs in obstaculos_tiles:
            if obs[1].colliderect(self.rect):
                self.kill()
                break

        return daño, pos_daño

    def dibujar(self, interfaz):

        interfaz.blit(self.image, (self.rect.centerx - int(self.image.get_width() / 6), 
                                self.rect.centery - int(self.image.get_height() / 2)))