import os
import math
import time
import pygame
from random import randint

# FUNCIONES LINGUISTICAS
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
angle_is_near_viejo = lambda a: (1/45)*a if (a <= 45) else ((1/45)*a -6 if (a >= 270 and a <= 315) else (1 - (1/45)*a + 1 if (a > 45 and a <= 90) else (1 - (1/45)*a + 7 if (a > 315 and a <= 360) else 0)))
angle_is_near = lambda a: (1.0) if (a <= 45) else ((1/45)*a -6 if (a >= 270 and a <= 315) else (1 - (1/45)*a + 1 if (a > 45 and a <= 90) else ( (1.0) if (a > 315 and a <= 360) else 0)))
angle_is_half = lambda a: (1/45)* (a-45) if (a <= 90 and a > 45) else ((1/45)*a - 5 if (a >= 225 and a <= 270) else (1 - (1/45)*a + 2 if (a > 90 and a <= 135) else (1 - (1/45)*a + 6 if (a > 270 and a <= 315) else 0)))
angle_is_wide = lambda a: (1/45)*a - 2 if (a >= 90 and a <= 135) else (1 - (1/45)*a + 5 if (a >= 225 and a <= 270) else ( 1 if (a > 135 and a < 225) else 0))

# return the sign of a value
sign = lambda x: (1, -1)[x < 0]

# pygame CONST
WIDTH = 300  # width window
HEIGHT = 300 # height window
FPS = 15 # frames per second

# random positions
# ball initial position
ball_x = WIDTH / 2 + randint(-130,130)
ball_y = HEIGHT / 2 + randint(-130, 130)

# player initial position
player_x = WIDTH / 2 + randint(-130,130)
player_y = HEIGHT / 2 + randint(-130, 130)
player_init_angle = randint(0, 360)

# pygames graphic display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # frame
pygame.display.set_caption("SIMULACION")            # name
clock = pygame.time.Clock()                         # clock

# pygame classes

# Player(sprite)
# Se encarga de crear el gameobject del jugador y almacena las funciones de
# rotacion y movimiento de este.
class Player(pygame.sprite.Sprite):

    # init
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

    # repinta al jugador y lo mueve (NO SE USA)
    def update(self):
        self.rect.x += 2
        if self.rect.left > WIDTH:
            self.rect.right = 0

    # rota al jugador una cierta cantidad de angulos
    def rotatePlayer(self, angle):
        x = self.rect.x
        y = self.rect.y
        self.rotation += angle
        self.image = pygame.transform.rotate(self.imageOriginal, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = x
        self.rect.y = y

        if (self.rotation > 360):
            self.rotation -= 360
        elif (self.rotation < 0):
            self.rotation += 360

    # rota al jugador a un angulo en especifico
    def rotatePlayerTo(self, angle):
        x = self.rect.x
        y = self.rect.y
        self.rotation = angle
        self.image = pygame.transform.rotate(self.imageOriginal, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = x
        self.rect.y = y

        if (self.rotation > 360):
            self.rotation -= 360
        elif (self.rotation < 0):
            self.rotation += 360

    # mueve al jugador hacia donde este rotado
    def movePlayer(self, mult = 1):
        rotation = self.rotation
        if rotation > 0 and rotation <= 90:
            self.rect.x -= math.ceil(mult * 5 * (rotation/90))
            self.rect.y -= math.ceil(mult * 5 * ((90 - rotation)/90))
        elif rotation > 90 and rotation <= 180:
            rotation -= 90
            self.rect.x -= math.ceil(mult * 10 * ((90 - rotation)/90))
            self.rect.y += math.ceil(mult * 10 * (rotation/90))
        elif rotation > 180 and rotation <= 270:
            rotation -= 180
            self.rect.x += math.ceil(mult * 10 * (rotation/90))
            self.rect.y += math.ceil(mult * 10 * ((90 - rotation)/90))
        else:
            rotation -= 270
            self.rect.x += math.ceil(mult * 10 * ((90 - rotation)/90))
            self.rect.y -= math.ceil(mult * 10 * (rotation/90))

# Ball(sprite)
# Se encarga de la creacion del gameobject de la pelota y el movimiento de este.
class Ball(pygame.sprite.Sprite):

    # init
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255,100,0))
        self.rect = self.image.get_rect()
        self.rect.center = (HEIGHT/2, WIDTH/2)
        self.rect.x = ball_x
        self.rect.y = ball_y
        self.accuracy = randint(-WIDTH/3,WIDTH/3) # hace que se pueda fallar
        self.printData = True

    # calcula la distancia a la porteria y tira el balon
    def kick_the_shit_out_of_it(self):
        distance_x = ball_x - WIDTH/2 + self.accuracy
        if distance_x < 0:
            to_move_x = math.floor(distance_x/ball_y) * 2
        else:
            to_move_x = math.ceil(distance_x/ball_y) * 2
        to_move_y = math.ceil(ball_y/abs(distance_x)) * 2
        if self.rect.y > 0:
            self.rect.y -= to_move_y
            self.rect.x -= to_move_x

        if self.printData:
            self.printData = False
            print((distance_x, ball_y, to_move_x, to_move_y, self.accuracy))

