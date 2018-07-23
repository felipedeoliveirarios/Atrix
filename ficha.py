# Os valores dos atributos são armazenados em arrays.
# Os índices são:
# 0 = Força
# 1 = Destreza
# 2 = Constituição
# 3 = Inteligência
# 4 = Sabedoria
# 5 = Carisma

# Os valores das perícias também são armazenados em arrays.
# Os índices são:


class Ficha:
    def __init_(self, nome, idade, sexo, nivel):
        self.nome = nome
        self.idade = idade
        self.sexo = sexo
        self.nivel = nivel
        self.atributos = {10, 10, 10, 10, 10, 10}
        self.atr_modif = {0, 0, 0, 0, 0, 0}
        self.pontos_de_poder = 10 * nivel
