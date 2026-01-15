-- ============================================
-- PAPÉIS
-- ============================================

INSERT INTO role (nome, descricao)
VALUES
('ADMIN', 'Usuário com acesso administrativo'),
('COMUM', 'Usuário padrão do sistema');

-- ============================================
-- USUÁRIOS
-- ============================================

INSERT INTO usuario (nome, email, cpf_rg, senha_hash, id_papel)
VALUES
('Ana Admin',         'ana.admin@exemplo.com',  '333.333.333-33', '$2b$12$CxSGTcLNjS1khDyWIQT5Rur1y1ddJRNluo0qCdLSsWOD5u2sfEf0S', 1),
('Carlos Usuário',    'carlos@exemplo.com',     '444.444.444-44', '$2b$12$Fn8ImpCq.sR8iWvr6gp6VO81USpc7u.YtTxMIVHOkm42uIWSMFPn2', 2),
('Maria Usuária',     'maria@exemplo.com',      '555.555.555-55', '$2b$12$H/DOXeWAPUuhfN.57eaPseSnGL.ZfEjwoLF2gB8s4gM6oA/JDcJKu', 2),
('Sanderley Usuario', 'sanderley@gmail.com',    '666.666.666-66', '$2b$12$k3qYDAod8uCsxIwm89taMO4hHBxaArGNt.r1EIYKSxsxDXB7OOjMi',    2),
('Cicero Usuario',    'cicero@gmail.com',       '777.777.777-77', '$2b$12$hs9Z6MoAOwFk5ocdx4hZ3.Jxk4xRoGNg9P6UTm1ZYJYBomobdorFm', 2),
('Ianara Usuaria',    'ianara@gmail.com',       '888.888.888-88', '$2b$12$7DVED4ZONRjKZLMJ0ftZE.Mc5AzjSof2/a6BoU3XVK1LjwvpGMvIe', 2),
('Marcos Usuario',    'marcos@gmail.com',       '999.999.999-99', '$2b$12$Qeq8z3icYRSjgrl/C5jNIONLQm0PUGgyNok2WOJx2PzGR5EWzFMt.', 2),
('Larissa Usuario',   'lariss@gmil.com',        '000.000.000-00', '$2b$12$uIlQD3zPCpWgCAqmg91rHuEbChFY3i/F13F.otYngfz7JY8p36tEC',2),
('Samia Usuario',     'samia@gmail.com',        '111.111.111-11', '$2b$12$OZ8t9bhNz9.131yX1LrQt.b5O9iF6Wo4Ojkz4cTDDK6sOf90uQZjG',  2),
('Joaquim Usuario',   'joaquim@gail.com',       '123.456.789-00', '$2b$12$VIg3nbmZ/G3zqXan1/bCeuk.ZrQpmwUEj8DowNGnNh/5SUOA8LJ76',  2);


-- ============================================
-- ESPAÇOS CULTURAIS
-- ============================================


INSERT INTO espaco_cultural (nome, rua, numero, bairro)
VALUES
('Case do cego Aderaldo',                         'Rua Pascoal Crispino',           '167',  'Centro'),
('Memorial Rachel de Queiroz',                    'Rua José Jucá',                  '343',  'Centro'),
('Museu Histórico Jacinto de Sousa',              'Rua Altran Moreno',              '202',  'Centro'),
('Teatrinho de Bolso Velho Didi',                 'Rua Oscar Barbosa',              '00',   'Centro'),
('UECE',                                          'Rua José de Queiroz Pessoa',     '2554', 'Planalto Universitário'),
('UFCQXD',                                        'Av. José de Freitas Queiroz',    '5003', 'Cedro'),
('Centro Universitário Católica de Quixadá',      'Av. Plácido Castelo',            '200',  'Centro'),
('IFCE',                                          'Av. José de Freitas Queiroz',    '5003', 'Cedro'),
('CDL - Câmara de Dirigentes Lojistas de Quixadá','Rua José Jucá',                  '551',  'Centro'),
('Praça do Leão - José de Barros',                'Av. Plácido Castelo',            'S/N',  'Centro');



-- ============================================
-- ARTISTAS (Sem cpf_rg)
-- ============================================

