import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
import os
from textos import DamageText
from items import Item
from mundo import Mundo
import csv




#IMAGENES
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, size=(w*scale, h*scale))
    return nueva_imagen


#FUNCION PARA CONTAR ELEMENTOS
def contar_elementos(directorio):
    return len(os.listdir(directorio))

#FUNCION LISTAR ELEMENTOS
def nombres_carpetas(directorio):
    return os.listdir(directorio)

pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, 
                                    constantes.ALTO_VENTANA))

pygame.display.set_caption("Bienvenidos a mi juego")

#VARIABLE
posicion_pantalla= [0, 0]
nivel = 1

#FUENTES
font = pygame.font.Font("assets//font//Super Space.otf", 25)
font_game_over = pygame.font.Font("assets//font//Super Space.otf", 100)
font_reinicio = pygame.font.Font("assets//font//Super Space.otf", 18)
font_incio = pygame.font.Font("assets//font//Super Space.otf", 30)
font_titulo = pygame.font.Font("assets//font//Super Space.otf", 75)

game_over_text = font_game_over.render('Game Over', True, constantes.BLANCO)
texto_boton_reinicio = font_reinicio.render('Reiniciar juego', True, constantes.NEGRO)

#BOTON INICIO   
boton_jugar = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100, constantes.ALTO_VENTANA / 2 - 50, 200, 50)
boton_salir = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100, constantes.ALTO_VENTANA / 2 + 50, 200, 50)

texto_boton_jugar =  font_incio.render('Jugar', True, constantes.NEGRO)
texto_boton_salir =  font_incio.render('Salir', True, constantes.NEGRO)


#PANTALLA INICIO
def pantalla_incio():
    imagen_fondo = pygame.image.load("assets//images//BK.jpg")
    imagen_fondo = pygame.transform.scale(imagen_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    #ventana.fill(constantes.COLOR_BACKGROUND)
    ventana.blit(imagen_fondo, (0, 0))
    dibujar_texto("El laberinto", font_titulo, constantes.COLOR_TITULO, constantes.ANCHO_VENTANA / 2 - 250, constantes.ALTO_VENTANA / 2 - 200 )
    pygame.draw.rect(ventana, constantes.BOTON_COLOR, boton_jugar)
    pygame.draw.rect(ventana, constantes.BOTON_COLOR_2, boton_salir)
    ventana.blit(texto_boton_jugar, (boton_jugar.x + 50, boton_jugar.y + 10))
    ventana.blit(texto_boton_salir, (boton_salir.x + 50, boton_salir.y + 10))
    pygame.display.update()


#############################################################################
###################### IMPORTAR IMAGENES ####################################
#############################################################################
#ENERGIA
corazon_completo = pygame.image.load("assets//energy//1.png").convert_alpha()
corazon_completo = escalar_img(corazon_completo, constantes.ESCALA_ENERGIA)

corazon_medio = pygame.image.load("assets//energy//2.png").convert_alpha()
corazon_medio = escalar_img(corazon_medio, constantes.ESCALA_ENERGIA)

corazon_vacio = pygame.image.load("assets//energy//3.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio, constantes.ESCALA_ENERGIA)


#PERSONAJE
animaciones = []
for i in range(6):
    img = pygame.image.load(f"assets//images//characters//personaje//hero_{i+1}.png")
    img = escalar_img( img, constantes.ESCALA_PERSONAJE)
    animaciones.append(img)

#ENEMIGOS
directorio_enemigos = "assets//images//characters//enemigos"
tipo_enemigos = nombres_carpetas(directorio_enemigos)
animacion_enemigo = []

for eni in tipo_enemigos:
    lista_temp = [] #LISTA TEMPORAL 
    ruta_temp = f"assets//images//characters//enemigos//{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(f"{ruta_temp}//{eni}_{i+1}.png").convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.ESCALA_ENEMIGOS)
        lista_temp.append(img_enemigo)
    animacion_enemigo.append(lista_temp)

imagen_balas = pygame.image.load(f"assets//images//weapon//bullet.png") 
imagen_balas = escalar_img(imagen_balas, constantes.ESCALA_ARMA)


#ARMA
imagen_pistola = pygame.image.load(f"assets//images//weapon//weapon.png") 
imagen_pistola = escalar_img(imagen_pistola, constantes.ESCALA_ARMA)

#BALAS
imagen_balas = pygame.image.load(f"assets//images//weapon//bullet.png") 
imagen_balas = escalar_img(imagen_balas, constantes.ESCALA_ARMA)

# #IMAGEBES DE LOS ITEMS
posion = pygame.image.load("assets//items//posion.png")
posion = escalar_img(posion, constantes.CAJA_ESCALA)

coin_images = []
ruta_img = "assets//items//coin//"
num_coin_images = contar_elementos(ruta_img)
for i in range(num_coin_images):
    img = pygame.image.load(f"assets//items//coin//coin_{i+1}.png")
    img = escalar_img(img, constantes.MONEDA_ESCALA)
    coin_images.append(img)

item_imagenes = [coin_images, [posion]]

#SCORE DEL PERSONAJE

def dibujar_texto(texto,fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x, y))



#CARGAR IMAGENES DEL MUNDO
tile_list = []
for x in range(constantes.TILE_TYPES): ########
    tile_image = pygame.image.load(f"assets//images//tiles//tile ({x+1}).png")
    tile_image = pygame.transform.scale(tile_image, (constantes.TILE_SIZE, constantes.TILE_SIZE))
    tile_list.append(tile_image)

#VIDA DEL JUGADOR
def vida_jugador():
    c_mitad_dibujado = False
    for i in range(4):
        if jugador.energia >= ((i+1)*25):
            ventana.blit(corazon_completo, (6+i*50, 5))
        elif jugador.energia % 16 > 0 and c_mitad_dibujado == False:
            ventana.blit(corazon_medio, (6+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio, (6+i*50, 5))

#RESETEAR MUNDO
def resetear_mundo():
    grupo_damage_text.empty()
    grupo_balas.empty()
    grupo_items.empty()

    data = []
    for fila in range(constantes.FILAS):
        filas = [2] * constantes.COLUMNAS
        data.append(filas)
    return data
    

#DIBUJAR MUNDO  
world_data = []

for filas in range(constantes.FILAS):
    filas = [5] * constantes.COLUMNAS
    world_data.append(filas)


with open("niveles//nivel_1.csv", newline='') as csvfile: #CARGA EL ARCHIVO CON EL NIVEL CREADO
    reader = csv.reader(csvfile, delimiter=',')
    for x, fila in enumerate(reader):
        for y, columna in enumerate(fila):
            if columna.strip():
                world_data[x][y] = int(columna)  


world = Mundo()
world.process_data(world_data, tile_list, item_imagenes, animacion_enemigo) 


#GRID EN PANTALLA

def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, constantes.BLANCO, (x*constantes.TILE_SIZE, 0), (x*constantes.TILE_SIZE, constantes.ALTO_VENTANA))
        pygame.draw.line(ventana, constantes.BLANCO, (0, x*constantes.TILE_SIZE), (constantes.ANCHO_VENTANA, x*constantes.TILE_SIZE))


#CREA JUGADOR DE LA CLASE PERSONAJE
jugador = Personaje(1000, 1000, animaciones, 100, 1)



#CREA LISTA DE ENEMIGOS
lista_enemigos = []
for ene in world.lista_enemigo:
    lista_enemigos.append(ene)

#CREA UN ARMA DE LA CLASE WEAPON
pistola = Weapon(imagen_pistola, imagen_balas) 

#CREA UN GRUPO DE SPRITES 
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

#AGREGA ITEMS DESDE LA DATA DEL LVL
for item in world.lista_item:
    grupo_items.add(item)

#VARIABLES DE MOVIMIENTO DE JUGADOR
mover_arriba = False
mover_abajo = False
mover_izquierda =  False
mover_derecha = False

reloj = pygame.time.Clock()

boton_reinicio = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100,
                            constantes.ALTO_VENTANA / 2 + 100, 200, 50)


