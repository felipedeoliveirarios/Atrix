import math
'''
Os valores das perícias são armazenados em dictionaries, mas não
serão criados na inicialização. Os conhecimentos, ofícios e performances
terão seus dados adicionais incluídos na parte de anotações.
Os índices são:
Acrobacia
Arte da Fuga
Blefar
Cavalgar
Computadores
Concentração
Conhecimento 1
Conhecimento 2
Conhecimento 3
Conhecimento 4
Conhecimento 5
Desarmar Dispositivo
Diplomacia
Dirigir
Disfarce
Escalar
Furtividade
Idiomas
Intimidar
Intuir Intenção
Investigar
Lidar c/ Animais
Medicina
Nadar
Notar
Obter Informação
Ofício 1
Ofício 2
Ofício 3
Performance 1
Performance 2
Performance 3
Pilotar
Prestidigitação
Procurar
Profissão
Sobrevivência
'''

class Ficha:
    def __init_(self, nome = '', identidade = '', idade = 0, sexo = '', nivel = 1,
                tamanho = '', altura = 0.0, peso = 0.0, olhos = '', cabelo = '',
                pele = '', grupo = '', identidadeSecreta = True):
        # nome pelo qual o personagem é conhecido
        self.nome = nome
        # identidade civil do personagem
        self.identidade = identidade
        # idade do personagem
        self.idade = idade
        # sexo do personagem
        self.sexo = sexo
        # nivel do personagem
        self.nivel = nivel
        # categoria de tamanho do personagem
        self.tamanho = tamanho
        # altura em metros do personagem
        self.altura = altura
        # peso em kg do personagem
        self.peso = peso
        # cor dos olhos do personagem
        self.olhos = olhos
        # cor dos cabelos do personagem
        self.cabelo = cabelo
        # cor da pele do personagem
        self.pele = pele
        # grupo ao qual o personagem é afiliado
        self.grupo = grupo
        # se a identidade civil do personagem é publicamente associada ao nome
        # pelo qual é conhecido
        self.identidadeSecreta = identidadeSecreta
        # pontos de poder disponíveis
        self.pontosDePoder = 15 * nivel
        # dictionary das habilidades (atributos)
        self.habilidadesBase = {
            'Força' : 10,
            'Destreza' : 10,
            'Constituição' : 10,
            'Inteligência' : 10,
            'Sabedoria' : 10,
            'Carisma' : 10
                              }
        # dictionary dos bônus de habilidades (atributos) concedidos por poderes
        self.habilidadesBonus = {
            'Força' : 0,
            'Destreza' : 0,
            'Constituição' : 0,
            'Inteligência' : 0,
            'Sabedoria' : 0,
            'Carisma' : 0
                              }
        # valor máximo das habilidades
        self.habilidadesMax = {
            'Força' : (2 * nivel + 10),
            'Destreza' : (2 * nivel + 20),
            'Constituição' : (2 * nivel + 10),
            'Inteligência' : (2 * nivel + 20),
            'Sabedoria' : (2 * nivel + 20),
            'Carisma' : (2 * nivel + 20)
                              }
        # dictionary das graduações em salvamentos
        self.salvamentosGrad = {
            'Resistência' : 0,
            'Fortitude' : 0,
            'Reflexo' : 0,
            'Vontade' : 0
        }
        # dictionary dos bonus concedidos por poderes em salvamentos
        self.salvamentosBonus = {
            'Resistência' : 0,
            'Fortitude' : 0,
            'Reflexo' : 0,
            'Vontade' : 0
        }
        # valores máximos dos salvamentos
        self.salvamentosMax = {
            'Resistência' : nivel,
            'Fortitude' : (nivel + 5),
            'Reflexo' : (nivel + 5),
            'Vontade' : (nivel + 5)
        }
        # dictionary das graduações em perícias
        self.periciasGrad = {}
        # dictionary dos bônus concedidos por poderes nas perícias
        self.periciasBonus = {}
        # valor máximo das perícias
        self.periciasMax = nivel + 5
        # pontos de perícia restantes
        self.pontosDePericia = 0

        
# -------------------------------------------------------------------------------
#       MÉTODOS RELACIONADOS A HABILIDADES
# -------------------------------------------------------------------------------
    # método que retorna o total de uma habilidade
    def getHabilidadeTotal(self, habilidade):
        return (self.habilidadesBase[habilidade] + self.habilidadesBonus[habilidade])

    # método que retorna o total de uma habilidade, bem como seus valores base
    # e bônus
    def getHabilidade(self, habilidade):
        return (self.habilidadesBase[habilidade] + self.habilidadesBonus[habilidade]), self.habilidadesBase[habilidade], self.habilidadesBonus[habilidade]
    

    # método que retorna o modificador gerado por uma habilidade na rolagem
    def getModifHabilidade(self, habilidade):
        total = self.habilidadesBase[habilidade] + self.habilidadesBonus[habilidade]
        
        return math.floor((total - 10) / 2)

    #método que adiciona pontos em uma habilidade
    def addPontosHabilidade(self, habilidade, valor):
        if (self.getHabilidadeTotal(self, habilidade) + valor) < self.habilidadesMax[habilidade] and pontosDePoder >= valor:
            self.habilidadesBase[habilidade] += valor
            self.pontosDePoder -= valor
            return True
        else:
            return False
        
    # método que subtrai pontos de uma habilidade
    def subPontosHabilidade(self, habilidade, valor):
        if (self.habilidadesBase[habilidade] - valor) >= 0:
            self.habilidadesBase[habilidade] -= valor
            self.pontosDePoder += valor
            return True
        else:
            return False

    # método que remove pontos de uma habilidade (não devolve os pontos de poder)
    def rmvPontosHabilidade(self, habilidade, valor):
        if (self.habilidadesBase[habilidade] - valor) >= 0:
            self.habilidadesBase[habilidade] -= valor
            return True
        else:
            return False

        
