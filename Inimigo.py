from CONST import DANOS_ATK_INI, ATRIBUTO_INIMIGO, ATAQUES_INIMIGO


class Inimigo:
    def __init__(self, nome, vida, ataque, defesa, nivel, classe,ataques):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.nivel = nivel
        self.classe = classe
        self.ataques = ataques

    def apresentacao_ini(self):
        print(f"=== Inimigo ===")
        print(f"Nome: {self.nome}")
        print(f"Classe: {self.classe}")
        print(f"Nível: {self.nivel}")
        print(f"Ataque: {self.ataque}")
        print(f"Defesa: {self.defesa}")
        print(f"Vida: {self.vida}")
        for atk in self.ataques:
            dados = DANOS_ATK_INI[atk]
            print(f"- {atk.title()} (Dano: {dados['dano']}, Intervalo: {dados['intervalo']}s)")

    @staticmethod
    @staticmethod
    def stats_ini():
        nome = "Mago das Trevas"
        classe = "Mago Negro"  # Certifique-se que esta chave existe no ATRIBUTO_INIMIGO

        if classe not in ATRIBUTO_INIMIGO:
            print("Classe inválida!")
            return None

        atributos = ATRIBUTO_INIMIGO[classe]
        lista_ataques = ATAQUES_INIMIGO.get(classe, [])

        return nome, classe, atributos["nivel"], atributos["ataque"], atributos["defesa"], atributos[
            "vida"], lista_ataques



