create database pythonC;
use pythonC;

CREATE TABLE Disciplinas (
    ID_Disciplina INT PRIMARY KEY AUTO_INCREMENT,
    Nome_Disciplina VARCHAR(255) NOT NULL
);

CREATE TABLE Assuntos (
    ID_Assunto INT PRIMARY KEY AUTO_INCREMENT,
    Assunto VARCHAR(30) NOT NULL,
    ID_Disciplina INT NOT NULL,
    CONSTRAINT fk_assuntos_disciplinas
        FOREIGN KEY (ID_Disciplina) REFERENCES Disciplinas(ID_Disciplina)
        ON DELETE CASCADE
) ENGINE=InnoDB;


CREATE TABLE Questoes (
    ID_Questao INT PRIMARY KEY AUTO_INCREMENT,
    ID_Disciplina INT NOT NULL, -- non identifying relationship/ permite haver uma disciplina sem questões, porque não está como PK aqui.
    ID_Assunto INT NOT NULL,
    Texto_Questao TEXT NOT NULL,
    Nivel_Dificuldade VARCHAR(50) not null,
    constraint fk_ID_Disciplina_tab_disciplinas
    FOREIGN KEY (ID_Disciplina) REFERENCES Disciplinas(ID_Disciplina),
    constraint fk_ID_Assunto_tab_Assuntos
    FOREIGN KEY (ID_Assunto) REFERENCES Assuntos(ID_Assunto)
) ENGINE=InnoDB;

CREATE TABLE Gabaritos (
    ID_Questao INT PRIMARY KEY, -- identifying relationship/ não permite haver uma questão sem gabaritos, porque está como PK aqui.
    Resposta_Correta TEXT NOT NULL,
    FOREIGN KEY (ID_Questao) REFERENCES Questoes(ID_Questao)
    ON DELETE CASCADE
);

insert into disciplinas (Nome_disciplina) values
('Matemática'),
('Português'),
('Saúde'),
('Faculdade');

INSERT INTO Assuntos (Assunto, ID_Disciplina) VALUES
('Aritmética', 1),
('Geometria', 1),
('Álgebra', 1);

-- Assuntos de Português (ID_Disciplina = 2)
INSERT INTO Assuntos (Assunto, ID_Disciplina) VALUES
('Gramática', 2),
('Interpretação', 2),
('Ortografia', 2);

-- Assuntos de Saúde (ID_Disciplina = 3)
INSERT INTO Assuntos (Assunto, ID_Disciplina) VALUES
('Sistema Único de Saúde', 3),
('Doenças e Prevenção', 3),
('Promoção à Saúde', 3);

-- Assuntos de Faculdade (ID_Disciplina = 4)
INSERT INTO Assuntos (Assunto, ID_Disciplina) VALUES
('Teorias da administração', 4);

-- inserts aqui em baixo

-- busca só uma das questões de saúde aleatoriamente.
/*
SELECT q.Texto_Questao
FROM questoes AS q
INNER JOIN gabaritos AS g ON q.ID_Questao = g.ID_Questao
INNER JOIN Disciplinas AS d ON d.ID_Disciplina = q.ID_Disciplina
WHERE d.Nome_Disciplina = 'Saúde'
ORDER BY RAND()
LIMIT 1;
*/

-- Busca busca disciplina, assunto, questões e gabarito, ordena em ordem crescente.
/*
SELECT
d.Nome_Disciplina,
a.Assunto,
q.Texto_Questao,
g.Resposta_Correta
FROM questoes AS q
INNER JOIN gabaritos AS g ON q.ID_Questao = g.ID_Questao
INNER JOIN Disciplinas AS d ON d.ID_Disciplina = q.ID_Disciplina
INNER JOIN Assuntos as a ON q.ID_Assunto = a.ID_Assunto
ORDER BY a.Assunto, d.Nome_Disciplina asc;
*/

