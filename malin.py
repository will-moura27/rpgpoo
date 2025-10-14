import pygame
import random
from pytmx.util_pygame import load_pygame
from PlayerMapa import PlayerMapa
from Personagem import Personagem
from Inimigo import Inimigo
from Batalha import Batalha
from CONST import CLASSES


# --- CLASSES, FUNÇÕES E SETUP (sem alteração) ---
class TextoFlutuante(pygame.sprite.Sprite):
    def __init__(self, x, y, texto, cor):
        pygame.sprite.Sprite.__init__(self)
        self.fonte = pygame.font.Font(None, 35)
        self.image = self.fonte.render(texto, True, cor)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0

    def update(self):
        self.rect.y -= 1
        self.contador += 1
        if self.contador > 60: self.kill()


# ... (o resto das suas funções de desenho continuam aqui, sem alteração)

def desenhar_barra_de_vida(surface, x, y, vida_atual, vida_maxima):
    if vida_atual < 0: vida_atual = 0
    comprimento_barra = 200
    altura_barra = 20
    percentual_vida = vida_atual / vida_maxima if vida_maxima > 0 else 0
    pygame.draw.rect(surface, (255, 0, 0), (x, y, comprimento_barra, altura_barra))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, comprimento_barra * percentual_vida, altura_barra))


def desenhar_barra_de_stamina(surface, x, y, stamina_atual, stamina_maxima):
    if stamina_atual < 0: stamina_atual = 0
    comprimento_barra = 200
    altura_barra = 15
    percentual_stamina = stamina_atual / stamina_maxima if stamina_maxima > 0 else 0
    pygame.draw.rect(surface, (50, 50, 50), (x, y, comprimento_barra, altura_barra))
    pygame.draw.rect(surface, (0, 150, 255), (x, y, comprimento_barra * percentual_stamina, altura_barra))


def desenhar_texto(surface, texto, tamanho, x, y, cor=(255, 255, 255)):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x, y)
    surface.blit(texto_surface, texto_rect)


def desenhar_texto_com_contorno(surface, texto, tamanho, x, y, cor_principal, cor_contorno=(0, 0, 0)):
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor_principal)
    contorno_surface = fonte.render(texto, True, cor_contorno)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x, y)
    surface.blit(contorno_surface, (texto_rect.x - 1, texto_rect.y))
    surface.blit(contorno_surface, (texto_rect.x + 1, texto_rect.y))
    surface.blit(contorno_surface, (texto_rect.x, texto_rect.y - 1))
    surface.blit(contorno_surface, (texto_rect.x, texto_rect.y + 1))
    surface.blit(texto_surface, texto_rect)


# --- INICIALIZAÇÃO DO PYGAME ---
pygame.init()
pygame.mixer.init()
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Meu RPG Gráfico")

try:
    background_image = pygame.image.load('background.png').convert()
    background_image = pygame.transform.scale(background_image, (LARGURA_TELA, ALTURA_TELA))
except pygame.error:
    background_image = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    background_image.fill((20, 20, 40))
game_surface = pygame.Surface((LARGURA_TELA, ALTURA_TELA))

# --- CARREGANDO O MAPA E COLISÕES ---
tmx_data = load_pygame("mundo.tmx")
paredes = []
for obj in tmx_data.get_layer_by_name("Colisao"):
    parede = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    paredes.append(parede)

# --- VARIÁVEIS DE ESTADO E LOOP ---
rodando = True
clock = pygame.time.Clock()
game_state = "exploracao"

# --- OBJETOS DO MODO EXPLORAÇÃO ---
player_group = pygame.sprite.GroupSingle()
player_exploracao = PlayerMapa(LARGURA_TELA / 2, ALTURA_TELA / 2)
player_group.add(player_exploracao)

# --- Variáveis do modo Batalha e outros estados ---
# ... (o resto das suas variáveis continua aqui)
jogador = None
inimigo = None
batalha = None
botoes_ataque = {}
grupo_texto_flutuante = pygame.sprite.Group()
shake_duration = 0
shake_intensity = 4
tempo_do_ataque_inimigo = 0
mensagem_fim_de_jogo = ""
card_images = {}
for nome_classe in CLASSES.keys():
    try:
        filename = f"card_{nome_classe}.png"
        image = pygame.image.load(filename).convert()
        image = pygame.transform.scale(image, (150, 200))
        card_images[nome_classe] = image
    except pygame.error:
        image = pygame.Surface((150, 200))
        image.fill((140, 0, 211))
        card_images[nome_classe] = image
botoes_classe = {}
lista_classes = list(CLASSES.keys())
pos_x_inicial = 150
pos_y_inicial = 250
espacamento = 170
for i, nome_classe in enumerate(lista_classes):
    pos_x = pos_x_inicial + (i * espacamento)
    botao_rect = pygame.Rect(0, 0, 150, 200)
    botao_rect.center = (pos_x, pos_y_inicial)
    botoes_classe[nome_classe] = botao_rect
hovered_class = None

# --- GAME LOOP ---
while rodando:
    clock.tick(60)

    # --- LÓGICA DE EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        # (outros eventos)

    # --- LÓGICA DE ATUALIZAÇÃO ---
    if game_state == "exploracao":
        # Passa a lista de paredes para o método update
        player_group.update(paredes)

    # (outras lógicas de atualização para batalha, etc.)
    elif game_state == "batalha":
        # ...
        pass

    # --- LÓGICA DE DESENHO ---
    game_surface.fill((0, 0, 0))

    if game_state == "exploracao":
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    game_surface.blit(surf, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

        player_group.draw(game_surface)

    # (outras lógicas de desenho)
    elif game_state == "escolha_personagem":
        # ...
        pass
    elif game_state == "batalha":
        # ...
        pass

    tela.blit(game_surface, (0, 0))
    pygame.display.flip()

# --- FINALIZAÇÃO DO JOGO ---
pygame.quit()