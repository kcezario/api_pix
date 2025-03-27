from pydantic import BaseModel, StringConstraints, validator
from typing_extensions import Annotated
import re

class PixPayment(BaseModel):
    key: str
    amount: float
    description: Annotated[str, StringConstraints(max_length=140)]

    @validator('key')
    def validate_pix_key(cls, v):
        if re.match(r'^\+\d{1,3}\d{1,14}$', v):
            return v  # Telefone válido (ex: +5511999998888)
        elif re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            return v  # E-mail válido
        elif re.match(r'^\d{11}$', v) or re.match(r'^\d{14}$', v):
            return v  # CPF ou CNPJ válido
        elif re.match(r'^[0-9a-fA-F]{32}$', v):
            return v  # EVP (chave aleatória) válido
        else:
            raise ValueError('Chave Pix inválida')