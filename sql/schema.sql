CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS moedas (
    codigo CHAR(3) PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    simbolo VARCHAR(5) NOT NULL,
    cotacao NUMERIC(10,4) NOT NULL CHECK (cotacao > 0)
);

CREATE TABLE IF NOT EXISTS saldos (
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    moeda CHAR(3) REFERENCES moedas(codigo),
    valor NUMERIC(14,2) NOT NULL DEFAULT 0 CHECK (valor >= 0),
    PRIMARY KEY (usuario_id, moeda)
);

CREATE TABLE IF NOT EXISTS movimentacoes (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('deposito', 'saque')),
    moeda CHAR(3) REFERENCES moedas(codigo),
    valor_moeda NUMERIC(14,2) NOT NULL,
    valor_reais NUMERIC(14,2),
    cotacao NUMERIC(10,4),
    feito_em TIMESTAMP DEFAULT NOW()
);

INSERT INTO moedas VALUES
('USD', 'Dólar', 'US$', 5.00),
('EUR', 'Euro',  '€',   5.67),
('GBP', 'Libra', '£',   6.67)
ON CONFLICT DO NOTHING;