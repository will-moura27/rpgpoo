import pygame


class PlayerMapa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load('player.png').convert_alpha()

        self.largura_sprite = 32
        self.altura_sprite = 32

        self.animations = {
            'down': [], 'left': [], 'right': [], 'up': []
        }

        self.carregar_animacoes()

        self.direcao = 'down'
        self.frame_atual = 0
        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150

        self.image = self.animations[self.direcao][self.frame_atual]
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidade_movimento = 2

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

    # --- MÉTODO UPDATE REVERTIDO PARA A VERSÃO ESTÁVEL COM COLISÃO ---
    def update(self, paredes):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        movendo = (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])

        if keys[pygame.K_LEFT]:
            dx = -1; self.direcao = 'left'
        elif keys[pygame.K_RIGHT]:
            dx = 1; self.direcao = 'right'
        if keys[pygame.K_UP]:
            dy = -1; self.direcao = 'up'
        elif keys[pygame.K_DOWN]:
            dy = 1; self.direcao = 'down'

        # Animação (lógica original)
        agora = pygame.time.get_ticks()
        if not movendo:
            self.frame_atual = 0
        else:
            if agora - self.ultima_atualizacao_anim > self.velocidade_animacao:
                self.ultima_atualizacao_anim = agora
                self.frame_atual = (self.frame_atual + 1) % len(self.animations[self.direcao])

        self.image = self.animations[self.direcao][self.frame_atual]

        # Lógica de Colisão
        self.rect.x += dx * self.velocidade_movimento
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dx > 0: self.rect.right = parede.left
                if dx < 0: self.rect.left = parede.right

        self.rect.y += dy * self.velocidade_movimento
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dy > 0: self.rect.bottom = parede.top
                if dy < 0: self.rect.top = parede.bottom