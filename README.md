pip install fastapi uvicorn[standard] jinja2 python-multipart sqlalchemy python-jose[cryptography] passlib[bcrypt] python-dotenv

pip freeze > requirements.txt
pip install -r requirements.txt

Depois de codar — sobe seu trabalho
Commit e push na sua branch
git add .
git commit -m "descrição do que fiz"
git push origin main primeiro e depos
git push origin jackelyne (ou yasmin)

O database.py vai na pasta app/ e o .env fica na raiz do projeto. O que cada parte faz:
engine — é a conexão com o SQLite. O check_same_thread: False é necessário porque o FastAPI usa threads diferentes por requisição e o SQLite reclamaria disso.
SessionLocal — é a "sessão" do banco. Toda vez que uma rota precisa acessar o banco, ela abre uma sessão nova e fecha no final.
Base — é a classe que todos os seus models vão herdar. Quando você fizer class Produto(Base), o SQLAlchemy sabe que aquilo é uma tabela.
get_db() — é a dependência que os routers vão usar com Depends(get_db) pra receber a sessão do banco automaticamente.
criar_tabelas() — vai ser chamada no main.py na inicialização. Ela lê todos os models e cria as tabelas no banco se ainda não existirem.
O aapm.db vai aparecer na raiz do projeto automaticamente quando você rodar o sistema pela primeira vez — não precisa criar na mão.

Agora precisa criar um __init__.py dentro de app/models/ pra o Python reconhecer a pasta como módulo e importar tudo junto:
python# app/models/__init__.py
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.fornecedor import Fornecedor
from app.models.produto import Produto
from app.models.venda import Venda, ItemVenda, Nota
Cria esse arquivo na mão mesmo, são só essas 5 linhas. Isso garante que quando o seed.py e os routers importarem os models, todos já estejam carregados e as relações entre tabelas funcionem.

# Instale as dependências se ainda não tiver
pip install fastapi uvicorn sqlalchemy python-jose passlib[bcrypt] python-dotenv python-multipart

# Popula o banco
python seed.py

# Sobe o servidor
uvicorn main:app --reload

python -m venv venv ambiente virtual
venv\Scripts\activate abrindo ambiente virtual 
