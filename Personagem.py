import pygame
from CONST import CLASSES, ATAQUES, ATAQUES_POR_CLASSE

class Personagem:
    def __init__(self, nome, classe, nivel, ataque, defesa, vida, ataques):
        # ... (seus atributos normais sem alteração)
        self.nome = nome
        self.classe = classe
        self.nivel = nivel
        self.ataque = ataque
        self.defesa = defesa
        self.vida = vida
        self.ataques = ataques
        self.stamina_jogador = 100
        self.max_stamina_jogador = 100
        self.vida_maxima = vida

        # --- SEÇÃO DE IMAGEM (sem alteração) ---
        self.image = pygame.image.load('mago.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 180))
        self.rect = self.image.get_rect()

        # --- NOVOS ATRIBUTOS PARA O EFEITO DE PISCAR ---
        self.flash_duration = 0
        self.flash_color = None

    # --- NOVO MÉTODO PARA ATIVAR O EFEITO ---
    def trigger_flash(self, color, duration):
        """Ativa o efeito de piscar com uma cor e duração específicas."""
        self.flash_color = color
        self.flash_duration = duration

    # --- NOVO MÉTODO DE ATUALIZAÇÃO ---
    def update(self):
        """Atualiza o estado do personagem a cada frame (por enquanto, só o timer do flash)."""
        if self.flash_duration > 0:
            self.flash_duration -= 1

    # O resto da classe (apresentacao, criacao_perso, etc.) continua exatamente igual...
    def apresentacao(self):
        # ...
        pass
    @staticmethod
    def criacao_perso():
        # ...
        return None
    @staticmethod
    def criacao_perso_teste(nome, classe):
        # ...
        if classe not in CLASSES: return None
        atributos = CLASSES[classe]
        lista_ataques = ATAQUES_POR_CLASSE.get(classe, [])
        return nome, classe, atributos["nivel"], atributos["ataque"], atributos["defesa"], atributos["vida"], lista_ataques