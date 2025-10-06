import pygame
from CONST import DANOS_ATK_INI, ATRIBUTO_INIMIGO, ATAQUES_INIMIGO

class Inimigo:
    def __init__(self, nome, vida, ataque, defesa, nivel, classe, ataques):
        # Atributos do jogo (sem alteração)
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.nivel = nivel
        self.classe = classe
        self.ataques = ataques
        self.vida_maxima = vida

        # --- SEÇÃO DE IMAGEM (sem alteração) ---
        self.image = pygame.image.load('mago_negro.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 200))
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
        """Atualiza o estado do inimigo a cada frame (por enquanto, só o timer do flash)."""
        if self.flash_duration > 0:
            self.flash_duration -= 1

    # O resto da classe (apresentacao_ini, stats_ini) continua exatamente igual...
    def apresentacao_ini(self):
        print(f"=== Inimigo ===")
        print(f"Nome: {self.nome}")
        # ... (resto do seu método)

    @staticmethod
    def stats_ini():
        classe = "Mago Negro"
        if classe not in ATRIBUTO_INIMIGO:
            return None
        nome = "Mago das Trevas"
        atributos = ATRIBUTO_INIMIGO[classe]
        lista_ataques = ATAQUES_INIMIGO.get(classe, [])
        return (nome, atributos["vida"], atributos["ataque"], atributos["defesa"], atributos["nivel"], classe, lista_ataques)