INSERT INTO artista (nome, email, telefone, descricao)
VALUES
('Grupo Teatro Sertão em Cena',
 'teatro.sertao@exemplo.com',
 '88981000001',
 'Grupo de teatro popular com foco na cultura sertaneja.'
),
('Coro Vozes do Sertão',
 'coro.vozes@exemplo.com',
 '88981000002',
 'Coro formado por moradores de Quixadá com repertório regional.'
),
('Banda Pedra da Galinha',
 'banda.pedra@exemplo.com',
 '88981000003',
 'Banda de forró e baião inspirada na Pedra da Galinha Choca.'
),
('Cia de Dança Quixadá em Movimento',
 'danca.quixada@exemplo.com',
 '88981000004',
 'Companhia de dança contemporânea com apresentações em praças públicas.'
),
('Quarteto Acadêmico',
 'quarteto.academico@exemplo.com',
 '88981000005',
 'Grupo instrumental formado por estudantes universitários.'
),
('Coletivo TechArt',
 'coletivo.techart@exemplo.com',
 '88981000006',
 'Coletivo que mistura arte digital e música eletrônica.'
),
('Grupo Universitário de Música',
 'grupo.musica.uni@exemplo.com',
 '88981000007',
 'Grupo de música acústica formado por alunos de várias instituições.'
),
('Trio IFCE Instrumental',
 'trio.ifce@exemplo.com',
 '88981000008',
 'Trio instrumental ligado a projetos de extensão do IFCE.'
),
('Coral do Comércio de Quixadá',
 'coral.comercio@exemplo.com',
 '88981000009',
 'Coral formado por lojistas e funcionários do comércio local.'
),
('Banda Praça do Leão',
 'banda.praca.leao@exemplo.com',
 '88981000010',
 'Banda que se apresenta tradicionalmente na Praça do Leão.'
);

-- ============================================
-- EVENTOS
-- ============================================

INSERT INTO evento (
    titulo, descricao, categoria, capacidade,
    data_inicio, data_fim, preco, status, id_espaco_cult
)
VALUES
('Mostra Cultural Casa do Cego Aderaldo',
 'Apresentações artísticas e contação de histórias sobre Cego Aderaldo.',
 'Cultural',
 150,
 '2025-04-10 19:00:00',
 '2025-04-10 22:00:00',
 0.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'Case do cego Aderaldo')
),
('Semana Rachel de Queiroz',
 'Palestras, rodas de leitura e exposições sobre a obra de Rachel de Queiroz.',
 'Literário',
 200,
 '2025-05-15 18:00:00',
 '2025-05-20 21:00:00',
 0.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'Memorial Rachel de Queiroz')
),
('Histórias de Quixadá',
 'Exposição sobre a história do município e da região do Sertão Central.',
 'História',
 120,
 '2025-06-05 09:00:00',
 '2025-06-30 17:00:00',
 10.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'Museu Histórico Jacinto de Sousa')
),
('Festival de Teatro Velho Didi',
 'Mostra de grupos de teatro com espetáculos para toda a comunidade.',
 'Teatro',
 180,
 '2025-07-12 19:30:00',
 '2025-07-14 22:30:00',
 20.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'Teatrinho de Bolso Velho Didi')
),
('Seminário Acadêmico UECE Quixadá',
 'Apresentação de trabalhos, palestras e mesas redondas da UECE.',
 'Acadêmico',
 300,
 '2025-08-10 08:00:00',
 '2025-08-12 18:00:00',
 0.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'UECE')
),
('Feira de Tecnologia UFCQXD',
 'Feira de projetos de tecnologia e inovação dos alunos da UFC Quixadá.',
 'Tecnologia',
 500,
 '2025-09-01 09:00:00',
 '2025-09-03 18:00:00',
 15.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'UFCQXD')
),
('Simpósio de Educação Católica',
 'Encontros e palestras sobre educação e espiritualidade.',
 'Educação',
 250,
 '2025-10-05 14:00:00',
 '2025-10-07 20:00:00',
 25.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'Centro Universitário Católica de Quixadá')
),
('Mostra de Projetos IFCE Quixadá',
 'Exposição de projetos de extensão e pesquisa do IFCE.',
 'Acadêmico',
 300,
 '2025-11-10 09:00:00',
 '2025-11-11 17:00:00',
 0.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'IFCE')
),
('Encontro do Comércio de Quixadá',
 'Palestras, painéis e networking para lojistas e empreendedores.',
 'Negócios',
 200,
 '2025-11-20 18:00:00',
 '2025-11-20 22:00:00',
 30.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'CDL - Câmara de Dirigentes Lojistas de Quixadá')
),
('Festival Praça do Leão',
 'Festival com apresentações musicais, dança e gastronomia na Praça do Leão.',
 'Festival',
 800,
 '2025-12-15 17:00:00',
 '2025-12-15 23:59:00',
 5.00,
 'ativo',
 (SELECT id_espaco_cult FROM espaco_cultural WHERE nome = 'Praça do Leão - José de Barros')
);


