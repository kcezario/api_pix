from fastapi import FastAPI
from app.routes import router
from app import config

print("TEST_MODE =", config.TEST_MODE)
print("CLIENT_ID =", config.CLIENT_ID)
print("CLIENT_SECRET =", config.CLIENT_SECRET)
print("CERT_PATH =", config.CERT_PATH)
print("KEY_PATH =", config.KEY_PATH)
print("PAGAMENTO_PIX_URL =", config.PAGAMENTO_PIX_URL)

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
