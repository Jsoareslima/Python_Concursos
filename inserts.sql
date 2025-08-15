-- Questões de Matemática
INSERT INTO Questoes (ID_Questao, ID_Disciplina, ID_Assunto, Texto_Questao, Nivel_Dificuldade) VALUES
(1, 1, 1, 'Quanto é 134 - 47 - 23?', 'Fácil'),
(2, 1, 1, 'O resultado da operação 3 x 8 x 2 é:', 'Fácil'),
(3, 1, 1, 'Qual é o valor de 91 - 17 - 34?', 'Médio'),
(4, 1, 1, 'Se João tem 480 reais e gasta 74 e depois 144, quanto sobra?', 'Médio'),
(5, 1, 3, '4 + 13 x 2 - 4 é igual a?', 'Médio'),
(6, 1, 1, 'Se 9 pessoas dividem 270 reais igualmente, cada uma recebe:', 'Fácil'),
(7, 1, 1, 'O triplo de 11 somado a 14 resulta em:', 'Fácil'),
(8, 1, 1, 'Calcule: 410 - 103 - 98', 'Difícil'),
(9, 1, 3, 'Qual o menor número entre: 44 + 39, 84 - 17, 32 x 2?', 'Médio'),
(10, 1, 1, 'Se 6 pessoas consomem 48 litros, cada uma consome em média:', 'Médio');

-- Gabarito de Matemática
INSERT INTO Gabaritos (ID_Questao, Resposta_Correta) VALUES
(1, '44'), (2, '48'), (3, '40'), (4, '240'), (5, '29'),
(6, '30'), (7, '47'), (8, '211'), (9, '62'), (10, '8');

-- Questões de Português (substituição)
INSERT INTO Questoes (ID_Questao, ID_Disciplina, ID_Assunto, Texto_Questao, Nivel_Dificuldade) VALUES
(11, 2, 4, 'A classe gramatical da palavra "rapidamente" é:', 'Fácil'),
(12, 2, 4, 'Em "Não me diga isso", a colocação pronominal é:', 'Fácil'),
(13, 2, 4, 'Em "Chegaram os convidados", identifique o sujeito:', 'Médio'),
(14, 2, 4, 'Assinale a regência correta do verbo "assistir" no sentido de ver:', 'Médio'),
(15, 2, 4, 'No período "Ana, feche a janela, por favor", o termo "Ana" é:', 'Médio'),
(16, 2, 4, 'Indique o uso correto da crase: "Vou ___ escola de manhã."', 'Médio'),
(17, 2, 4, 'A função de linguagem predominante em anúncios que buscam convencer o leitor é a:', 'Fácil'),
(18, 2, 4, 'Complete: "Não fui à festa ___ estava doente."', 'Fácil'),
(19, 2, 4, 'Em "Os alunos consideraram a prova difícil", o predicativo é:', 'Médio'),
(20, 2, 4, 'Concordância: "A maioria dos alunos ___ cedo." A forma preferencial é:', 'Difícil');

-- Gabaritos de Português (substituição)
INSERT INTO Gabaritos (ID_Questao, Resposta_Correta) VALUES
(11, 'Advérbio'),
(12, 'Próclise'),
(13, 'Os convidados (sujeito simples)'),
(14, 'Assistir a (ex.: assisti ao filme)'),
(15, 'Vocativo'),
(16, 'à'),
(17, 'Conativa (apelativa)'),
(18, 'porque'),
(19, 'difícil (predicativo do objeto)'),
(20, 'chegou');

