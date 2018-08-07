import sys    # para usar exit()
import pygame
import time # control de tiempos
import os

posicion = 100, 40
os.environ["SDL_VIDEO_WINDOW_POS"] = str(posicion[0]) + "," + str(posicion[1])

ANCHO = 840 # Ancho de la pantalla.
ALTO = 600  # Alto de la pantalla.
color_azul = (0, 0, 64)  # Color azul para el fondo.
color_rojo = (188, 15, 15)
fond = pygame.image.load("background.jpg")

# Icono
gameIcon = pygame.image.load("ico.png")
pygame.display.set_icon(gameIcon)

pygame.init()

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('skull.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla.
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        # Establecer velocidad inicial.
        self.speed = [0, 0]

    def update(self):
        # Evitar que salga por encima.
        if self.rect.bottom <= 50:
            self.speed[1] = -self.speed[1]

        # Evitar que salga por la derecha o izquierda.
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Mover en base a posición actual y velocidad.
        self.rect.move_ip(self.speed)


class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('paleta2.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial centrada en pantalla en X.
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        # Establecer velocidad inicial.
        self.speed = [0, 0]

    def update(self, evento):
        # Buscar si se presionó flecha izquierda.
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-17, 0]
        # Si se presionó flecha derecha.
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [17, 0]
        else:
            self.speed = [0, 0]
        # Mover en base a posición actual y velocidad.
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        # Cargar imagen
        self.image = pygame.image.load('ladrillo.png')
        # Obtener rectángulo de la imagen
        self.rect = self.image.get_rect()
        # Posición inicial, provista externamente.
        self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height

# Funcion llamada tras dejar ir la bolita
def juego_terminado():
	fuente = pygame.font.SysFont("Consolas", 72)        
	texto = fuente.render("Game Over", True, color_rojo)
	texto_rect = texto.get_rect()
	texto_rect.center = [ANCHO / 2, ALTO / 2]
	pantalla.blit(texto, texto_rect)
	pygame.display.flip()
	# Pausar por tres segundos
	time.sleep(2)
	# Salir
	sys.exit()

def mostrar_puntuacion():
	fuente = pygame.font.SysFont("Consolas", 20)        
	texto = fuente.render(str(puntuacion).zfill(4), True, color_rojo)
	texto_rect = texto.get_rect()
	texto_rect = [595 , 0]
	pantalla.blit(texto, texto_rect)

def mostrar_vidas():
	fuente = pygame.font.SysFont("Consolas", 20)
	cadena = "Vidas:" + str(vidas).zfill(2)     
	texto = fuente.render(cadena, True, color_rojo)
	texto_rect = texto.get_rect()
	texto_rect.topright = [90 , 0]
	pantalla.blit(texto, texto_rect)


# Inicializando pantalla.
pantalla = pygame.display.set_mode((ANCHO, ALTO))
# Configurar título de pantalla.
pygame.display.set_caption('Game_Pong')


# Crear el reloj.
reloj = pygame.time.Clock()
# Ajustar repetición de evento de tecla presionada.
pygame.key.set_repeat(60)


bolita = Bolita()
jugador = Paleta()
muro = Muro(147) # 147
puntuacion = 0
vidas = 1
saque = True

cambioVelocidad = 10
velocidadBola = 4

done = False
while not done:
    # Establecer FPS.
    reloj.tick(60)


    # Revisar todos los eventos.
    for evento in pygame.event.get():
 
        # Si se presiona la la "X" de la barra de título,
        if evento.type == pygame.QUIT:
            done = True
            break

        # Buscar eventos del teclado,
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)
            if saque == True and evento.key == pygame.K_SPACE:
            	saque = False
            	if bolita.rect.centerx < ANCHO / 2:
            		bolita.speed = [-velocidadBola, velocidadBola]
            	else:
            		bolita.speed = [-velocidadBola, -velocidadBola]

            # Para salir con la Tecla ESCAPE
            if evento.key == pygame.K_ESCAPE:
                done = True
                break

    if cambioVelocidad == puntuacion:
        cambioVelocidad += 20
        velocidadBola += 0.15
        print("V: ", velocidadBola, "cambio V: ", cambioVelocidad,"\n puntuacion: ", puntuacion)
        #bolita.speed = [velocidadBola, velocidadBola]
        if bolita.rect.centerx < ANCHO / 2:
            bolita.speed = [-velocidadBola, velocidadBola]
        else:
            bolita.speed = [-velocidadBola, -velocidadBola]


    # Actualizar posición de la bolita.
    if saque == False:
    	bolita.update()
    else:
    	bolita.rect.midbottom = jugador.rect.midtop
    # Colision entre bolita y el jugador
    if pygame.sprite.collide_rect(bolita, jugador):
    	bolita.speed[1] = -bolita.speed[1]

    # Colision con el Muro
    lista = pygame.sprite.spritecollide(bolita, muro, False)
    if lista:
    	ladrillo = lista[0]
    	cx = bolita.rect.centerx
    	if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
    		bolita.speed[0] = -bolita.speed[0]
    	else:
    		bolita.speed[1] = -bolita.speed[1]
    	muro.remove(ladrillo)
    	puntuacion += 10


    # Revisar si bolita sale de la pantalla
    if bolita.rect.top > ALTO:
    	vidas -= 1
    	saque = True

    # Rellenar la pantalla.
    pantalla.blit(fond, (0,0))
    # Mostrar Puntuacion
    mostrar_puntuacion()
    # Mostrar Vidas
    mostrar_vidas()
    # Dibujar bolita en pantalla.
    pantalla.blit(bolita.image, bolita.rect)
    # Dibujar jugador en pantalla.
    pantalla.blit(jugador.image, jugador.rect)
    # Dibujar los ladrillos.
    muro.draw(pantalla)
    # Actualizar los elementos en pantalla.
    pygame.display.flip()

    if vidas <= 0:
    	juego_terminado()