# methods for calculations

# calcula el angulo entre la pelota y el jugador
def ball_player_ang(gameobject, bx = ball_x, by = ball_y):
    triangle_x = bx - gameobject.rect.x
    triangle_y = by - gameobject.rect.y

    cuadrante = lambda x, y: 'RD' if (x == 1 and y == 1) else ('LD' if (x == -1 and y == 1) else ('LU' if (x ==-1 and y ==-1) else ('RU' if (x ==1 and y ==-1) else 0)))
    cua = cuadrante(sign(triangle_x), sign(triangle_y))
    if triangle_x == 0:
        angle = 0
    else:
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

    if toRotate > 180:
        return(toRotate - 360)
    if toRotate < -180:
        return(toRotate + 360)
    else:
        return(toRotate)

# calcula la distancia entre la pelota y el jugador
def get_distance(gameobject, bx = ball_x, by = ball_y):
    triangle_x = bx - gameobject.rect.x
    triangle_y = by - gameobject.rect.y
    return((triangle_x ** 2 + triangle_y ** 2)**(1/2))

# sprites
all_sprites = pygame.sprite.Group()
player = Player()   # jugador
ball = Ball()       # pelota
all_sprites.add(player)
all_sprites.add(ball)

# display loop
done = False
kick = False
while not done:
    # FPS
    clock.tick(FPS)

    # key and display controls
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True

    # player movement
    if kick == False:
        # rotation logic
        tmp_ang = ball_player_ang(player)
        near_ang = angle_is_near_viejo(abs(tmp_ang) * 2)
        half_ang = angle_is_half(abs(tmp_ang) * 2)
        away_ang = angle_is_wide(abs(tmp_ang) * 2)
        toRotate = max((near_ang,half_ang,away_ang))

        # movement logic
        tmp_distance = get_distance(player)
        near_ball = ball_is_close(tmp_distance)
        half_ball = ball_is_medium(tmp_distance)
        away_ball = ball_is_far(tmp_distance)
        toMove = max((near_ball, half_ang, away_ball))

        # execute movements
        if (tmp_ang < 0):
            player.rotatePlayer(toRotate * -10) # rotate to right
        else:
            player.rotatePlayer(toRotate * 10)  # rotate to left
        player.movePlayer(toMove)               # move

        # on position to kick
        if player.rect.x > ball_x - 5 and player.rect.x < ball_x + 5:
            if player.rect.y > ball_y - 5 and player.rect.y < ball_y + 5:
                kick = True

    # player kicks the ball
    if kick:
        ball.kick_the_shit_out_of_it()

        # stop game after throw
        if ball.rect.y <= 0:
            if ball.rect.x >= 100 and  ball.rect.x <= 200:
                print("GOAL!!!")
            else:
                print("Failed...")
            done = True;

    # update render
    screen.fill((0,0,0))
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(WIDTH/3, 0, WIDTH/3, 2))
    pygame.display.flip()

# quit pygames
time.sleep(1)
pygame.quit()
