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

    def mostrar_ataques(self):
        print("\nSeus ataques:")
        for i, atk in enumerate(self.jogador.ataques, 1):
            dados = ATAQUES[atk]
            cooldown = self.cooldowns_jogador[atk]
            print(f"{i}. {atk.title()} (Dano: {dados['dano']}, Cooldown: {cooldown}, Stamina: {dados['stamina']})")

    def turno_jogador(self):
        # Verifica se há ataques disponíveis com stamina suficiente e cooldown zero
        ataques_disponiveis = [
            atk for atk in self.jogador.ataques
            if self.cooldowns_jogador[atk] == 0 and self.stamina_jogador >= ATAQUES[atk]["stamina"]
        ]

        if len(ataques_disponiveis) == 0:
            if self.stamina_jogador == 0:
                print("Sua stamina zerou! Você está exausto e perdeu o jogo.")
                self.jogo_terminado = True
                return
            else:
                print("Você não tem stamina suficiente para usar nenhum ataque. Você perdeu o turno e está se recuperando...")
                self.regenerar_stamina()  # Regenera stamina normalmente no turno perdido
                return

        self.mostrar_ataques()
        while True:
            try:
                escolha = int(input("Escolha seu ataque (número): ")) - 1
                ataque_nome = self.jogador.ataques[escolha]
                dados = ATAQUES[ataque_nome]

                if self.cooldowns_jogador[ataque_nome] > 0:
                    print("Esse ataque ainda está em cooldown.")
                    continue
                if self.stamina_jogador < dados["stamina"]:
                    print("Stamina insuficiente.")
                    continue
                break
            except:
                print("Escolha inválida.")

        print(f"\nVocê usou {ataque_nome.title()}!")
        self.cooldowns_jogador[ataque_nome] = dados["intervalo"]
        self.stamina_jogador -= dados["stamina"]

        if "cura" in dados:
            cura = dados["cura"]
            self.jogador.vida += cura
            print(f"Você se curou em {cura} de vida!")
        elif "bloqueio" in dados:
            self.bloqueio_ativo = dados["bloqueio"]
            print(f"Você ativou um bloqueio de {self.bloqueio_ativo} de dano!")
        elif "stun" in dados:
            if random.random() < 0.7:
                self.stun_inimigo = dados["stun"]
                print(f"O inimigo foi atordoado e perderá o próximo turno!")
            else:
                print("O ataque de stun falhou!")
        else:
            dano = dados["dano"] + self.jogador.ataque - self.inimigo.defesa
            dano = max(dano, 0)
            self.inimigo.vida -= dano
            print(f"Você causou {dano} de dano ao inimigo!")

    def turno_inimigo(self):
        if self.stun_inimigo > 0:
            print("O inimigo está atordoado e perdeu o turno!")
            self.stun_inimigo -= 1
            return

        ataques_disponiveis = [atk for atk in self.inimigo.ataques if self.cooldowns_inimigo[atk] == 0 and self.stamina_inimigo >= DANOS_ATK_INI[atk]["stamina"]]
        if not ataques_disponiveis:
            print("O inimigo está sem stamina ou ataques disponíveis!")
            return

        ataque = random.choice(ataques_disponiveis)
        dados = DANOS_ATK_INI[ataque]
        self.cooldowns_inimigo[ataque] = dados["intervalo"]
        self.stamina_inimigo -= dados["stamina"]

        print(f"O inimigo usou {ataque.title()}!")
        dano_base = dados["dano"]
        ataque_total = self.inimigo.ataque
        defesa_total = self.jogador.defesa

        dano = max(0, int(dano_base * (ataque_total / (ataque_total + defesa_total))))

        if self.bloqueio_ativo > 0:
            dano -= self.bloqueio_ativo
            dano = max(dano, 0)
            print(f"Você bloqueou parte do dano! Dano final: {dano}")
            self.bloqueio_ativo = 0

        self.jogador.vida -= max(dano, 0)
        print(f"O inimigo causou {dano} de dano em você!")

    def reduzir_cooldowns(self):
        for dicionario in [self.cooldowns_jogador, self.cooldowns_inimigo]:
            for atk in dicionario:
                if dicionario[atk] > 0:
                    dicionario[atk] -= 1

    def regenerar_stamina(self):
        self.stamina_jogador = min(self.stamina_jogador + 10, 100)
        self.stamina_inimigo = min(self.stamina_inimigo + 10, 100)

    def mostrar_status(self):
        print(f"\n{self.jogador.nome}: {self.jogador.vida} HP, {self.stamina_jogador} STAMINA")
        print(f"{self.inimigo.nome}: {self.inimigo.vida} HP, {self.stamina_inimigo} STAMINA\n")

    def iniciar(self):
        while self.jogador.vida > 0 and self.inimigo.vida > 0 and not self.jogo_terminado:
            self.mostrar_status()
            self.turno_jogador()
            if self.jogo_terminado or self.inimigo.vida <= 0:
                break
            self.turno_inimigo()
            self.reduzir_cooldowns()
            self.regenerar_stamina()

        if self.jogador.vida > 0 and not self.jogo_terminado:
            print("\nVocê venceu a batalha!")
        else:
            print("\nVocê foi derrotado.")
