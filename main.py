from pygame import *
import sys

init()

LARGURA = 800
ALTURA = 600
TAMANHO_TILE = 48
FPS = 60

tela = display.set_mode((LARGURA, ALTURA))
relogio = time.Clock()


def cria_tile_grama():
    tile = Surface((TAMANHO_TILE, TAMANHO_TILE))
    tile.fill((56, 142, 60))
    draw.rect(tile, (46, 125, 50), (0, 0, TAMANHO_TILE, TAMANHO_TILE), 2)
    draw.line(tile, (46, 125, 50), (0, TAMANHO_TILE // 2), (TAMANHO_TILE, TAMANHO_TILE // 2), 1)
    draw.line(tile, (46, 125, 50), (TAMANHO_TILE // 2, 0), (TAMANHO_TILE // 2, TAMANHO_TILE), 1)
    return tile


def cria_tile_parede():
    tile = Surface((TAMANHO_TILE, TAMANHO_TILE))
    tile.fill((117, 117, 117))
    draw.rect(tile, (80, 80, 80), (1, 1, 22, 22))
    draw.rect(tile, (80, 80, 80), (25, 25, 22, 22))
    draw.rect(tile, (80, 80, 80), (25, 1, 22, 22))
    draw.rect(tile, (80, 80, 80), (1, 25, 22, 22))
    draw.rect(tile, (60, 60, 60), (0, 0, TAMANHO_TILE, TAMANHO_TILE), 2)
    return tile


def cria_tile_agua():
    tile = Surface((TAMANHO_TILE, TAMANHO_TILE))
    tile.fill((25, 118, 210))
    draw.ellipse(tile, (66, 165, 245), (5, 12, 18, 8))
    draw.ellipse(tile, (66, 165, 245), (24, 28, 18, 8))
    return tile


def cria_tile_areia():
    tile = Surface((TAMANHO_TILE, TAMANHO_TILE))
    tile.fill((212, 180, 100))
    draw.circle(tile, (190, 155, 75), (14, 14), 4)
    draw.circle(tile, (190, 155, 75), (36, 32), 3)
    return tile


def cria_frames_personagem():
    frames = {}
    for direcao in ['down', 'up', 'left', 'right']:
        lista_frames = []
        for f in range(4):
            imagem = Surface((32, 40), SRCALPHA)

            alt_esq = 14 + (4 if f in [1, 3] else 0)
            alt_dir = 14 + (4 if f in [0, 2] else 0)
            draw.rect(imagem, (30, 60, 120), (8, 24, 7, alt_esq))
            draw.rect(imagem, (30, 60, 120), (17, 24, 7, alt_dir))

            draw.rect(imagem, (33, 150, 243), (6, 14, 20, 16))
            draw.rect(imagem, (255, 200, 150), (8, 2, 16, 14))
            draw.rect(imagem, (80, 50, 20), (7, 1, 18, 5))

            if direcao == 'down':
                draw.rect(imagem, (0, 0, 0), (11, 10, 3, 3))
                draw.rect(imagem, (0, 0, 0), (18, 10, 3, 3))
            elif direcao == 'left':
                draw.rect(imagem, (0, 0, 0), (10, 10, 3, 3))
            elif direcao == 'right':
                draw.rect(imagem, (0, 0, 0), (19, 10, 3, 3))

            lista_frames.append(imagem)
        frames[direcao] = lista_frames
    return frames


def carregar_mapa(nome_arquivo):
    mapa = []
    arquivo = open(nome_arquivo, 'r')
    for linha in arquivo:
        linha = linha.strip()
        if linha != '':
            numeros = linha.split(',')
            linha_mapa = []
            for n in numeros:
                linha_mapa.append(int(n))
            mapa.append(linha_mapa)
    arquivo.close()
    return mapa


def checar_colisao(retangulo, mapa, tiles_solidos):
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            if mapa[linha][coluna] in tiles_solidos:
                retangulo_tile = Rect(coluna * TAMANHO_TILE, linha * TAMANHO_TILE, TAMANHO_TILE, TAMANHO_TILE)
                if retangulo.colliderect(retangulo_tile):
                    return True, retangulo_tile
    return False, None


tile_grama = cria_tile_grama()
tile_parede = cria_tile_parede()
tile_agua = cria_tile_agua()
tile_areia = cria_tile_areia()

tiles_dict = {
    0: tile_grama,
    1: tile_parede,
    2: tile_agua,
    3: tile_areia,
}

tiles_solidos = [1, 2]

frames_personagem = cria_frames_personagem()

mapa = carregar_mapa('mapa.txt')

LARGURA_MAPA = len(mapa[0]) * TAMANHO_TILE
ALTURA_MAPA = len(mapa) * TAMANHO_TILE

camera_x = 0
camera_y = 0

PW = 32
PH = 40
jogador = Rect(
    2 * TAMANHO_TILE + (TAMANHO_TILE - PW) // 2,
    2 * TAMANHO_TILE + (TAMANHO_TILE - PH) // 2,
    PW, PH
)

direcao = 'down'
frame_atual = 0
timer_animacao = 0
VELOCIDADE = 3

running = True
while running:
    dt = relogio.tick(FPS)

    for ev in event.get():
        if ev.type == QUIT:
            running = False
        elif ev.type == KEYDOWN and ev.key == K_ESCAPE:
            running = False

    keys = key.get_pressed()
    dx = 0
    dy = 0
    movendo = False

    if keys[K_LEFT] or keys[K_a]:
        dx = -VELOCIDADE
        direcao = 'left'
        movendo = True
    elif keys[K_RIGHT] or keys[K_d]:
        dx = VELOCIDADE
        direcao = 'right'
        movendo = True

    if keys[K_UP] or keys[K_w]:
        dy = -VELOCIDADE
        direcao = 'up'
        movendo = True
    elif keys[K_DOWN] or keys[K_s]:
        dy = VELOCIDADE
        direcao = 'down'
        movendo = True

    jogador.x = jogador.x + dx
    colidiu, tile_rect = checar_colisao(jogador, mapa, tiles_solidos)
    if colidiu:
        if dx > 0:
            jogador.right = tile_rect.left
        else:
            jogador.left = tile_rect.right

    jogador.y = jogador.y + dy
    colidiu, tile_rect = checar_colisao(jogador, mapa, tiles_solidos)
    if colidiu:
        if dy > 0:
            jogador.bottom = tile_rect.top
        else:
            jogador.top = tile_rect.bottom

    if movendo:
        timer_animacao = timer_animacao + dt
        if timer_animacao >= 120:
            timer_animacao = 0
            frame_atual = (frame_atual + 1) % 4
    else:
        frame_atual = 0
        timer_animacao = 0

    camera_x = jogador.centerx - LARGURA // 2
    camera_y = jogador.centery - ALTURA // 2

    if camera_x < 0:
        camera_x = 0
    if camera_y < 0:
        camera_y = 0
    if camera_x > LARGURA_MAPA - LARGURA:
        camera_x = LARGURA_MAPA - LARGURA
    if camera_y > ALTURA_MAPA - ALTURA:
        camera_y = ALTURA_MAPA - ALTURA

    tela.fill((20, 20, 20))

    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])):
            id_tile = mapa[linha][coluna]
            tile_surf = tiles_dict[id_tile]
            pos_x = coluna * TAMANHO_TILE - camera_x
            pos_y = linha * TAMANHO_TILE - camera_y
            tela.blit(tile_surf, (pos_x, pos_y))

    imagem_jogador = frames_personagem[direcao][frame_atual]
    tela.blit(imagem_jogador, (jogador.x - camera_x, jogador.y - camera_y))

    display.flip()

quit()
sys.exit()