-- ============================================
-- usuario participa evento
-- ============================================


INSERT INTO usuario_participa_evento (id_usuario, id_evento)
VALUES
((SELECT id_usuario FROM usuario WHERE email = 'ana.admin@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Mostra Cultural Casa do Cego Aderaldo')),
((SELECT id_usuario FROM usuario WHERE email = 'carlos@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Festival Praça do Leão')),
((SELECT id_usuario FROM usuario WHERE email = 'maria@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Semana Rachel de Queiroz')),
((SELECT id_usuario FROM usuario WHERE email = 'sanderley@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Feira de Tecnologia UFCQXD')),
((SELECT id_usuario FROM usuario WHERE email = 'cicero@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Encontro do Comércio de Quixadá')),
((SELECT id_usuario FROM usuario WHERE email = 'ianara@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Festival de Teatro Velho Didi')),
((SELECT id_usuario FROM usuario WHERE email = 'marcos@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Mostra de Projetos IFCE Quixadá')),
((SELECT id_usuario FROM usuario WHERE email = 'lariss@gmil.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Histórias de Quixadá')),
((SELECT id_usuario FROM usuario WHERE email = 'samia@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Seminário Acadêmico UECE Quixadá')),
((SELECT id_usuario FROM usuario WHERE email = 'joaquim@gail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Simpósio de Educação Católica'));


--============================================
--artista apresenta evento
--============================================

INSERT INTO artista_apresenta_evento (id_evento, id_artista, data, hora)
VALUES
((SELECT id_evento  FROM evento  WHERE titulo = 'Mostra Cultural Casa do Cego Aderaldo'),
 (SELECT id_artista FROM artista WHERE nome   = 'Grupo Teatro Sertão em Cena'), '2025-04-10', '19:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Semana Rachel de Queiroz'),
 (SELECT id_artista FROM artista WHERE nome   = 'Coro Vozes do Sertão'), '2025-05-15', '18:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Histórias de Quixadá'),
 (SELECT id_artista FROM artista WHERE nome   = 'Banda Pedra da Galinha'), '2025-06-05', '09:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Festival de Teatro Velho Didi'),
 (SELECT id_artista FROM artista WHERE nome   = 'Cia de Dança Quixadá em Movimento'), '2025-07-12', '19:30:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Seminário Acadêmico UECE Quixadá'),
 (SELECT id_artista FROM artista WHERE nome   = 'Quarteto Acadêmico'), '2025-08-10', '08:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Feira de Tecnologia UFCQXD'),
 (SELECT id_artista FROM artista WHERE nome   = 'Coletivo TechArt'), '2025-09-01', '09:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Simpósio de Educação Católica'),
 (SELECT id_artista FROM artista WHERE nome   = 'Grupo Universitário de Música'), '2025-10-05', '14:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Mostra de Projetos IFCE Quixadá'),
 (SELECT id_artista FROM artista WHERE nome   = 'Trio IFCE Instrumental'), '2025-11-10', '09:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Encontro do Comércio de Quixadá'),
 (SELECT id_artista FROM artista WHERE nome   = 'Coral do Comércio de Quixadá'), '2025-11-20', '18:00:00'),
