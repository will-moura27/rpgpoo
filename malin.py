from Inimigo import Inimigo
from Personagem import Personagem
from Batalha import Batalha
# Criando personagem
while True:
    dados = Personagem.criacao_perso()
    if dados:
        break
    print("Classe inválida. Tente novamente.")

nome, classe, nivel, ataque, defesa, vida, ataques = dados
jogador = Personagem(nome, classe, nivel, ataque, defesa, vida, ataques)

jogador.apresentacao()

print("\n")
# Criando inimigo
dados = Inimigo.stats_ini()
if dados is None:
    print("Erro ao criar o inimigo. Verifique a classe e os atributos.")
    exit()

nome, classe, nivel, ataque, defesa, vida, ataques = dados
inimiguin = Inimigo(nome, vida, ataque, defesa, nivel, classe, ataques)
inimiguin.apresentacao_ini()

batalha = Batalha(jogador, inimiguin)
batalha.iniciar()


