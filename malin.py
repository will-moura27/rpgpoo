import pygame
import random  # Precisamos importar a biblioteca random
from Personagem import Personagem
from Inimigo import Inimigo
from Batalha import Batalha


# --- CLASSES, FUNÇÕES E SETUP (sem alteração até a inicialização) ---
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
        if self.contador > 60:
            self.kill()


def desenhar_barra_de_vida(surface, x, y, vida_atual, vida_maxima):
    # ... (código sem alteração)
    if vida_atual < 0:
        vida_atual = 0
    comprimento_barra = 200
    altura_barra = 20
    percentual_vida = vida_atual / vida_maxima if vida_maxima > 0 else 0
    pygame.draw.rect(surface, (255, 0, 0), (x, y, comprimento_barra, altura_barra))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, comprimento_barra * percentual_vida, altura_barra))


def desenhar_barra_de_stamina(surface, x, y, stamina_atual, stamina_maxima):
    # ... (código sem alteração)
    if stamina_atual < 0:
        stamina_atual = 0
    comprimento_barra = 200
    altura_barra = 15
    percentual_stamina = stamina_atual / stamina_maxima if stamina_maxima > 0 else 0
    pygame.draw.rect(surface, (50, 50, 50), (x, y, comprimento_barra, altura_barra))
    pygame.draw.rect(surface, (0, 150, 255), (x, y, comprimento_barra * percentual_stamina, altura_barra))


def desenhar_texto(surface, texto, tamanho, x, y):
    # ... (código sem alteração)
    fonte = pygame.font.Font(None, tamanho)
    texto_surface = fonte.render(texto, True, (255, 255, 255))
    texto_rect = texto_surface.get_rect()
    texto_rect.midtop = (x, y)
    surface.blit(texto_surface, texto_rect)


# --- INICIALIZAÇÃO DO PYGAME ---
pygame.init()
LARGURA_TELA, ALTURA_TELA = 800, 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Meu RPG Gráfico")

# --- NOVA SUPERFÍCIE PARA O JOGO ---
# Esta é a nossa "tela virtual" onde tudo será desenhado
game_surface = pygame.Surface((LARGURA_TELA, ALTURA_TELA))

# --- CRIAÇÃO DOS PERSONAGENS E BATALHA (sem alteração) ---
atributos_jogador = Personagem.criacao_perso_teste("Player", "mago")
jogador = Personagem(*atributos_jogador)
dados_inimigo = Inimigo.stats_ini()
inimigo = Inimigo(*dados_inimigo)
batalha = Batalha(jogador, inimigo)
turno_atual = "jogador"
jogador.rect.bottomleft = (40, 500)
inimigo.rect.topright = (750, 15)

# --- VARIÁVEIS DO GAME LOOP ---
rodando = True
clock = pygame.time.Clock()
botoes_ataque = {}
tempo_do_ataque_inimigo = 0
mensagem_fim_de_jogo = ""
grupo_texto_flutuante = pygame.sprite.Group()

# --- NOVAS VARIÁVEIS PARA O EFEITO DE TREMOR ---
shake_duration = 0
shake_intensity = 4  # Quão forte é a tremida