sonido_disparo = pygame.mixer.Sound("assets//sounds//shot.mp3")

mostrar_inicio = True
run = True

while run:
    if mostrar_inicio:
        pantalla_incio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if boton_salir.collidepoint(event.pos):
                    run = False
    else:

        reloj.tick(constantes.FPS) 
        ventana.fill(constantes.COLOR_BACKGROUND) #COLOR DE FONDO

        if jugador.vivo == True:

            #CALCULAR MOVIMIENTO DEL JUGADOR
            delta_x = 0
            delta_y = 0

            if mover_derecha == True:
                delta_x = constantes.VELOCIDAD
            if mover_izquierda == True:
                delta_x = -constantes.VELOCIDAD
            if mover_arriba == True:
                delta_y = -constantes.VELOCIDAD
            if mover_abajo == True:
                delta_y = constantes.VELOCIDAD

            #MOVER AL JUGADOR
            posicion_pantalla, nivel_completado = jugador.mover_personaje(delta_x, delta_y, world.obstaculos_tiles, world.exit_tile)
            #ACTAULIZAR MAPA
            world.update(posicion_pantalla)

            #ACTUALIZA ESTADO DEL JUGADOR   
            jugador.update()

            #ACTUALIZA EL ESTADO DEL ENEMIGO
            for ene in lista_enemigos:
                ene.update()


            #ACTUALIZA ESTADO DEL ARMA //cuando reconozca el click izq se guardara en el grupo balas
            bala = pistola.update(jugador)
            if bala:
                grupo_balas.add(bala)
                sonido_disparo.play()
            for bala in grupo_balas:
                damage, pos_damage = bala.update(lista_enemigos, world.obstaculos_tiles) #CADA VEZ QUE ACTUALIZA LA BALA DEVUELVE EL DAÑO
                if damage:
                    damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, constantes.ROJO)
                    grupo_damage_text.add(damage_text)

            #ACTUALIZAR DAÑO
            grupo_damage_text.update(posicion_pantalla)

            #ACTUALIZAR ITEMS
            grupo_items.update(posicion_pantalla, jugador)

        #DIBUJAR MUNDO
        world.draw(ventana)

        #BIBUJAR JUGADOR
        jugador.dibujar(ventana)

        #BIBUJAR ENEMIGO
        for ene in lista_enemigos:
            if ene.energia == 0:
                lista_enemigos.remove(ene)
            if ene.energia > 0:
                ene.enemigos(jugador, world.obstaculos_tiles, posicion_pantalla, world.exit_tile)
                ene.dibujar(ventana)

        #DIBUJAR ARMA
        pistola.dibujar(ventana) 

        #DIBUJAR BALA
        for bala in grupo_balas:
            bala.dibujar(ventana)

        #DIBUJA LOS CORAZONES DEL JUGADOR
        vida_jugador()

        #DIBUJAR TEXTOS
        grupo_damage_text.draw(ventana)
        dibujar_texto(f"Score: {jugador.score}", font, constantes.BOTON_COLOR, 600, 8)
        #DIBUJA EL NIVEL
        dibujar_texto(f"Nivel "+ str(nivel), font, constantes.BOTON_COLOR, constantes.ANCHO_VENTANA // 2.5, 8)
        

        #DIBUJAR ITEMS
        grupo_items.draw(ventana)

        if nivel_completado == True:
            if nivel < constantes.NIVEL_MAXIMO:
                nivel += 1
                world_data = resetear_mundo()
                with open(f"niveles//nivel_{nivel}.csv", newline='') as csvfile: #CARGA EL ARCHIVO CON EL NIVEL CREADO
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, fila in enumerate(reader):
                        for y, columna in enumerate(fila):
                            if columna.strip():
                                world_data[x][y] = int(columna)  
                world = Mundo()
                world.process_data(world_data, tile_list, item_imagenes, animacion_enemigo) 
                jugador.actualizar_coordenadas(constantes.COORDENADAS[str(nivel)])

                #CREA ENEMIGOS NUEVOS
                lista_enemigos = []
                for ene in world.lista_enemigo:
                    lista_enemigos.append(ene)
                
                #AGREGA ITEMS DESDE LA DATA DEL LVL
                for item in world.lista_item:
                    grupo_items.add(item)

        if jugador.vivo == False:
            ventana.fill(constantes.ROJO_OSCURO)
            text_rect = game_over_text.get_rect(center=(constantes.ANCHO_VENTANA /2,
                                                        constantes.ALTO_VENTANA / 2))
            
            ventana.blit(game_over_text, text_rect)
            
            pygame.draw.rect(ventana, constantes.AMARILLO, boton_reinicio)
            ventana.blit(texto_boton_reinicio, (boton_reinicio.x + 50, boton_reinicio.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

            if event.type == pygame.KEYDOWN:
                if event.key  == pygame.K_a:
                    mover_izquierda = True
                if event.key  == pygame.K_d:
                    mover_derecha = True
                if event.key  == pygame.K_w:
                    mover_arriba = True
                if event.key  == pygame.K_s:
                    mover_abajo = True
                if event.key == pygame.K_e:
                    if world.abrir_puerta(jugador, tile_list):
                        print("Puerta abierta")


            if event.type == pygame.KEYUP:
                if event.key  == pygame.K_a:
                    mover_izquierda = False
                if event.key  == pygame.K_d:
                    mover_derecha = False
                if event.key  == pygame.K_w:
                    mover_arriba = False
                if event.key  == pygame.K_s:
                    mover_abajo = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reinicio.collidepoint(event.pos) and not jugador.vivo:
                    jugador.vivo = True
                    jugador.energia = 100
                    jugador.score = 0
                    nivel = 1
                    world_data = resetear_mundo()
                    with open(f"niveles//nivel_{nivel}.csv", newline='') as csvfile: #CARGA EL ARCHIVO CON EL NIVEL CREADO
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, fila in enumerate(reader):
                            for y, columna in enumerate(fila):
                                if columna.strip():
                                    world_data[x][y] = int(columna) 
                    world = Mundo()
                    world.process_data(world_data, tile_list, item_imagenes, animacion_enemigo) 
                    jugador.actualizar_coordenadas(constantes.COORDENADAS[str(nivel)])

                    #CREA ENEMIGOS NUEVOS
                    lista_enemigos = []
                    for ene in world.lista_enemigo:
                        lista_enemigos.append(ene)
                
                    #AGREGA ITEMS DESDE LA DATA DEL LVL
                    for item in world.lista_item:
                        grupo_items.add(item)

        pygame.display.update()

pygame.quit()