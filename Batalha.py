import random
from CONST import ATAQUES, DANOS_ATK_INI


class Batalha:
    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo
        self.cooldowns_jogador = {atk: 0 for atk in jogador.ataques}
        self.cooldowns_inimigo = {atk: 0 for atk in inimigo.ataques}
        self.stamina_jogador = 100
        self.stamina_inimigo = 100
        self.stun_inimigo = 0
        self.bloqueio_ativo = 0
        self.jogo_terminado = False

    def turno_jogador(self, ataque_nome):
        dados = ATAQUES[ataque_nome]
        # Se o ataque for inválido, retorna uma mensagem de erro
        if self.cooldowns_jogador[ataque_nome] > 0:
            return ("aviso", "Em Cooldown!")
        if self.stamina_jogador < dados["stamina"]:
            return ("aviso", "Sem Stamina!")

        # Se for válido, o resto do código continua
        self.cooldowns_jogador[ataque_nome] = dados["intervalo"]
        self.stamina_jogador -= dados["stamina"]

        if "cura" in dados:
            cura = dados["cura"]
            self.jogador.vida = min(self.jogador.vida_maxima, self.jogador.vida + cura)
            return ("cura", cura)
        elif "bloqueio" in dados:
            self.bloqueio_ativo = dados["bloqueio"]
            return ("texto", "Bloqueio Ativado!")
        elif "stun" in dados:
            if random.random() < 0.7:
                self.stun_inimigo = dados["stun"]
                return ("texto", "Atordoado!")
            else:
                return ("texto", "Falhou!")
        else:
            dano = dados["dano"] + self.jogador.ataque - self.inimigo.defesa
            dano = max(dano, 0)
            self.inimigo.vida -= dano
            return ("dano", dano)

    def turno_inimigo(self):
        if self.stun_inimigo > 0:
            self.stun_inimigo -= 1
            return ("texto", "Atordoado!")

        ataques_disponiveis = [atk for atk in self.inimigo.ataques if
                               self.cooldowns_inimigo[atk] == 0 and self.stamina_inimigo >= DANOS_ATK_INI[atk][
                                   "stamina"]]
        if not ataques_disponiveis: return ("texto", "")

        ataque = random.choice(ataques_disponiveis)
        dados = DANOS_ATK_INI[ataque]
        self.cooldowns_inimigo[ataque] = dados["intervalo"]
        self.stamina_inimigo -= dados["stamina"]

        dano = max(0, dados['dano'] + self.inimigo.ataque - self.jogador.defesa)
        if self.bloqueio_ativo > 0:
            dano -= self.bloqueio_ativo
            dano = max(dano, 0)
            self.bloqueio_ativo = 0
        self.jogador.vida -= dano
        return ("dano", dano)

    def reduzir_cooldowns(self):
        for dicionario in [self.cooldowns_jogador, self.cooldowns_inimigo]:
            for atk in dicionario:
                if dicionario[atk] > 0:
                    dicionario[atk] -= 1

    def regenerar_stamina(self):
        self.stamina_jogador = min(self.stamina_jogador + 10, 100)
        self.stamina_inimigo = min(self.stamina_inimigo + 10, 100)