((SELECT id_evento  FROM evento  WHERE titulo = 'Festival Praça do Leão'),
 (SELECT id_artista FROM artista WHERE nome   = 'Banda Praça do Leão'), '2025-12-15', '17:00:00');


--==============================
--Denuncia
--==============================

INSERT INTO usuario_denuncia_evento (motivo, descricao, status, id_usuario, id_evento)
VALUES
('Som muito alto',
 'O som estava muito alto durante o festival.',
 'aberta',
 (SELECT id_usuario FROM usuario WHERE email = 'carlos@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Festival Praça do Leão')
),
('Atraso na programação',
 'O evento começou com mais de 1 hora de atraso.',
 'aberta',
 (SELECT id_usuario FROM usuario WHERE email = 'maria@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Semana Rachel de Queiroz')
),
('Superlotação',
 'Havia mais pessoas do que a capacidade informada.',
 'em análise',
 (SELECT id_usuario FROM usuario WHERE email = 'sanderley@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Feira de Tecnologia UFCQXD')
),
('Problemas de acessibilidade',
 'Poucas opções de acesso para pessoas com deficiência.',
 'em análise',
 (SELECT id_usuario FROM usuario WHERE email = 'cicero@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Histórias de Quixadá')
),
('Banheiros sujos',
 'Condições de higiene nos banheiros eram ruins.',
 'fechada',
 (SELECT id_usuario FROM usuario WHERE email = 'ianara@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Festival de Teatro Velho Didi')
),
('Iluminação fraca',
 'Dificuldade de enxergar o palco em alguns momentos.',
 'aberta',
 (SELECT id_usuario FROM usuario WHERE email = 'marcos@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Mostra Cultural Casa do Cego Aderaldo')
),
('Informações confusas',
 'Sinalização dentro do evento poderia ser melhor.',
 'em análise',
 (SELECT id_usuario FROM usuario WHERE email = 'lariss@gmil.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Mostra de Projetos IFCE Quixadá')
),
('Preço diferente do divulgado',
 'O valor cobrado na entrada era maior do que o divulgado.',
 'aberta',
 (SELECT id_usuario FROM usuario WHERE email = 'samia@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Simpósio de Educação Católica')
),
('Falta de segurança',
 'Poucos seguranças para o número de pessoas.',
 'aberta',
 (SELECT id_usuario FROM usuario WHERE email = 'joaquim@gail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Encontro do Comércio de Quixadá')
),
('Problemas de som',
 'Microfone falhando durante as apresentações.',
 'fechada',
 (SELECT id_usuario FROM usuario WHERE email = 'ana.admin@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Seminário Acadêmico UECE Quixadá')
);


--==============================================
--Avaliação (Sem comentário)
--==============================================

INSERT INTO usuario_avalia_evento (nota, id_usuario, id_evento)
VALUES
(5,
 (SELECT id_usuario FROM usuario WHERE email = 'ana.admin@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Mostra Cultural Casa do Cego Aderaldo')
),
(4,
 (SELECT id_usuario FROM usuario WHERE email = 'carlos@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Festival Praça do Leão')
),
(5,
 (SELECT id_usuario FROM usuario WHERE email = 'maria@exemplo.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Semana Rachel de Queiroz')
),
(5,
 (SELECT id_usuario FROM usuario WHERE email = 'sanderley@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Feira de Tecnologia UFCQXD')
),
(3,
 (SELECT id_usuario FROM usuario WHERE email = 'cicero@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Histórias de Quixadá')
),
(5,
 (SELECT id_usuario FROM usuario WHERE email = 'ianara@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Festival de Teatro Velho Didi')
),
(4,
 (SELECT id_usuario FROM usuario WHERE email = 'marcos@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Seminário Acadêmico UECE Quixadá')
),
(4,
 (SELECT id_usuario FROM usuario WHERE email = 'lariss@gmil.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Mostra de Projetos IFCE Quixadá')
),
(5,
 (SELECT id_usuario FROM usuario WHERE email = 'samia@gmail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Encontro do Comércio de Quixadá')
),
(5,
 (SELECT id_usuario FROM usuario WHERE email = 'joaquim@gail.com'),
 (SELECT id_evento  FROM evento  WHERE titulo = 'Simpósio de Educação Católica')
);
