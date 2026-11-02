
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Pasta onde ficará o banco
PASTA_DATABASE = BASE_DIR / "database"
PASTA_DATABASE.mkdir(exist_ok=True)

# Endereço do banco SQLite
DATABASE_URL = f"sqlite:///{PASTA_DATABASE / 'techassist.db'}"

# Criar conexão
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Criar sessões para acessar o banco
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para os modelos
Base = declarative_base()