# --------------------------------------------------------------------------------
#       MÉTODOS RELACIONADOS A SALVAMENTOS
# --------------------------------------------------------------------------------
    # método que retorna o total de um dado salvamento
    def getSalvamentoTotal(self, salvamento):
        modif = 0
        if salvamento == 'Resistência':
            modif = self.getModifHabilidade('Constituição')
        elif salvamento == 'Fortitude':
            modif = self.getModifHabilidade('Constituição')
        elif salvamento == 'Reflexo':
            modif = self.getModifHabilidade('Destreza')
        elif salvamento == 'Vontade':
            modif = self.getModifHabilidade('Sabedoria')
        else:
            return -1

        return (self.salvamentosGrad[salvamento] +
                self.salvamentosBonus[salvamento] +
                modif)
    
    # método que retorna o total de um dado salvamento, bem como suas graduações,
    # bônus por poderes e modificador por habilidade
    def getSalvamento(self, salvamento):
        modif = 0
        
        if salvamento == 'Resistência':
            modif = self.getModifHabilidade('Constituição')
        elif salvamento == 'Fortitude':
            modif = self.getModifHabilidade('Constituição')
        elif salvamento == 'Reflexo':
            modif = self.getModifHabilidade('Destreza')
        elif salvamento == 'Vontade':
            modif = self.getModifHabilidade('Sabedoria')
        else:
            return -1

        return (self.salvamentosGrad[salvamento] + self.salvamentosBonus[salvamento] + modif), self.salvamentosGrad[salvamento], self.salvamentosBonus[salvamento], modif
                
    # método que adiciona pontos em um salvamento
    def addPontosSalvamento(self, salvamento, valor):
        if salvamento != 'Resistência' and \
        (getSalvamentoTotal(salvamento) + valor) < self.salvamentosMax[salvamento] and \
        pontosDePoder >= valor:
            self.salvamentosGrad[salvamento] += valor
            self.pontosDePoder -= valor
            return True
        else:
            return False

    # método que subtrai pontos de um salvamento
    def subPontosSalvamento(self, salvamento, valor):
        if salvamento != 'Resistência' and \
        (self.salvamentosGrad[salvamento] - valor) >= 0:
            self.salvamentosGrad[salvamento] -= valor
            self.pontosDePoder += valor
            return True
        else:
            return False
        
    # método que remove pontos de salvamento (não devolve os pontos gastos)
    def rmvPontosSalvamento(self, salvamento, valor):
        if salvamento != 'Resistência' and \
        (self.salvamentosGrad[salvamento] - valor) >= 0:
            self.salvamentosGrad[salvamento] -= valor
            return True
        else:
            return False


