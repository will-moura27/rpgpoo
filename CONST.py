

CLASSES = {
    "mago": {
        "nivel": 1,
        "ataque": 130,
        "defesa": 70,
        "vida": 400
    },
    "guerreiro": {
        "nivel": 1,
        "ataque": 100,
        "defesa": 80,
        "vida": 420
    },
    "tanque": {
        "nivel": 1,
        "ataque": 70,
        "defesa": 100,
        "vida": 430
    },
    "mercenario": {
        "nivel": 1,
        "ataque": 100,
        "defesa": 100,
        "vida": 400
    }
}

ATAQUES = {
    "bola de fogo" : {
        "dano" : 20,
        "intervalo":2,
        "stamina" : 15


    },
    "raio do trovão": {
        "dano" : 35,
        "intervalo": 4,
        "stamina"  : 25

    },
    "cura divina": {
        "dano" : 30,
        "intervalo": 3,
        "cura" :30,
        "stamina" : 20


    },
    "bloqueio astral": {
        "dano" : 35,
        "intervalo": 3,
        "bloqueio":35,
        "stamina" : 30

    },
    "espada flamejante": {
        "dano" : 20,
        "intervalo": 2,
        "stamina" :15

    },
    "corte celestial": {
        "dano" : 35,
        "intervalo": 4,
        "stamina" :20

    },
    "investida psicotica": {
        "dano" : 35,
        "intervalo": 4,
        "stamina" :25

    },
    "furia do berserker": {
        "dano" : 35,
        "intervalo": 4,
        "stamina" :30

    },
    "escudo aegis": {
        "dano" : 35,
        "intervalo": 4,
        "bloqueio" : 35,
        "stamina" :30

    },
    "benção dos céus": {
        "dano" : 35,
        "intervalo": 4,
        "cura": 35,
        "stamina" :25

    },
    "lamaçal": {
        "dano" : 35,
        "intervalo": 4,
        "stun": 1, # paralisa por um turno, tem chance de erro
        "stamina" :30

    },
    "luz de espadas": {
        "dano" : 35,
        "intervalo": 4,
        "stamina" :20

    },
    "emboscada da meia-noite": {
        "dano" : 35,
        "intervalo": 4,
        "stamina" :25

    },
    "tiro certo": {
        "dano" : 35,
        "intervalo": 4,
        "stamina" : 20

    },
    "rebite": {
        "dano" : 35,
        "intervalo": 4,
        "cura" : 35,
        "stamina" :25


    }

}

ATAQUES_POR_CLASSE = {
    "mago": ["bola de fogo", "raio do trovão", "cura divina", "bloqueio astral"],
    "guerreiro": ["espada flamejante", "corte celestial", "furia do berserker", "escudo aegis"],
    "tanque": ["benção dos céus", "lamaçal", "luz de espadas", "escudo aegis"],
    "mercenario": ["emboscada da meia-noite", "tiro certo", "rebite", "investida psicotica"]
}

ATRIBUTO_INIMIGO = {
    "inimigo inicial" : {
        "nivel": 3,
        "ataque": 150,
        "defesa": 100,
        "vida": 150,
        "stamina" :100
    },
    "Mago Negro": {
        "nivel": 3,
        "ataque": 150,
        "defesa": 100,
        "vida": 150,
        "stamina": 100

    }
}

ATAQUES_INIMIGO = {

    "Mago Negro": ["raio do vazio","investida astral","colisão universal","ressurgir"],
    "inimigo inicial" : ["raio do vazio","investida astral","colisão universal","ressurgir"]

}

DANOS_ATK_INI = {
    "raio do vazio": {
        "dano" : 20,
        "intervalo":2,
        "stamina": 30

    },

    "investida astral" : {
        "dano" : 20,
        "intervalo":2,
        "stamina": 30

    },

    "colisão universal" : {
        "dano" : 20,
        "intervalo":2,
        "stamina": 30

    },

    "ressurgir" : {
        "dano" : 0,
        "intervalo":6,
        "cura" : 60,
        "stamina": 30

    }
}