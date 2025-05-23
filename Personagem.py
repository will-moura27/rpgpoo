from CONST import CLASSES, ATAQUES, ATAQUES_POR_CLASSE

class Personagem:
    def __init__(self, nome, classe, nivel, ataque, defesa, vida, ataques):
        self.nome = nome
        self.classe = classe
        self.nivel = nivel
        self.ataque = ataque
        self.defesa = defesa
        self.vida = vida
        self.ataques = ataques  # lista de nomes de ataques
        self.stamina_jogador = 100
        self.max_stamina_jogador = 100

    def apresentacao(self):
        print(f"=== Personagem ===")
        print(f"Nome: {self.nome}")
        print(f"Classe: {self.classe}")
        print(f"Nível: {self.nivel}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"Vida: {self.vida}")
        print("\nAtaques:")
        for atk in self.ataques:
            dados = ATAQUES[atk]
            print(f"- {atk.title()} (Dano: {dados['dano']}, Intervalo: {dados['intervalo']}s)")

    @staticmethod
    def criacao_perso():
        nome = input("Digite o nome desejado: ")
        classe = input("Escolha uma das classes (mago, guerreiro, tanque, mercenario): ").lower()

        if classe not in CLASSES:
            print("Classe inválida!")
            return None

        atributos = CLASSES[classe]
        lista_ataques = ATAQUES_POR_CLASSE.get(classe, [])

        return nome, classe, atributos["nivel"], atributos["ataque"], atributos["defesa"], atributos["vida"], lista_ataques
