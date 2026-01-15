
-- ============================================
-- ROLES / PAPÉIS
-- ============================================
CREATE TABLE role (
    id_papel    SERIAL PRIMARY KEY,
    nome        VARCHAR(50) NOT NULL UNIQUE,  
    descricao   TEXT
);

-- ============================================
-- USUÁRIOS
-- ============================================
CREATE TABLE usuario (
    id_usuario   SERIAL PRIMARY KEY,
    nome         VARCHAR(100) NOT NULL,
    email        VARCHAR(255) NOT NULL UNIQUE,
    cpf_rg       VARCHAR(20)  NOT NULL UNIQUE,
    senha_hash   VARCHAR(255) NOT NULL,
    id_papel     INTEGER NOT NULL,
    CONSTRAINT fk_usuario_role
        FOREIGN KEY (id_papel)
        REFERENCES role (id_papel)
        ON DELETE CASCADE
);

-- ============================================
-- PASSWORD RESET TOKENS
-- ============================================
CREATE TABLE password_reset_token (
    id_token    SERIAL PRIMARY KEY,
    id_usuario  INTEGER NOT NULL,
    token_hash  VARCHAR(64) NOT NULL,
    expires_at  TIMESTAMP NOT NULL,
    used_at     TIMESTAMP,
    CONSTRAINT fk_token_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE
);

-- ============================================
-- ESPAÇOS CULTURAIS
-- ============================================
CREATE TABLE espaco_cultural (
    id_espaco_cult SERIAL PRIMARY KEY,
    nome           VARCHAR(100) NOT NULL,
    rua            VARCHAR(100) NOT NULL,
    numero         VARCHAR(10)  NOT NULL,
    bairro         VARCHAR(60)  NOT NULL
);

-- ============================================
-- ARTISTAS
-- ============================================
CREATE TABLE artista (
    id_artista  SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(255),
    telefone    VARCHAR(20),
    descricao   TEXT
);

-- ============================================
-- EVENTOS
-- ============================================
CREATE TABLE evento (
    id_evento       SERIAL PRIMARY KEY,
    titulo          VARCHAR(150) NOT NULL,
    descricao       TEXT,
    categoria       VARCHAR(60),
    capacidade      INTEGER CHECK (capacidade >= 0),
    data_inicio     TIMESTAMP NOT NULL,
    data_fim        TIMESTAMP NOT NULL,
    preco           NUMERIC(10,2) DEFAULT 0 CHECK (preco >= 0),
    status          VARCHAR(20) NOT NULL,   
    id_espaco_cult  INTEGER NOT NULL,
    CONSTRAINT fk_evento_espaco
        FOREIGN KEY (id_espaco_cult)
        REFERENCES espaco_cultural (id_espaco_cult)
        ON DELETE CASCADE
);

-- ============================================
-- RELACIONAMENTOS N:N
-- ============================================

-- Usuário participa de evento
CREATE TABLE usuario_participa_evento (
    id_participacao SERIAL PRIMARY KEY,
    id_usuario      INTEGER NOT NULL,
    id_evento       INTEGER NOT NULL,
    data_inscricao  TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_usuario_participa
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
    CONSTRAINT fk_evento_participa
        FOREIGN KEY (id_evento)
        REFERENCES evento (id_evento)
        ON DELETE CASCADE
);

-- Artista apresenta de evento
CREATE TABLE artista_apresenta_evento (
    id_evento   INTEGER NOT NULL,
    id_artista  INTEGER NOT NULL,
    data        DATE,
    hora        TIME,
    PRIMARY KEY (id_evento, id_artista),
    CONSTRAINT fk_evento_artista
        FOREIGN KEY (id_evento)
        REFERENCES evento (id_evento)
        ON DELETE CASCADE,
    CONSTRAINT fk_artista_evento
        FOREIGN KEY (id_artista)
        REFERENCES artista (id_artista)
        ON DELETE CASCADE
);

-- ============================================
-- DENÚNCIA DE EVENTO
-- ============================================
CREATE TABLE usuario_denuncia_evento (
    id_denuncia SERIAL PRIMARY KEY,
    motivo      VARCHAR(150) NOT NULL,
    data        TIMESTAMP NOT NULL DEFAULT NOW(),
    descricao   TEXT,
    status      VARCHAR(20) NOT NULL DEFAULT 'aberta',
    id_usuario  INTEGER NOT NULL,
    id_evento   INTEGER NOT NULL,
    CONSTRAINT fk_denuncia_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
    CONSTRAINT fk_denuncia_evento
        FOREIGN KEY (id_evento)
        REFERENCES evento (id_evento)
        ON DELETE CASCADE
);

-- ============================================
-- AVALIAÇÃO DE EVENTO
-- ============================================
CREATE TABLE usuario_avalia_evento (
    id_avaliacao SERIAL PRIMARY KEY,
    data         TIMESTAMP NOT NULL DEFAULT NOW(),
    nota         INTEGER CHECK (nota BETWEEN 0 AND 5),
    id_usuario   INTEGER NOT NULL,
    id_evento    INTEGER NOT NULL,
    CONSTRAINT fk_avalia_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
    CONSTRAINT fk_avalia_evento
        FOREIGN KEY (id_evento)
        REFERENCES evento (id_evento)
        ON DELETE CASCADE
);
