import pygame, pgzero, pgzrun, random
from pgzhelper import *

# Tamanho da tela
WIDTH = 800
HEIGHT = 800

# Passaro variaveis
passaro_x = 200
passaro_y = 200
passaro_speed = 0

# Passaro actor e animação
passaro = Actor('twitter_bird')
passaro.scale = 0.1
passaro.images = ['twitter_bird','twitter_bird_1','twitter_bird_2', 'twitter_bird_3']
passaro.fps = 60

# Tubos
espaco_tubos = random.randint(50, 250)

tubo_img = pygame.image.load('images/tubo.png')
tubo_y = (900 - espaco_tubos) - random.randint(0, 100)
tubo_x = WIDTH-199
tubo2_img = pygame.image.load('images/tubo2.png')
tubo2_y = (-900 + espaco_tubos) + random.randint(0, 100)
tubo2_x = WIDTH-199

# Cenário
nuvem = pygame.image.load('images/nuvem.png')
nuvem_x = 700
nuvem_y = 100
fundo = pygame.image.load('images/fundo.png')
fundo_x = 0
fundo_y = 0
    
# vars globais
dt_global = 0
pontos = 0

# Música e sons
#  music.play('zapzap.wav')
#  music.set_volume(0.1)

def draw():
    global dt_global
    screen.fill((255, 255, 255))
    screen.blit(nuvem, (nuvem_x, nuvem_y))
    screen.blit(fundo, (fundo_x, fundo_y))
    screen.blit(nuvem, (nuvem_x+300, nuvem_y+200))
    screen.blit(nuvem, (nuvem_x+700, nuvem_y+500))
    passaro.pos = ((passaro_x, passaro_y))
    passaro.draw()
    screen.blit(tubo_img, (tubo_x, tubo_y))
    screen.blit(tubo2_img, (tubo2_x, tubo2_y))
    screen.draw.text(f"Tempo: {dt_global}", topright=(700, 20), color="#41E95F", fontname='matchuppro.ttf', fontsize=30, owidth=1.5, ocolor="#000000")
    screen.draw.text(f"Pontos: {pontos}", topright=(150, 20), color="#41E95F", fontname='matchuppro.ttf', fontsize=30, owidth=1.5, ocolor="#000000")
    screen.draw.text(f"Dt: {dt_global/10000}", topright=(300, 20), color="#41E95F", fontname='matchuppro.ttf', fontsize=30, owidth=1.5, ocolor="#000000")


#Verificar e fazer o passaro voar
def on_key_down(key):
    global passaro_speed, passaro_y
    if key == keys.SPACE and passaro_y < HEIGHT-200:
        passaro_speed -= random.uniform(200, 300)
        
        sounds.asa.play()

#Verificar e mostrar a tela de morte
def verificar_morte():
    global passaro_y
    if passaro_y < 0:
        print("Game Over")

#"Anima" o passaro para simular que está caindo melhor
def virar_angulo():
    global passaro_speed
    if passaro_speed > 0 and passaro.angle > -90:
        passaro.angle -= random.uniform(0.5, 1)
    elif passaro_speed < 0 and passaro.angle < 20:
        passaro.angle += random.uniform(0.5, 1)

# Função que faz os objetos (cenário, tubos e nuvens) andarem na tela
def andar_objetos(dt):
    global passaro_y, passaro_speed, dt_global
    global tubo_x, tubo_y, tubo_img, espaco_tubos
    global tubo2_x, tubo2_y, tubo2_img, nuvem_x
    global fundo_x
    if tubo_x > -100:
        tubo_x -= int(165 * dt)
    else:
        tubo_x = WIDTH - tubo_x + 300    
        espaco_tubos = random.randint(50, 100)
        tubo_y = (900 - espaco_tubos) - random.randint(0, 100)
    if tubo2_x > -100:
        tubo2_x -= int(165 * dt)
    else:
        tubo2_x = WIDTH - tubo2_x + 300
        espaco_tubos = random.randint(50, 100)
        tubo2_y = (-900 + espaco_tubos) + random.randint(0, 100)
    if nuvem_x>-237:
        nuvem_x -= int(100 * dt)
    else:
        nuvem_x = WIDTH+237
    if fundo_x>-1120:
        fundo_x -= int(70 * dt)
    else:
        fundo_x = 0
    passaro_speed += random.uniform(300, 400) * dt
    passaro_y += passaro_speed * dt

#Verifica e soma os pontos
def verificar_pontos():
    global pontos
    if passaro_x > tubo_x-1  and passaro_x < tubo_x+1:
        pontos += 1
        sounds.ponto.play()

def update(dt):
    global dt_global
    passaro.animate()
    virar_angulo()
    verificar_morte()
    andar_objetos(dt)    
    verificar_pontos()
    dt_global = pygame.time.get_ticks()
    
    '''if passaro.collidepoint_pixel(  ):
        print('col')'''
    pass

pgzrun.go()