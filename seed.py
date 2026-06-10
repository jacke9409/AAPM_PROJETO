"""
seed_produtos.py
Popula o banco de dados com as categorias e produtos da AAPM.
Execute com: python seed_produtos.py
"""
from app.database import SessionLocal, Base, engine
from app.models import Categoria, Produto

# Garante que as tabelas existam
Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        # ── Evita duplicatas ──────────────────────────────────────────────────
        if db.query(Categoria).first():
            print("⚠️  Banco já populado. Seed ignorado.")
            return

        # ── Categorias ────────────────────────────────────────────────────────
        categorias_nomes = [
            "Papelaria",
            "Escritório",
            "Costura e Artesanato",
            "Informática e Eletrônicos",
            "Vestuário",
            "Medição e Traçado",
            "Serviços e Taxas",
        ]

        cats = {nome: Categoria(nome=nome) for nome in categorias_nomes}
        db.add_all(cats.values())
        db.flush()  # gera IDs sem fechar transação

        # ── Produtos ──────────────────────────────────────────────────────────
        # Estrutura: (nome, preco_normal, preco_associado, categoria_key, estoque)
        produtos_raw = [
            # Serviços e Taxas
            ("Semestralidade AAPM",       None,   100.00, "Serviços e Taxas", 999),
            ("Armário / Semestralidade",  None,   130.00, "Serviços e Taxas", 999),
            ("2ª via de crachá",          20.00,   15.00, "Serviços e Taxas", 999),

            # Vestuário
            ("Avental",                   65.00,   58.00, "Vestuário", 30),
            ("Camiseta malha Branca",      40.00,   35.00, "Vestuário", 50),
            ("Camiseta malha Preta",       40.00,   35.00, "Vestuário", 50),
            ("Camiseta POLO de malha preta", 60.00, 55.00, "Vestuário", 30),
            ("Touca protetora (5 un)",      6.00,    5.00, "Vestuário", 20),

            # Costura e Artesanato
            ("Agulha de máquina Nº11 - pacote c/10un", 10.00, 8.00, "Costura e Artesanato", 25),
            ("Alfinete c/ cabeça colorida",  3.00,  2.00, "Costura e Artesanato", 40),
            ("Alfinete simples",             6.00,  5.00, "Costura e Artesanato", 40),
            ("Almofada Alfineteita Tomate",  8.00,  6.00, "Costura e Artesanato", 15),
            ("Bobina",                       2.00,  1.00, "Costura e Artesanato", 30),
            ("Fita Crepe - rolo 18mm x 10m", 3.00,  2.00, "Costura e Artesanato", 50),
            ("Fita Crepe - rolo 18mm x 50m",10.00,  8.00, "Costura e Artesanato", 30),
            ("Fita Métrica",                 5.00,  3.00, "Costura e Artesanato", 25),
            ("Giz lápis marcar tecido cores",5.00,  4.00, "Costura e Artesanato", 20),
            ("Passador de linha grande",     4.00,  3.00, "Costura e Artesanato", 20),
            ("Passador de linha pequeno",    1.50,  1.00, "Costura e Artesanato", 20),
            ("Percevejos",                   8.00,  5.00, "Costura e Artesanato", 30),
            ("Pinça Costura",                7.00,  5.00, "Costura e Artesanato", 20),
            ("Tesoura Aremate",              6.00,  4.00, "Costura e Artesanato", 20),
            ("Tesoura de Picotar Profissional", 43.00, 39.00, "Costura e Artesanato", 10),
            ("Tesoura Picotar escolar",      14.00, 12.00, "Costura e Artesanato", 15),
            ("Tesoura",                      20.00, 18.00, "Costura e Artesanato", 20),
            ("Vazador 2mm",                  16.00, 14.00, "Costura e Artesanato", 10),

            # Medição e Traçado
            ("Compasso",                     17.00, 13.00, "Medição e Traçado", 15),
            ("Curva Francesa grande 1119",   23.00, 19.00, "Medição e Traçado", 10),
            ("Curva Francesa pequena 1105",  20.00, 15.00, "Medição e Traçado", 10),
            ("Esquadro",                      5.00,  4.00, "Medição e Traçado", 20),
            ("Guia Magnético G20",            5.00,  4.00, "Medição e Traçado", 15),
            ("Lente Conta Fio",              40.00, 35.00, "Medição e Traçado",  8),
            ("Óculos de sobrepor 3M",        30.00, 28.00, "Medição e Traçado", 10),
            ("Óculos simples 3M",            17.00, 15.00, "Medição e Traçado", 10),
            ("Régua 15cm",                    5.00,  3.00, "Medição e Traçado", 25),
            ("Régua 3 em 1",                 70.00, 65.00, "Medição e Traçado",  8),
            ("Régua 30cm",                    5.00,  3.00, "Medição e Traçado", 25),
            ("Régua Curvas",                  5.00,  5.00, "Medição e Traçado", 15),
            ("Régua mm 30cm",                20.00, 17.00, "Medição e Traçado", 15),
            ("Régua mm 60cm",                30.00, 28.00, "Medição e Traçado", 10),

            # Informática e Eletrônicos
            ("Cabo USB tipo C",              12.00, 10.00, "Informática e Eletrônicos", 20),
            ("Carregador de Celular V8 USB", 16.00, 14.00, "Informática e Eletrônicos", 15),
            ("Fone de Ouvido",               10.00,  8.00, "Informática e Eletrônicos", 20),
            ("Protetor auricular",            9.00,  7.00, "Informática e Eletrônicos", 15),

            # Escritório
            ("Abridor de casa",              5.00,  4.00, "Escritório", 15),
            ("Alicate de Pic",              37.00, 30.00, "Escritório", 10),
            ("Apontador",                    4.00,  3.00, "Escritório", 30),
            ("Bolinha de Pebolim (un)",       6.00,  5.00, "Escritório", 20),
            ("Bolinha de Ping Pong (un)",     3.00,  2.50, "Escritório", 30),
            ("Bolinha de Ping Pong (pacote com 4un)", 10.00, 9.00, "Escritório", 15),
            ("Bolsa SENAI",                  42.00, 36.50, "Escritório", 20),
            ("Borracha Artística",           10.00,  9.00, "Escritório", 25),
            ("Borracha branca",               2.50,  2.00, "Escritório", 30),
            ("Borracha Caneta",              13.50, 11.00, "Escritório", 20),
            ("Caixa de bobina",              10.00,  8.00, "Escritório", 15),
            ("Calculadora",                  18.00, 14.00, "Escritório", 10),
            ("Caneta Bic",                    2.50,  1.30, "Escritório", 50),
            ("Caneta Mágica fantasminha colorida", 9.00, 8.00, "Escritório", 20),
            ("Caneta Marca Texto",            7.00,  5.00, "Escritório", 30),
            ("Caneta para desenho Faber Castell 0.4", 10.00, 8.00, "Escritório", 20),
            ("Canetinha colorida c/ 12 cores",10.00, 8.50, "Escritório", 20),
            ("Carretilha cao de madeira",     6.00,  5.00, "Escritório", 15),
            ("Clips Nr 3/0",                  6.00,  5.00, "Escritório", 25),
            ("Cola bastão 10g",               5.00,  4.00, "Escritório", 30),
            ("Corretivo (Fita Corretiva)",    6.00,  5.00, "Escritório", 25),
            ("Cola Liquida",                  5.00,  4.50, "Escritório", 25),
            ("Cordão para crachá SENAI",      5.00,  4.00, "Escritório", 30),
            ("CÓPIA (Preto e branco) unitário", 3.00, 2.00, "Escritório", 999),
            ("Durex",                         4.00,  3.00, "Escritório", 30),
            ("Esfuminho",                     6.50,  5.50, "Escritório", 15),
            ("Estojo Organizador M",         20.00, 17.00, "Escritório", 15),
            ("Furador",                       6.00,  5.00, "Escritório", 15),
            ("Grafite Faber Castell e HB",    6.00,  5.00, "Escritório", 20),
            ("Grafite Leo&Leo 05,07 e 09mm",  4.00,  3.00, "Escritório", 20),
            ("Grampeador pequeno",           10.00,  9.00, "Escritório", 10),
            ("Grampo para grampeador cx. c/1000un", 3.00, 2.00, "Escritório", 20),
            ("Lápis HB nº2 e nº4",            2.00,  1.50, "Escritório", 40),
            ("Lapiseira 0,7mm",               7.00,  5.00, "Escritório", 25),
            ("Lapiseira 0,9mm",               7.00,  5.00, "Escritório", 25),
            ("Lapiseira 2,0mm",               7.00,  5.00, "Escritório", 20),
            ("Papel Canson",                 15.00, 12.00, "Papelaria", 30),
            ("Papel Kraft - rolo 10 metros", 18.00, 16.00, "Papelaria", 15),
            ("Papel Kraft Folha unitária",    3.00,  2.00, "Papelaria", 50),
            ("Papel Sulfite c/100f",         10.00,  8.50, "Papelaria", 20),
            ("Pasta com aba e elástico",      5.00,  4.00, "Papelaria", 20),
            ("Porta crachá",                  5.00,  4.00, "Escritório", 30),
        ]

        produtos = []
        for nome, preco_normal, preco_assoc, cat_key, estoque in produtos_raw:
            p = Produto(
                nome=nome,
                preco=preco_normal if preco_normal else preco_assoc,
                preco_associado=preco_assoc,
                estoque=estoque,
                disponivel=True,
                categoria_id=cats[cat_key].id,
                imagem=None,  # imagem adicionada depois pelo admin
            )
            produtos.append(p)

        db.add_all(produtos)
        db.commit()
        print(f"✅ Seed concluído! {len(categorias_nomes)} categorias e {len(produtos)} produtos inseridos.")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro no seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()