# --- GAME LOOP ---
while rodando:
    clock.tick(60)

    # --- 1. CHECAR EVENTOS ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and turno_atual == "jogador":
                pos_mouse = pygame.mouse.get_pos()
                for ataque_nome, botao_rect in botoes_ataque.items():
                    if botao_rect.collidepoint(pos_mouse):
                        tipo_resultado, valor = batalha.turno_jogador(ataque_nome)
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
                                # ATIVAR A TREMIDA DA TELA
                                shake_duration = 15
                            elif tipo_resultado == "cura":
                                texto_cura = TextoFlutuante(jogador.rect.centerx, jogador.rect.top, f"+{valor}",
                                                            (0, 255, 0))
                                grupo_texto_flutuante.add(texto_cura)
                                jogador.trigger_flash((0, 255, 0, 120), 20)
                            if inimigo.vida <= 0:
                                turno_atual = "fim_de_jogo"
                                mensagem_fim_de_jogo = "Você Venceu!"
                            else:
                                turno_atual = "inimigo"
                                tempo_do_ataque_inimigo = pygame.time.get_ticks()
                            break

    # --- 2. LÓGICA DO JOGO (ATUALIZAÇÕES) ---
    grupo_texto_flutuante.update()
    jogador.update()
    inimigo.update()

    # ATUALIZAR O TIMER DA TREMIDA
    if shake_duration > 0:
        shake_duration -= 1

    if turno_atual == "inimigo":
        if pygame.time.get_ticks() - tempo_do_ataque_inimigo > 1500:
            tipo_resultado, valor = batalha.turno_inimigo()
            if tipo_resultado == "dano" and valor > 0:
                texto_dano_inimigo = TextoFlutuante(jogador.rect.centerx, jogador.rect.top, str(valor), (255, 100, 100))
                grupo_texto_flutuante.add(texto_dano_inimigo)
                jogador.trigger_flash((255, 0, 0, 150), 20)
                # ATIVAR A TREMIDA DA TELA
                shake_duration = 15
            if jogador.vida <= 0:
                turno_atual = "fim_de_jogo"
                mensagem_fim_de_jogo = "Você Perdeu!"
            else:
                turno_atual = "jogador"
                batalha.reduzir_cooldowns()
                batalha.regenerar_stamina()

    # --- 3. DESENHAR TUDO NA "TELA VIRTUAL" (game_surface) ---
    # Note que todos os "tela." foram trocados por "game_surface."
    game_surface.fill((20, 20, 40))
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
    desenhar_texto(game_surface, "HP", 22, jogador.rect.right + 45, jogador.rect.bottom + 28)
    desenhar_texto(game_surface, "STM", 22, jogador.rect.right + 45, jogador.rect.bottom + 53)
    desenhar_barra_de_vida(game_surface, jogador.rect.left - 20, jogador.rect.bottom + 30, jogador.vida,
                           jogador.vida_maxima)
    desenhar_barra_de_stamina(game_surface, jogador.rect.left - 20, jogador.rect.bottom + 55, batalha.stamina_jogador,
                              100)
    desenhar_texto(game_surface, f"{inimigo.nome} ({inimigo.classe.title()})", 25, inimigo.rect.centerx,
                   inimigo.rect.top + 245)
    desenhar_texto(game_surface, "HP", 22, inimigo.rect.left - 25, inimigo.rect.top + 198)
    desenhar_texto(game_surface, "STM", 22, inimigo.rect.left - 25, inimigo.rect.top + 223)
    desenhar_barra_de_vida(game_surface, inimigo.rect.left, inimigo.rect.top + 200, inimigo.vida, inimigo.vida_maxima)
    desenhar_barra_de_stamina(game_surface, inimigo.rect.left, inimigo.rect.top + 225, batalha.stamina_inimigo, 100)

    if turno_atual == "jogador":
        # ... (código da UI de batalha desenha na game_surface) ...
        menu_rect = pygame.Rect(LARGURA_TELA - 260, ALTURA_TELA - 210, 240, 210)
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
            pygame.draw.rect(game_surface, (140, 0, 211), botao_rect, border_radius=raio_arredondamento)
            pygame.draw.rect(game_surface, (0, 0, 0), botao_rect, 2, border_radius=raio_arredondamento)
            desenhar_texto(game_surface, ataque_nome.title(), 25, botao_rect.centerx, botao_rect.centery - 10)
            botoes_ataque[ataque_nome] = botao_rect
            pos_y_botao += 50

    if turno_atual == "fim_de_jogo":
        # ... (tela de fim de jogo desenha na game_surface) ...
        overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        game_surface.blit(overlay, (0, 0))
        desenhar_texto(game_surface, mensagem_fim_de_jogo, 80, LARGURA_TELA / 2, ALTURA_TELA / 3)

    # --- 4. DESENHAR A TELA VIRTUAL NA TELA PRINCIPAL (COM O EFEITO DE TREMOR) ---
    offset = [0, 0]
    if shake_duration > 0:
        offset[0] = random.randint(-shake_intensity, shake_intensity)
        offset[1] = random.randint(-shake_intensity, shake_intensity)

    # Copia a game_surface (com tudo desenhado) para a tela principal, com o desvio
    tela.blit(game_surface, offset)

    pygame.display.flip()

# --- FINALIZAÇÃO DO JOGO ---
pygame.quit()