-- Questões de Saúde
INSERT INTO Questoes (ID_Questao, ID_Disciplina, ID_Assunto, Texto_Questao, Nivel_Dificuldade) VALUES
(21, 3, 8, 'A sífilis é causada por qual agente?', 'Fácil'),
(22, 3, 8, 'Qual das opções é uma forma de prevenir a leptospirose?', 'Fácil'),
(23, 3, 8, 'A transmissão do HIV ocorre principalmente por:', 'Fácil'),
(24, 3, 9, 'O aleitamento materno exclusivo é indicado até:', 'Fácil'),
(25, 3, 8, 'A principal forma de transmissão da leptospirose é:', 'Fácil'),
(26, 3, 8, 'Uma das formas de prevenção da sífilis é:', 'Fácil'),
(27, 3, 8, 'A febre e a dor muscular podem indicar:', 'Médio'),
(28, 3, 8, 'A sífilis congênita pode ser evitada por meio de:', 'Médio'),
(29, 3, 8, 'O HIV ataca principalmente o sistema:', 'Fácil'),
(30, 3, 8, 'Transfusão de sangue contaminado pode transmitir:', 'Fácil'),
(31, 3, 7, 'A Lei 8.080/90 regulamenta qual aspecto do Sistema Único de Saúde?', 'Fácil'),
(32, 3, 7, 'Um dos princípios do SUS é a universalidade. Isso significa que:', 'Fácil'),
(33, 3, 7, 'A integralidade no SUS se refere a:', 'Fácil'),
(34, 3, 7, 'Qual destes NÃO é um princípio ou diretriz do SUS?', 'Fácil'),
(35, 3, 7, 'A descentralização no SUS significa que:', 'Médio'),
(36, 3, 7, 'A participação da comunidade é importante porque:', 'Médio'),
(37, 3, 7, 'A Lei 8.080/90 define a saúde como:', 'Fácil'),
(38, 3, 7, 'A organização do SUS é feita de forma regionalizada e hierarquizada. Isso quer dizer que:', 'Médio'),
(39, 3, 7, 'Os municípios, estados e União têm quais responsabilidades no SUS?', 'Difícil'),
(40, 3, 7, 'Um direito garantido pela Lei 8.080/90 é:', 'Fácil');

-- Gabaritos de Saúde
INSERT INTO Gabaritos (ID_Questao, Resposta_Correta) VALUES
(21, 'Bactéria Treponema pallidum'), 
(22, 'Evitar contato com água contaminada'),
(23, 'Relação sexual sem preservativo'), 
(24, '6 meses'), 
(25, 'Urina de ratos'),
(26, 'Uso de preservativo'), 
(27, 'Leptospirose'), 
(28, 'Pré-natal adequado'),
(29, 'Sistema imunológico'), 
(30, 'HIV'),
(31, 'A organização, funcionamento e ações de saúde pública e privada'),
(32, 'Todos têm direito ao acesso à saúde, sem discriminação'),
(33, 'Oferecer ações preventivas, curativas e reabilitadoras'),
(34, 'Privatização da saúde pública'),
(35, 'Gestão feita com autonomia pelos entes federativos'),
(36, 'Garante controle social e fiscalização das políticas de saúde'),
(37, 'Um direito fundamental do ser humano'),
(38, 'Serviços são organizados por níveis e por regiões'),
(39, 'Todos são responsáveis de forma integrada e complementar'),
(40, 'Acesso universal e igualitário às ações de saúde');

-- Questões sobre teorias da administração, Ford e Fayol
INSERT INTO Questoes (ID_Questao, ID_Disciplina, ID_Assunto, Texto_Questao, Nivel_Dificuldade) VALUES
(41, 4, 10, 'Qual é o foco principal da Administração Científica de Frederick Taylor?', 'Fácil'),
(42, 4, 10, 'Quem foi o criador da Teoria Clássica da Administração?', 'Fácil'),
(43, 4, 10, 'Qual princípio da Administração Clássica de Fayol defende que cada funcionário deve receber ordens de apenas um superior?', 'Médio'),
(44, 4, 10, 'Antes das teorias de administração, como eram geralmente as práticas administrativas nas empresas?', 'Médio'),
(45, 4, 10, 'Qual era a principal inovação de Henry Ford na organização da produção?', 'Fácil'),
(46, 4, 10, 'O que significa o termo "linha de montagem" criado por Henry Ford?', 'Médio'),
(47, 4, 10, 'Qual função administrativa, segundo Fayol, envolve planejar ações para alcançar objetivos?', 'Fácil'),
(48, 4, 10, 'Antes de Taylor e Fayol, as tarefas eram geralmente organizadas de que maneira?', 'Médio'),
(49, 4, 10, 'Qual teoria enfatiza a eficiência no uso de recursos e divisão de trabalho clara?', 'Fácil'),
(50, 4, 10, 'Henry Ford aplicou princípios de qual teoria para aumentar a produtividade em suas fábricas?', 'Médio');

-- Gabaritos correspondentes
INSERT INTO Gabaritos (ID_Questao, Resposta_Correta) VALUES
(41, 'Aumentar eficiência por meio de métodos científicos e padronização do trabalho'),
(42, 'Henri Fayol'),
(43, 'Princípio da Unidade de Comando'),
(44, 'Desorganizadas, sem padronização e baseadas na experiência individual dos gestores'),
(45, 'Introdução da linha de montagem'),
(46, 'Processo de produção contínuo onde o produto se move e os trabalhadores realizam tarefas específicas sequenciais'),
(47, 'Função de Planejamento'),
(48, 'De forma empírica, sem estudos sistematizados'),
(49, 'Teoria Clássica da Administração'),
(50, 'Administração Científica');