# --------------------------------------------------------------------------------
#       MÉTODOS RELACIONADOS A PERÍCIAS
# --------------------------------------------------------------------------------
    
    # método que retorna o valor total de uma perícia
    def getPericiaTotal(self, pericia):
        modif = 0
        grad = 0
        bonus = 0
        
        if pericia == 'Acrobacia' \
        or pericia == 'Arte da Fuga' \
        or pericia == 'Cavalgar' \
        or pericia == 'Dirigir' \
        or pericia == 'Furtividade' \
        or pericia == 'Pilotar' \
        or pericia == 'Prestidigitação':
            modif = self.getModifHabilidade(self, 'Destreza')
            
        elif pericia == 'Blefar' \
        or pericia == 'Diplomacia' \
        or pericia == 'Disfarce' \
        or pericia == 'Intimidar' \
        or pericia == 'Lidar c/ Animais' \
        or pericia == 'Obter Informação' \
        or pericia == 'Performance 1' \
        or pericia == 'Performance 2' \
        or pericia == 'Performance 3':
            modif = self.getModifHabilidade(self, 'Destreza')
            
        elif pericia == 'Computadores' \
        or pericia == 'Conhecimento 1' \
        or pericia == 'Conhecimento 2' \
        or pericia == 'Conhecimento 3' \
        or pericia == 'Conhecimento 4' \
        or pericia == 'Conhecimento 5' \
        or pericia == 'Desarmar Dispositivo' \
        or pericia == 'Ofício 1' \
        or pericia == 'Ofício 2' \
        or pericia == 'Ofício 3' \
        or pericia == 'Procurar' \
        or pericia == 'Profissão':
            modif = self.getModifHabilidade(self, 'Inteligência')
            
        elif pericia == 'Concentração' \
        or pericia == 'Intuir Intenção' \
        or pericia == 'Investigar' \
        or pericia == 'Medicina' \
        or pericia == 'Notar' \
        or pericia == 'Sobrevivência':
            modif = self.getModifHabilidade(self, 'Sabedoria')
            
        elif pericia == 'Escalar' \
        or pericia == 'Nadar':
            modif = self.getModifHabilidade(self, 'Força')
            # a perícia "Idiomas" não recebe bônus de atributos
        else:
            return -1
        if pericia in Self.periciasGrad:
            grad = self.periciasGrad[pericia]
        if pericia in Self.periciasBonus:
            bonus = self.periciasBonus[pericia]
        return (grad + bonus + modif)

    # método que retorna o valor total de uma perícia, bem como suas graduações,
    # bônus por poderes e modificador por habilidade
    def getPericia(self, pericia):
        modif = 0
        grad = 0
        bonus = 0
        
        if pericia == 'Acrobacia' \
        or pericia == 'Arte da Fuga' \
        or pericia == 'Cavalgar' \
        or pericia == 'Dirigir' \
        or pericia == 'Furtividade' \
        or pericia == 'Pilotar' \
        or pericia == 'Prestidigitação':
            modif = self.getModifHabilidade(self, 'Destreza')
            
        elif pericia == 'Blefar' \
        or pericia == 'Diplomacia' \
        or pericia == 'Disfarce' \
        or pericia == 'Intimidar' \
        or pericia == 'Lidar c/ Animais' \
        or pericia == 'Obter Informação' \
        or pericia == 'Performance 1' \
        or pericia == 'Performance 2' \
        or pericia == 'Performance 3':
            modif = self.getModifHabilidade(self, 'Destreza')
            
        elif pericia == 'Computadores' \
        or pericia == 'Conhecimento 1' \
        or pericia == 'Conhecimento 2' \
        or pericia == 'Conhecimento 3' \
        or pericia == 'Conhecimento 4' \
        or pericia == 'Conhecimento 5' \
        or pericia == 'Desarmar Dispositivo' \
        or pericia == 'Ofício 1' \
        or pericia == 'Ofício 2' \
        or pericia == 'Ofício 3' \
        or pericia == 'Procurar' \
        or pericia == 'Profissão':
            modif = self.getModifHabilidade(self, 'Inteligência')
            
        elif pericia == 'Concentração' \
        or pericia == 'Intuir Intenção' \
        or pericia == 'Investigar' \
        or pericia == 'Medicina' \
        or pericia == 'Notar' \
        or pericia == 'Sobrevivência':
            modif = self.getModifHabilidade(self, 'Sabedoria')
            
        elif pericia == 'Escalar' \
        or pericia == 'Nadar':
            modif = self.getModifHabilidade(self, 'Força')
            # a perícia "Idiomas" não recebe bônus de atributos
        else:
            return -1
        if pericia in Self.periciasGrad:
            grad = self.periciasGrad[pericia]
        if pericia in Self.periciasBonus:
            bonus = self.periciasBonus[pericia]
        return (grad + bonus + modif), grad, bonus, modif
                
    # método que converte pontos de poder em pontos de pericia
    def convertePontos(self, pontosDePericia):
        if self.pontosDePoder >= math.ceil(pontosDePericia/4):
            self.pontosDePericia = (math.ceil(pontosDePericia/4) * 4)
            self.pontosDePoder -= math.ceil(pontosDePericia/4)
            return True
        else:
            return False

    # método que adiciona pontos de perícia
    def addPontosPericia(self, pericia, valor):
        if (self.getPericiaTotal(self, pericia) + valor) <= self.periciasMax:
            if self.pontosDePericia < valor:
                if not self.convertePontos(self, valor):
                    return False
            if not pericia in self.periciaGrad:
                self.periciaGrad[pericia] = 0
            self.periciaGrad[pericia] += valor
            pontosDePericia -= valor
            return True
        else:
            return False
    
    # método que subtrai pontos de perícia
    def subPontosPericia(self, pericia, valor):
        if (self.getPericiaTotal(self, pericia) - valor) >= 0:
            if not pericia in self.periciaGrad:
                return False
            if (self.getPericiaTotal(self, pericia) - valor) == 0:
                del self.periciaGrad[pericia]
            else:
                self.periciaGrad[pericia] -= valor    
            pontosDePericia += valor
            return True
        else:
            return False
    
    # método que remove pontos de perícia (não devolve os pontos gastos)
    def rmvPontosPericia(self, pericia, valor):
        if (self.getPericiaTotal(self, pericia) - valor) >= 0:
            if not pericia in self.periciaGrad:
                return False
            if (self.getPericiaTotal(self, pericia) - valor) == 0:
                del self.periciaGrad[pericia]
            else:
                self.periciaGrad[pericia] -= valor
            return True
        else:
            return False
