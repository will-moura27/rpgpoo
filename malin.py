import pygame
import random
from Personagem import Personagem
from Inimigo import Inimigo
from Batalha import Batalha
from CONST import CLASSES


# --- CLASSES, FUNÇÕES E SETUP ---
class TextoFlutuante(pygame.sprite.Sprite):
    # ... (código sem alteração)
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


def desenhar_barra_de_vida(surface, x, y, vida_atual, vida_maxima):
    # ... (código sem alteração)
    if vida_atual < 0: vida_atual = 0
    comprimento_barra = 200
    altura_barra = 20
    percentual_vida = vida_atual / vida_maxima if vida_maxima > 0 else 0
    pygame.draw.rect(surface, (255, 0, 0), (x, y, comprimento_barra, altura_barra))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, comprimento_barra * percentual_vida, altura_barra))


def desenhar_barra_de_stamina(surface, x, y, stamina_atual, stamina_maxima):
    # ... (código sem alteração)
    if stamina_atual < 0: stamina_atual = 0
    comprimento_barra = 200
    altura_barra = 15
    percentual_stamina = stamina_atual / stamina_maxima if stamina_maxima > 0 else 0
    pygame.draw.rect(surface, (50, 50, 50), (x, y, comprimento_barra, altura_barra))
    pygame.draw.rect(surface, (0, 150, 255), (x, y, comprimento_barra * percentual_stamina, altura_barra))


def desenhar_texto(surface, texto, tamanho, x, y, cor=(255, 255, 255)):
    # Esta é a nossa função original, a manteremos para textos sem contorno
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x, y)
    surface.blit(texto_surface, texto_rect)


# --- NOVA FUNÇÃO PARA TEXTO COM CONTORNO ---
def desenhar_texto_com_contorno(surface, texto, tamanho, x, y, cor_principal, cor_contorno=(0, 0, 0)):
    fonte = pygame.font.Font(None, tamanho)
    # Renderiza o texto principal e o do contorno
    texto_surface = fonte.render(texto, True, cor_principal)
    contorno_surface = fonte.render(texto, True, cor_contorno)

    # Pega o retângulo do texto principal e define sua posição central
    texto_rect = texto_surface.get_rect()
    texto_rect.center = (x, y)

    # Desenha o contorno deslocado em 4 direções
    surface.blit(contorno_surface, (texto_rect.x - 1, texto_rect.y))
    surface.blit(contorno_surface, (texto_rect.x + 1, texto_rect.y))
    surface.blit(contorno_surface, (texto_rect.x, texto_rect.y - 1))
    surface.blit(contorno_surface, (texto_rect.x, texto_rect.y + 1))

    # Desenha o texto principal por cima
    surface.blit(texto_surface, texto_rect)


