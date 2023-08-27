import pygame, pgzero, pgzrun, random, sys
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
gameover_overlay = pygame.image.load('images/gameover.png')
    
# Variáveis globais
dt_global = 0
pontos = 0
gameover = False
velocidade = 0

# Música e sons
#  music.play('zapzap.wav')
#  music.set_volume(0.1)

# Cria retângulos de colisão nos tubos e no player
retangulo_player = passaro.get_rect()
retangulo_tubo1 = tubo_img.get_rect()
retangulo_tubo2 = tubo2_img.get_rect()

# Desenha na tela todos os objetos
def draw():
    global dt_global, gameover

    if not gameover:
        screen.blit(fundo, (fundo_x, fundo_y))
        screen.blit(nuvem, (nuvem_x, nuvem_y))
        screen.blit(nuvem, (nuvem_x+300, nuvem_y+200))
        screen.blit(nuvem, (nuvem_x+700, nuvem_y+500))
        passaro.pos = ((passaro_x, passaro_y))
        passaro.draw()
        screen.blit(tubo_img, (tubo_x, tubo_y))
        screen.blit(tubo2_img, (tubo2_x, tubo2_y))
        screen.draw.text(f"Tempo: {dt_global}", topright=(700, 20), color="#41E95F", fontname='matchuppro.ttf', fontsize=30, owidth=1.5, ocolor="#000000")
        screen.draw.text(f"Pontos: {pontos}", topright=(150, 20), color="#41E95F", fontname='matchuppro.ttf', fontsize=30, owidth=1.5, ocolor="#000000")
        screen.draw.text(f"Dt: {dt_global/10000}", topright=(300, 20), color="#41E95F", fontname='matchuppro.ttf', fontsize=30, owidth=1.5, ocolor="#000000")
    else:
        screen.blit(gameover_overlay, (0,0))

# Verifica e dar ações para as teclas
def on_key_down(key):
    global passaro_speed, passaro_y, gameover

    if key == keys.SPACE and gameover == False:
        passaro_speed -= random.uniform(200, 300)    
        sounds.asa.play()
        #passaro.animate()
    if key == keys.F and gameover == True:
        pygame.quit()
        sys.exit()

# Verificar e mostrar a tela de morte
def verificar_morte():
    global passaro_y, gameover

    if passaro_y < 0:
        gameover = True

# Muda o ângulo do pássaro para simular que está caindo melhor
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
    global tubo2_x, tubo2_y, tubo2_img
    global fundo_x , nuvem_x

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

# Verifica e soma os pontos
def verificar_pontos():
    global pontos, passando_entre_tubos

    if passaro_x > tubo_x-1 and passaro_x < tubo_x+1 :
        passando_entre_tubos = True
        pontos += 1
        sounds.ponto.play()        

# Detecta a colisao do player com os tubos e chama a morte
def colisao():
    global passaro_x, passaro_y, gameover
    global tubo_x, tubo_y
    global tubo2_x, tubo2_y
    global retangulo_player, retangulo_tubo1, retangulo_tubo2

    retangulo_player.x = passaro_x
    retangulo_player.y = passaro_y
    retangulo_tubo1.x = tubo_x
    retangulo_tubo1.y = tubo_y
    retangulo_tubo2.x = tubo2_x
    retangulo_tubo2.y = tubo2_y

    if retangulo_player.colliderect(retangulo_tubo1) or retangulo_player.colliderect(retangulo_tubo2):
        gameover = True

# Faz a atualização de todo o jogo
def update(dt):
    global dt_global, gameover
    
    if not gameover:
        virar_angulo()
        verificar_morte()
        andar_objetos(dt)    
        verificar_pontos()
        colisao()
        dt_global = pygame.time.get_ticks()        
    pass
 
# Inicia o jogo
pgzrun.go()