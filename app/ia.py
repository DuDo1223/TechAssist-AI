import os
from dotenv import load_dotenv
from openai import OpenAI
from app.prompts import INSTRUCOES

load_dotenv()
def responder(mensagem):
    chave = os.getenv("openai_api_key")
    if not(chave):
        raise ValueError("chave da API nao configurada.")
    cliente = OpenAI(api_key=chave)
    resposta= cliente.responses.create(
        model="gpt-6-luna",
        instructions=INSTRUCOES,
        input=mensagem

    )

    return resposta.output_text