# --- INICIALIZAÇÃO, SETUP E VARIÁVEIS (sem alteração) ---
pygame.init()
pygame.mixer.init()
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Meu RPG Gráfico")
background_image = pygame.image.load('background.png').convert()
background_image = pygame.transform.scale(background_image, (LARGURA_TELA, ALTURA_TELA))
game_surface = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
rodando = True
clock = pygame.time.Clock()
game_state = "escolha_personagem"
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
        print(f"Aviso: Imagem '{filename}' não encontrada. Usando cor sólida.")
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

    # --- LÓGICA DE EVENTOS (sem alteração) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if game_state == "escolha_personagem":
            if evento.type == pygame.MOUSEMOTION:
                pos_mouse = pygame.mouse.get_pos()
                hovered_class = None
                for nome_classe, botao_rect in botoes_classe.items():
                    if botao_rect.collidepoint(pos_mouse):
                        hovered_class = nome_classe
                        break
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                for nome_classe, botao_rect in botoes_classe.items():
                    if botao_rect.collidepoint(pos_mouse):
                        atributos_jogador = Personagem.criacao_perso_teste("Player", nome_classe)
                        jogador = Personagem(*atributos_jogador)
                        dados_inimigo = Inimigo.stats_ini()
                        inimigo = Inimigo(*dados_inimigo)
                        batalha = Batalha(jogador, inimigo)
                        jogador.rect.bottomleft = (40, 500)
                        inimigo.rect.topright = (750, 15)
                        game_state = "batalha"
                        try:
                            pygame.mixer.music.load('battle_music.mp3')
                            pygame.mixer.music.set_volume(0.5)
                            pygame.mixer.music.play(-1)
                        except pygame.error:
                            print("Aviso: Arquivo 'battle_music.mp3' não encontrado.")
        elif game_state == "batalha":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and batalha.turno_atual == "jogador":
                pos_mouse = pygame.mouse.get_pos()
                for acao, botao_rect in botoes_ataque.items():
                    if botao_rect.collidepoint(pos_mouse):
                        if acao == "passar_turno":
                            batalha.turno_atual = "inimigo"
                            tempo_do_ataque_inimigo = pygame.time.get_ticks()
                            break
                        else:
                            tipo_resultado, valor = batalha.turno_jogador(acao)
                            if tipo_resultado == "aviso":
                                aviso_texto = TextoFlutuante(jogador.rect.centerx, jogador.rect.top, str(valor),
                                                             (255, 255, 0))
                                grupo_texto_flutuante.add(aviso_texto)
                            else:
                                if tipo_resultado == "dano" and valor > 0:
                                    texto_dano = TextoFlutuante(inimigo.rect.centerx, inimigo.rect.top + 70, str(valor),
                                                                (255, 100, 100))
                                    grupo_texto_flutuante.add(texto_dano)
                                    inimigo.trigger_flash((255, 0, 0, 150), 20)
                                    shake_duration = 15
                                elif tipo_resultado == "cura":
                                    texto_cura = TextoFlutuante(jogador.rect.centerx, jogador.rect.top, f"+{valor}",
                                                                (0, 255, 0))
                                    grupo_texto_flutuante.add(texto_cura)
                                    jogador.trigger_flash((0, 255, 0, 120), 20)
                                if inimigo.vida <= 0:
                                    batalha.turno_atual = "fim_de_jogo"
                                    mensagem_fim_de_jogo = "Você Venceu!"
                                    pygame.mixer.music.stop()
                                else:
                                    batalha.turno_atual = "inimigo"
                                    tempo_do_ataque_inimigo = pygame.time.get_ticks()
                                break
    # --- LÓGICA DE ATUALIZAÇÃO (sem alteração) ---
    if game_state == "batalha":
        grupo_texto_flutuante.update()
        jogador.update()
        inimigo.update()
        if shake_duration > 0: shake_duration -= 1
        if batalha.turno_atual == "inimigo":
            if pygame.time.get_ticks() - tempo_do_ataque_inimigo > 1500:
                tipo_resultado, valor = batalha.turno_inimigo()
                if tipo_resultado == "dano" and valor > 0:
                    texto_dano_inimigo = TextoFlutuante(jogador.rect.centerx, jogador.rect.top, str(valor),
                                                        (255, 100, 100))
                    grupo_texto_flutuante.add(texto_dano_inimigo)
                    jogador.trigger_flash((255, 0, 0, 150), 20)
                    shake_duration = 15
                if jogador.vida <= 0:
                    batalha.turno_atual = "fim_de_jogo"
                    mensagem_fim_de_jogo = "Você Perdeu!"
                    pygame.mixer.music.stop()
                else:
                    batalha.turno_atual = "jogador"
                    batalha.reduzir_cooldowns()
                    batalha.regenerar_stamina()

    # --- LÓGICA DE DESENHO ---
    game_surface.blit(background_image, (0, 0))
    if game_state == "escolha_personagem":
        # --- SEÇÃO MODIFICADA ---
        # Agora usamos a nova função para desenhar com contorno
        desenhar_texto_com_contorno(game_surface, "Escolha sua Classe", 60, LARGURA_TELA / 2, 100, (255, 215, 0))

        for nome_classe, botao_rect in botoes_classe.items():
            game_surface.blit(card_images[nome_classe], botao_rect)

            cor_borda = (255, 255, 255) if nome_classe == hovered_class else (0, 0, 0)
            pygame.draw.rect(game_surface, cor_borda, botao_rect, 3, border_radius=15)

            desenhar_texto_com_contorno(game_surface, nome_classe.title(), 30, botao_rect.centerx, botao_rect.top + 20,
                                        (255, 255, 255))

            if nome_classe == hovered_class:
                stats = CLASSES[nome_classe]
                cor_dos_stats = (173, 216, 230)
                desenhar_texto_com_contorno(game_surface, f"HP: {stats['vida']}", 22, botao_rect.centerx,
                                            botao_rect.centery - 10, cor_dos_stats)
                desenhar_texto_com_contorno(game_surface, f"ATK: {stats['ataque']}", 22, botao_rect.centerx,
                                            botao_rect.centery + 15, cor_dos_stats)
                desenhar_texto_com_contorno(game_surface, f"DEF: {stats['defesa']}", 22, botao_rect.centerx,
                                            botao_rect.centery + 40, cor_dos_stats)

    elif game_state == "batalha":
        # ... (código de desenhar a batalha, sem alteração) ...
        game_surface.blit(jogador.image, jogador.rect)
        game_surface.blit(inimigo.image, inimigo.rect)
        if jogador.flash_duration > 0:
            overlay = pygame.Surface(jogador.rect.size, pygame.SRCALPHA)
            overlay.fill(jogador.flash_color)
            game_surface.blit(overlay, jogador.rect.topleft)
        if inimigo.flash_duration > 0:
            overlay = pygame.Surface(inimigo.rect.size, pygame.SRCALPHA)
            overlay.fill(inimigo.flash_color)
            game_surface.blit(overlay, inimigo.rect.topleft)
        grupo_texto_flutuante.draw(game_surface)
        desenhar_texto(game_surface, f"{jogador.nome} ({jogador.classe.title()})", 25, jogador.rect.centerx,
                       jogador.rect.bottom + 10)
        desenhar_texto(game_surface, "HP", 22, jogador.rect.right + 45, jogador.rect.bottom + 38)
        desenhar_texto(game_surface, "STM", 22, jogador.rect.right + 45, jogador.rect.bottom + 63)
        desenhar_barra_de_vida(game_surface, jogador.rect.left - 20, jogador.rect.bottom + 30, jogador.vida,
                               jogador.vida_maxima)
        desenhar_barra_de_stamina(game_surface, jogador.rect.left - 20, jogador.rect.bottom + 55,
                                  batalha.stamina_jogador, 100)
        desenhar_texto(game_surface, f"{inimigo.nome} ({inimigo.classe.title()})", 25, inimigo.rect.centerx,
                       inimigo.rect.top + 255)
        if batalha.stun_inimigo > 0:
            texto_stun = f"Atordoado: {batalha.stun_inimigo}t"
            desenhar_texto(game_surface, texto_stun, 22, inimigo.rect.centerx, inimigo.rect.top + 270,
                           cor=(255, 255, 0))
        desenhar_texto(game_surface, "HP", 22, inimigo.rect.left - 25, inimigo.rect.top + 210)
        desenhar_texto(game_surface, "STM", 22, inimigo.rect.left - 25, inimigo.rect.top + 233)
        desenhar_barra_de_vida(game_surface, inimigo.rect.left, inimigo.rect.top + 200, inimigo.vida,
                               inimigo.vida_maxima)
        desenhar_barra_de_stamina(game_surface, inimigo.rect.left, inimigo.rect.top + 225, batalha.stamina_inimigo, 100)
        if batalha.turno_atual == "jogador":
            menu_rect = pygame.Rect(LARGURA_TELA - 260, ALTURA_TELA - 260, 240, 260)
            raio_caixa = 15
            pygame.draw.rect(game_surface, (140, 0, 211), menu_rect, border_radius=raio_caixa)
            pygame.draw.rect(game_surface, (0, 0, 0), menu_rect, 3, border_radius=raio_caixa)
            pos_x_botao = menu_rect.centerx
            pos_y_botao = menu_rect.top + 30
            botoes_ataque.clear()
            for ataque_nome in jogador.ataques:
                botao_rect = pygame.Rect(0, 0, 140, 40)
                botao_rect.center = (pos_x_botao, pos_y_botao)
                raio_arredondamento = 10
                cooldown = batalha.cooldowns_jogador[ataque_nome]
                cor_botao = (70, 0, 105) if cooldown > 0 else (140, 0, 211)
                pygame.draw.rect(game_surface, cor_botao, botao_rect, border_radius=raio_arredondamento)
                pygame.draw.rect(game_surface, (0, 0, 0), botao_rect, 2, border_radius=raio_arredondamento)
                if cooldown > 0:
                    desenhar_texto(game_surface, str(cooldown), 40, botao_rect.centerx, botao_rect.centery)
                else:
                    tamanho_fonte = 25
                    fonte = pygame.font.Font(None, tamanho_fonte)
                    texto_largura, _ = fonte.size(ataque_nome.title())
                    while texto_largura > botao_rect.width - 15:
                        tamanho_fonte -= 1
                        fonte = pygame.font.Font(None, tamanho_fonte)
                        texto_largura, _ = fonte.size(ataque_nome.title())
                    desenhar_texto(game_surface, ataque_nome.title(), tamanho_fonte, botao_rect.centerx,
                                   botao_rect.centery)
                botoes_ataque[ataque_nome] = botao_rect
                pos_y_botao += 50
            passar_rect = pygame.Rect(0, 0, 140, 40)
            passar_rect.center = (pos_x_botao, pos_y_botao)
            pygame.draw.rect(game_surface, (50, 50, 50), passar_rect, border_radius=10)
            pygame.draw.rect(game_surface, (0, 0, 0), passar_rect, 2, border_radius=10)
            desenhar_texto(game_surface, "Passar Turno", 22, passar_rect.centerx, passar_rect.centery)
            botoes_ataque["passar_turno"] = passar_rect
        if batalha.turno_atual == "fim_de_jogo":
            overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            game_surface.blit(overlay, (0, 0))
            desenhar_texto(game_surface, mensagem_fim_de_jogo, 80, LARGURA_TELA / 2, ALTURA_TELA / 2)

    # --- DESENHAR A TELA VIRTUAL NA TELA PRINCIPAL ---
    offset = [0, 0]
    if shake_duration > 0:
        offset[0] = random.randint(-shake_intensity, shake_intensity)
        offset[1] = random.randint(-shake_intensity, shake_intensity)
    tela.blit(game_surface, offset)

    pygame.display.flip()

# --- FINALIZAÇÃO DO JOGO ---
pygame.quit()