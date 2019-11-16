import os
import math
import pygame
from random import randint

# Analiza el estado del campo
# Decide cuando rotar
# Hacer lanzamiento a la porteria con probabilidad de desvio
# random pelota random carro

'''
Propuestas para variables de entrada crisp
--- HACIA LA PELOTA
- Distancia a la pelota
x -> [0:1] creciente polinomica
- Direccion hacia la pelota basado en signos de catetos
x, y -> NO | NE | SO | SE
'''

'''
Dimensiones del tablero
- HEIGHT 100
- WIDTH 100
'''

'''
Clausulas de Horn propuestas
            | NO      | NE       | SO        | SE
[0.0 : 0.2] | (45, 1) | (135, 1) | (315, 1)  | (225, 1)
[0.2 : 0.7] | (45, 5) | (135, 5) | (315, 5)  | (225, 5)
[0.7 : 1.0] | (45, 10)| (135, 10)| (315, 10) | (225, 10)
Direccion y Maginitud

Clausulas de Horn propuestas V2.0
            | NO      | NE       | SO        | SE
[0.0 : 0.2] | (1, 1)  | (-1, 1)  | (1, -1)   | (-10, -1)
[0.2 : 0.7] | (5, 5)  | (-5, 5)  | (5, -5)   | (-10, -5)
[0.7 : 1.0] | (10, 10)| (-10, 10)| (10, -10) | (-10, -10)
Cambio en X y Y
'''

'''
Reglas
IF x = [0.0 : 0.2] AND x, y = NO then m = (1, 1) -> moveto(x+1, y+1)
..el resto..
'''


# return the absolute distance between two points
abs_dist = lambda x, y: math.sqrt(x**2 + y**2)

# return the angle adjacent to x in a right triangle
abs_angle = lambda x, y: math.degrees(math.atan(y/x))

# return the sign of a value
sign = lambda x: (1, -1)[x < 0]

# FUNCIONES LINGUISTICAS
# return the modeled value based on the function provided
distance_ling = lambda x: 0.02551565 + 0.01470778*x - 0.00005531812*x**2 if x < 142 else 0

# return the direction based on the signs of the triangle legs REQUIRES SIGNED INPUT
orientation_ling = lambda x, y: 'NO' if (x == 1 and y == 1) else ('NE' if (x == -1 and y == 1) else ('SE' if (x ==-1 and y ==-1) else ('SO' if (x ==1 and y ==-1) else 0)))

# not used
# orientation_ling = lambda a: 'N' if (a > 45 and a < 135) else ('O' if (a > 135 and a < 180) else ('E' if (a > 0 and a < 45) else 0))

# pygame CONST
WIDTH = 300  # width window
HEIGHT = 300 # height window
FPS = 30 # frames per second

# pygames graphic display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIMULACION")
clock = pygame.time.Clock()

# random positions
# ball
ball_x = WIDTH / 2 + randint(-140,140)
ball_y = HEIGHT / 2 + randint(-140, 140)

# player
player_x = WIDTH / 2 + randint(-140,140)
player_y = HEIGHT / 2 + randint(-140, 140)
player_init_angle = randint(0, 360)

# pygame classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('mario.png'))
        self.imageOriginal = pygame.image.load(os.path.join('mario.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = player_x
        self.rect.y = player_y
        self.rotation = 0
        self.rotatePlayer(player_init_angle)
        self.rotateTo = 1

    def update(self):
        self.rect.x += 2
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def rotatePlayer(self, angle):
        self.rotation += angle
        self.image = pygame.transform.rotate(self.imageOriginal, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = player_x
        self.rect.y = player_y

    def rotatePlayerTo(self, angle):
        self.rotation = angle
        self.image = pygame.transform.rotate(self.imageOriginal, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = player_x
        self.rect.y = player_y

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3, 3))
        self.image.fill((255,100,0))
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = ball_x
        self.rect.y = ball_y

# methods for calculations
def ball_player_ang(gameobject, bx = ball_x, by = ball_y, px = player_x, py = player_y):
    triangle_x = bx - px
    triangle_y = by - py

    cuadrante = lambda x, y: 'RD' if (x == 1 and y == 1) else ('LD' if (x == -1 and y == 1) else ('LU' if (x ==-1 and y ==-1) else ('RU' if (x ==1 and y ==-1) else 0)))
    cua = cuadrante(sign(triangle_x), sign(triangle_y))
    angle = abs(math.degrees(math.atan(triangle_y / triangle_x)))

    if cua == "RU":
        angle = 270 + angle
    elif cua == "RD":
        angle = 270 - angle
    elif cua == "LU":
        angle = 90 - angle
    elif cua == "LD":
        angle = 90 + angle

    toRotate = angle - gameobject.rotation
    if toRotate < -180:
        return(toRotate + 360)
    elif toRotate > 180:
        return(toRotate - 360)
    else:
        return(toRotate)

'''
Ball is reciben valores entre 0 y 420 (WIDTH**2 + HEIGHT**2)**(1/2) da pertenencia a proximidad
Output [0-1]
'''

ball_is_close = lambda d: (1/105)*d if (d <= 105) else ((1/105) * d - 1 if (d > 105 and d <= 210) else 0)
ball_is_medium = lambda d: (1/105)*(d-105) if (d <= 210 and d > 105) else (1 - (1/105) * (d-105) + 1 if (d > 210 and d <= 315) else 0)
ball_is_far = lambda d: (1/105)*(d-210) if (d <= 315 and d > 210) else (1 - (1/105) * (d-210) + 1 if (d > 315 and d <= 420) else 0)


'''
Angle is reciben valores entre 0 y 360 da pertenencia a direccion
Output [0-1]
'''
# angle_is_near_viejo = lambda a: (1/45)*a if (a <= 45) else ((1/45)*a -6 if (a >= 270 and a <= 315) else (1 - (1/45)*a + 1 if (a > 45 and a <= 90) else (1 - (1/45)*a + 7 if (a > 315 and a <= 360) else 0)))
angle_is_near = lambda a: (1.0) if (a <= 45) else ((1/45)*a -6 if (a >= 270 and a <= 315) else (1 - (1/45)*a + 1 if (a > 45 and a <= 90) else ( (1.0) if (a > 315 and a <= 360) else 0)))
angle_is_half = lambda a: (1/45)* (a-45) if (a <= 90 and a > 45) else ((1/45)*a - 5 if (a >= 225 and a <= 270) else (1 - (1/45)*a + 2 if (a > 90 and a <= 135) else (1 - (1/45)*a + 6 if (a > 270 and a <= 315) else 0)))
angle_is_wide = lambda a: (1/45)*a - 2 if (a >= 90 and a <= 135) else (1 - (1/45)*a + 5 if (a >= 225 and a <= 270) else ( 1 if (a > 135 and a < 225) else 0))


# sprites
all_sprites = pygame.sprite.Group()
player = Player()
ball = Ball()
all_sprites.add(player)
all_sprites.add(ball)

print(ball_player_ang(player))

# display loop
done = False
while not done:
    # FPS
    clock.tick(FPS)

    # key and display controls
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.rotatePlayer(15)

    # update
    screen.fill((0,0,0))

    # render
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 0, 100, 2))
    pygame.display.flip()

# quit pygames
pygame.quit()
