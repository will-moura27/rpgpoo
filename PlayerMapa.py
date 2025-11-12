import pygame


class PlayerMapa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.spritesheet = pygame.image.load('player.png').convert_alpha()
        self.largura_sprite = 32
        self.altura_sprite = 32

        # O dicionário de animações ainda é útil para sabermos quantos quadros existem por direção
        self.animations = {'down': [], 'left': [], 'right': [], 'up': []}
        self.carregar_animacoes_placeholder()  # Apenas para contar os quadros

        self.direcao = 'down'
        self.frame_atual = 0
        self.ultima_atualizacao_anim = pygame.time.get_ticks()
        self.velocidade_animacao = 150

        # Define a imagem inicial (será recriada no primeiro update)
        self.image = pygame.Surface((self.largura_sprite, self.altura_sprite), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

        self.velocidade_movimento = 2

    def carregar_animacoes_placeholder(self):
        """Preenche as listas com placeholders apenas para sabermos o comprimento da animação."""
        for i in range(4): self.animations['down'].append(None)
        for i in range(4): self.animations['left'].append(None)
        for i in range(4): self.animations['right'].append(None)
        for i in range(4): self.animations['up'].append(None)

    def get_image(self, x, y):
        """Corta uma imagem fresca do spritesheet a cada chamada."""
        image = pygame.Surface((self.largura_sprite, self.altura_sprite), pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), (x, y, self.largura_sprite, self.altura_sprite))
        return image

    def update(self, paredes):
        # 1. LER O TECLADO E DEFINIR VETOR DE MOVIMENTO
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        movendo = (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN])

        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1

        # 2. ATUALIZAR A DIREÇÃO E O QUADRO DA ANIMAÇÃO
        direcao_anterior = self.direcao

        if dx > 0:
            self.direcao = 'right'
        elif dx < 0:
            self.direcao = 'left'
        elif dy > 0:
            self.direcao = 'down'
        elif dy < 0:
            self.direcao = 'up'

        if self.direcao != direcao_anterior:
            self.frame_atual = 1

        agora = pygame.time.get_ticks()
        if not movendo:
            self.frame_atual = 0
        else:
            if agora - self.ultima_atualizacao_anim > self.velocidade_animacao:
                self.ultima_atualizacao_anim = agora
                self.frame_atual += 1

                # AQUI ESTÁ A CORREÇÃO:
                if self.frame_atual >= 3:  # <-- ALTERADO (Era len(self.animations[self.direcao]) que é 4)
                    self.frame_atual = 1

        # --- A CORREÇÃO CRUCIAL ESTÁ AQUI ---
        # Recorta a imagem correta DIRETAMENTE do spritesheet a cada frame.
        mapa_direcao_linha = {'down': 0, 'left': 1, 'right': 2, 'up': 3}
        linha_y = mapa_direcao_linha[self.direcao]
        x_coord = self.frame_atual * self.largura_sprite
        y_coord = linha_y * self.altura_sprite
        self.image = self.get_image(x_coord, y_coord)

        # 3. MOVER E COLIDIR
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