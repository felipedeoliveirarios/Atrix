CREATE TABLE IF NOT EXISTS GRUPOS (
        Id_Grupo INTEGER NOT NULL PRIMARY KEY,
        Id_Mestre INTEGER,
	Edição_Aberta BOOLEAN
        
);
CREATE TABLE IF NOT EXISTS FICHAS (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER NOT NULL,
        Nome CHAR(32),
        Identidade_Civil CHAR(64),
        Identidade_Secreta BOOLEAN,
        Sexo CHAR,
        Idade INT,
        Altura FLOAT,
        Peso FLOAT,
        Tamanho INT,
        Olhos CHAR(16),
	Pele CHAR(16),
	Cabelo CHAR(16),
        Base_de_Operações CHAR(32),
        Nível_de_Poder INT,
        Pontos_de_Poder INT,
        Ataques INT,
        Defesa INT,
	FOREIGN KEY(Id_Grupo) REFERENCES GRUPOS(Id_Grupo),
	PRIMARY KEY(Id_grupo, Id_jogador)
);
CREATE TABLE IF NOT EXISTS HABILIDADES (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER NOT NULL,
        Força_Base INT,
        Destreza_Base INT,
        Constituição_Base INT,
        Inteligência_Base INT,
        Sabedoria_Base INT,
        Carisma_Base INT,
        Força_Bonus INT,
        Destreza_Bonus INT ,
        Constituição_Bonus INT,
        Inteligência_Bonus INT,
        Sabedoria_Bonus INT,
        Carisma_Bonus INT,
	FOREIGN KEY(Id_grupo, Id_jogador) REFERENCES FICHAS(Id_grupo, Id_jogador),
	PRIMARY KEY(Id_grupo, Id_jogador)
);
CREATE TABLE IF NOT EXISTS SALVAMENTOS (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER NOT NULL,
        Fortitude_Grad INT,
        Reflexo_Grad INT,
        Vontade_Grad INT,
        Resistencia_Bonus INT,
        Fortitude_Bonus INT,
        Reflexo_Bonus INT,
        Vontade_Bonus INT,
	FOREIGN KEY(Id_grupo, Id_jogador) REFERENCES FICHAS(Id_grupo, Id_jogador),
	PRIMARY KEY(Id_grupo, Id_jogador)
);
CREATE TABLE IF NOT EXISTS FEITOS (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER NOT NULL,
        Nome CHAR(32),
        Bonus CHAR(32),
	FOREIGN KEY(Id_grupo, Id_jogador) REFERENCES FICHAS(Id_grupo, Id_jogador),
	PRIMARY KEY(Id_grupo, Id_jogador, Nome)
);
CREATE TABLE IF NOT EXISTS PERICIAS (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER,
        Nome CHAR(32),
        Bonus_Habilidade CHAR(3),
        Graduações INT,
        Bonus INT,
	FOREIGN KEY(Id_grupo, Id_jogador) REFERENCES FICHAS(Id_grupo, Id_jogador),
	PRIMARY KEY(Id_grupo, Id_jogador, Nome)
);
CREATE TABLE IF NOT EXISTS DESVANTAGENS (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER,
        Descrição CHAR(64),
        Frequência INT,
        Intensidade INT,
	FOREIGN KEY(Id_grupo, Id_jogador) REFERENCES FICHAS(Id_grupo, Id_jogador),
	PRIMARY KEY(Id_grupo, Id_jogador, Descrição)
);
CREATE TABLE IF NOT EXISTS PODERES_E_DISPOSITIVOS (
        Id_Grupo INTEGER,
        Id_Jogador INTEGER NOT NULL,
        Nome CHAR(32),
        Descrição CHAR(100),
        Tipo CHAR(16),
        Ativa BOOLEAN,
        Área_Efeito CHAR(32),
        Tempo_Ativação CHAR(16),
        Tempo_Recarga INT,
        Duração INT,
        Custo_Base INT,
        Graduações INT,
        Feitos INT,
        Extras INT,
        Falhas INT,
	FOREIGN KEY(Id_grupo, Id_jogador) REFERENCES FICHAS(Id_grupo, Id_jogador),
	PRIMARY KEY(Id_grupo, Id_jogador, Nome)
);
