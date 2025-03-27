from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Pix API - Banco Inter",
    description="Realiza pagamentos via Pix usando a API do Banco Inter",
    version="1.0.0"
)

# Inclui as rotas do módulo de pagamento
app.include_router(router)

# Opcional: Health check
@app.get("/")
def read_root():
    return {"message": "API Pix do Banco Inter está rodando 🚀"}
