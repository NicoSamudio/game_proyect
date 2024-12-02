import pygame
import math
import constantes


class Personaje():

    def __init__(self, x, y, animaciones, energia, tipo):

        self.score = 0
        self.energia = energia
        self.vivo = True
        self.flip  = False
        self.animaciones = animaciones
        #IMAGEN DE LA ANIMACION QUE SE MUESTRA ACTUALMENTE
        self.frames_index = 0
        #SE GUARDA LA HORA ACTUAL EN MILISEGUNDOS DESDE QUE SE INICIO PYGAME
        self.upadate_time = pygame.time.get_ticks()
        self.image = animaciones[self.frames_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.tipo = tipo # 1 PERSONAJE // 2 ENEMIGO
        self.golpe = False
        self.ultimo_golpe = pygame.time.get_ticks()

    def actualizar_coordenadas(self, tupla):
        self.forma.center = (tupla[0], tupla[1])

    def enemigos(self, jugador, obstaculos_tiles, posicion_pantalla, exit_tile):

        clipped_line = ()
        ene_dx = 0 #ENEMIGO EN DELTA X O DELTA Y
        ene_dy = 0

        #ENEMIGOS EN LA POSICION DE PANTALLA
        self.forma.x += posicion_pantalla[0]
        self.forma.y += posicion_pantalla[1]

        #LINEA DE VISION

        linea_vision = ((self.forma.centerx, self.forma.centery),
                        (jugador.forma.centerx, jugador.forma.centery))
        
        #VERIFICA SI HAY ALGUN OBSTACULO
        for obs in obstaculos_tiles:
            if obs[1].clipline(linea_vision):
                clipped_line = obs[1].clipline(linea_vision) #GUARDA LAS COORDENADAS DE LA COLISON
            

        #DISTANCIA CON EL JUGADOR 
        distancia = math.sqrt(((self.forma.centerx - jugador.forma.centerx)**2) + 
                            ((self.forma.centery - jugador.forma.centery)**2))
        
        if not clipped_line and distancia < constantes.RANGO:
            #LOGICA DE SEGUIMIENTO DEL ENEMIGO
            if self.forma.centerx > jugador.forma.centerx:
                ene_dx = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centerx < jugador.forma.centerx:
                ene_dx = constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery > jugador.forma.centery:
                ene_dy = -constantes.VELOCIDAD_ENEMIGO
            if self.forma.centery < jugador.forma.centery:
                ene_dy = constantes.VELOCIDAD_ENEMIGO


        self.mover_personaje(ene_dx, ene_dy, obstaculos_tiles, exit_tile)
        
        #ATAQUE DE ENEMIGO
        if distancia  < constantes.RANGO_DE_ATAQUE and jugador.golpe == False:
            jugador.energia -= 10
            jugador.golpe = True
            jugador.ultimo_golpe = pygame.time.get_ticks()

    
    def update(self):
        
        #COMPRUEBA SI ESTA VIVO
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        #COOLDOWN DAÑO
        golpe_cooldown = 1000
        if self.tipo == 1:
            if self.golpe == True:
                if pygame.time.get_ticks() - self.ultimo_golpe > golpe_cooldown:
                    self.golpe = False


        #TIEMPO QUE MANTIENE LA IMAGEN ANTES DE CAMBIARLA   
        cooldown_animacion = 100
        self.image = self.animaciones[self.frames_index]
        if pygame.time.get_ticks() - self.upadate_time >= cooldown_animacion:
            self.frames_index = self.frames_index + 1
            self.upadate_time = pygame.time.get_ticks()
        if self.frames_index >= len(self.animaciones):
            self.frames_index = 0

    def dibujar(self, ventana):

        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.forma)
        # pygame.draw.rect(ventana, constantes.COLOR_PERSONAJE, self.forma, width= 1)  #DIBUJAMOS RECTANGULO PARA LOS PERSONAJES // ENEMIGOS


    def mover_personaje(self, delta_x, delta_y, obstaculos_tiles, exit_tile):

        posicion_pantalla = [0, 0]
        nivel_completado = False
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        

        self.forma.x = self.forma.x + delta_x
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_x > 0:
                    self.forma.right = obstacle[1].left
                if delta_x < 0:
                    self.forma.left = obstacle[1].right


        self.forma.y = self.forma.y + delta_y
        for obstacle in obstaculos_tiles:
            if obstacle[1].colliderect(self.forma):
                if delta_y > 0:
                    self.forma.bottom = obstacle[1].top
                if delta_y < 0:
                    self.forma.top = obstacle[1].bottom


        #LOGICA PARA JUGADOR
        if self.tipo == 1:
            
            #CHEQUEO COLISION DE SALIDA
            if exit_tile[1].colliderect(self.forma):
                nivel_completado = True


            if self.forma.right > (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[0] = (constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA) - self.forma.right
                self.forma.right = constantes.ANCHO_VENTANA - constantes.LIMITE_PANTALLA
            if self.forma.left < constantes.LIMITE_PANTALLA:
                posicion_pantalla[0] = constantes.LIMITE_PANTALLA - self.forma.left
                self.forma.left = constantes.LIMITE_PANTALLA

            if self.forma.bottom > (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA):
                posicion_pantalla[1] = (constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA) - self.forma.bottom
                self.forma.bottom = constantes.ALTO_VENTANA - constantes.LIMITE_PANTALLA
            if self.forma.top < constantes.LIMITE_PANTALLA:
                posicion_pantalla[1] = constantes.LIMITE_PANTALLA - self.forma.top
                self.forma.top = constantes.LIMITE_PANTALLA

            return posicion_pantalla, nivel_completado

