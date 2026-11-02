
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ia import responder
from app.database import engine, Base, SessionLocal
from app import models


app = FastAPI(
    title="TechAssist AI",
    description="Assistente inteligente para suporte técnico",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


# CONEXÃO COM O BANCO DE DADOS
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MODELO PARA MENSAGENS DA IA
class Mensagem(BaseModel):
    texto: str


# MODELO PARA CADASTRO DE CLIENTES
class ClienteCreate(BaseModel):
    nome: str
    telefone: str | None = None
    email: str | None = None


# MODELO PARA ABERTURA DE CHAMADOS
class AtendimentoCreate(BaseModel):
    cliente_id: int
    equipamento: str
    problema: str


# PÁGINA INICIAL
@app.get("/")
def inicio():
    return {
        "mensagem": "TechAssist AI iniciado!",
        "status": "Online"
    }


# SOBRE O PROJETO
@app.get("/sobre")
def sobre():
    return {
        "projeto": "TechAssist AI",
        "objetivo": "Automatizar atendimentos técnicos com inteligência artificial"
    }


# CHAT COM IA
@app.post("/chat")
def chat(dados: Mensagem):
    try:
        resposta = responder(dados.texto)

        return {
            "pergunta": dados.texto,
            "resposta": resposta
        }

    except Exception as erro:
        print(repr(erro))
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar a mensagem. Verifique o terminal."
        )


# CADASTRAR CLIENTE
@app.post("/clientes", status_code=201)
def cadastrar_cliente(
    dados: ClienteCreate,
    db: Session = Depends(get_db)
):
    cliente = models.Cliente(
        nome=dados.nome,
        telefone=dados.telefone,
        email=dados.email
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return {
        "mensagem": "Cliente cadastrado com sucesso!",
        "id": cliente.id,
        "nome": cliente.nome,
        "telefone": cliente.telefone,
        "email": cliente.email
    }


# LISTAR CLIENTES
@app.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes


# ABRIR CHAMADO
@app.post("/atendimentos", status_code=201)
def abrir_atendimento(
    dados: AtendimentoCreate,
    db: Session = Depends(get_db)
):
    cliente = db.get(models.Cliente, dados.cliente_id)

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    atendimento = models.Atendimento(
        cliente_id=dados.cliente_id,
        equipamento_id=dados.equipamento,
        problema=dados.problema,
        status="Aberto"
    )

    db.add(atendimento)
    db.commit()
    db.refresh(atendimento)

    return {
        "mensagem": "Atendimento aberto com sucesso!",
        "id": atendimento.id,
        "cliente": cliente.nome,
        "equipamento": atendimento.equipamento_id,
        "problema": atendimento.problema,
        "status": atendimento.status
    }


# LISTAR ATENDIMENTOS
@app.get("/atendimentos")
def listar_atendimentos(db: Session = Depends(get_db)):
    atendimentos = db.query(models.Atendimento).all()
    return atendimentos
