import pygame


class InimigoMapa(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range):
        super().__init__()

        self.spritesheet = pygame.image.load('inimigo_mapa.png').convert_alpha()
        self.largura_sprite = 32
        self.altura_sprite = 32

        self.animations = {'down': [], 'left': [], 'right': [], 'up': []}
        self.carregar_animacoes()

        self.direcao = 'right'
        self.frame_atual = 1  # <-- ALTERADO (Começa no frame 1, pulando o 0)
        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150

        self.image = self.animations[self.direcao][self.frame_atual]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidade_movimento = 1

        self.spawn_x = x
        self.target_x = x + patrol_range
        self.patrol_state = 'outgoing'

        # --- RETÂNGULO DE DETECÇÃO ---
        self.detection_rect = self.rect.inflate(50, 50)

    def carregar_animacoes(self):
        for i in range(4): self.animations['down'].append(self.get_image(i * self.largura_sprite, 0))
        for i in range(4): self.animations['left'].append(self.get_image(i * self.largura_sprite, self.altura_sprite))
        for i in range(4): self.animations['right'].append(
            self.get_image(i * self.largura_sprite, 2 * self.altura_sprite))
        for i in range(4): self.animations['up'].append(self.get_image(i * self.largura_sprite, 3 * self.altura_sprite))

    def get_image(self, x, y):
        image = pygame.Surface((self.largura_sprite, self.altura_sprite), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, self.largura_sprite, self.altura_sprite))
        return image

    def update(self, paredes):
        # Patrulha
        if self.patrol_state == 'outgoing':
            self.rect.x += self.velocidade_movimento
            self.direcao = 'right'
            if self.rect.x >= self.target_x:
                self.patrol_state = 'returning'

        elif self.patrol_state == 'returning':
            self.rect.x -= self.velocidade_movimento
            self.direcao = 'left'
            if self.rect.x <= self.spawn_x:
                self.patrol_state = 'outgoing'

        # --- ATUALIZA A POSIÇÃO DO RETÂNGULO DE DETECÇÃO ---
        self.detection_rect.center = self.rect.center

        # Animação
        agora = pygame.time.get_ticks()
        if agora - self.ultima_atualizacao_anim > self.velocidade_animacao:
            self.ultima_atualizacao_anim = agora

            # --- BLOCO DE ANIMAÇÃO ALTERADO ---
            # Força um ciclo 1, 2, 1, 2...
            # Pula o frame 0 (parado) e o 3 (que deve estar quebrando)
            self.frame_atual += 1
            if self.frame_atual >= 3:  # Quando o frame vira 3...
                self.frame_atual = 1  # ...ele volta para o 1

        self.image = self.animations[self.direcao][self.frame_atual]